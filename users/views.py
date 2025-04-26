from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from django.db import transaction

from .models import CustomUser, UserProfile, EmailVerification
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    UserProfileForm,
    ProfilePictureForm,
    EmailChangeForm
)

import uuid
from datetime import timedelta

def register(request):
    """Handle user registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user = form.save(commit=False)
                user.is_active = False  # User needs to verify email first
                user.save()
                
                # Create user profile
                UserProfile.objects.create(user=user)
                
                # Create email verification token
                token = uuid.uuid4().hex
                expiry = timezone.now() + timedelta(days=2)
                EmailVerification.objects.create(
                    user=user,
                    token=token,
                    expires_at=expiry
                )
                
                # Send verification email
                verification_url = request.build_absolute_uri(
                    reverse('users:verify_email', kwargs={'token': token})
                )
                send_verification_email(user, verification_url)
                
                messages.success(
                    request,
                    'Registration successful. Please check your email to verify your account.'
                )
                return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

def verify_email(request, token):
    """Handle email verification"""
    verification = get_object_or_404(
        EmailVerification,
        token=token,
        is_used=False,
        expires_at__gt=timezone.now()
    )
    
    with transaction.atomic():
        user = verification.user
        user.is_email_verified = True
        user.is_active = True
        user.save()
        
        verification.is_used = True
        verification.save()
    
    messages.success(request, 'Email verified successfully. You can now log in.')
    return redirect('users:login')

@login_required
def profile(request):
    """Display and update user profile"""
    user = request.user
    profile = user.profile
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        picture_form = ProfilePictureForm(request.POST, request.FILES, instance=user)
        
        if user_form.is_valid() and profile_form.is_valid() and picture_form.is_valid():
            user_form.save()
            profile_form.save()
            if 'profile_picture' in request.FILES:
                picture_form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('users:profile')
    else:
        user_form = CustomUserChangeForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
        picture_form = ProfilePictureForm(instance=user)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'picture_form': picture_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def change_email(request):
    """Handle email change requests"""
    if request.method == 'POST':
        form = EmailChangeForm(request.user, request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['email']
            
            # Create verification token for new email
            token = uuid.uuid4().hex
            expiry = timezone.now() + timedelta(days=2)
            
            verification = EmailVerification.objects.create(
                user=request.user,
                token=token,
                expires_at=expiry
            )
            
            # Send verification email to new address
            verification_url = request.build_absolute_uri(
                reverse('users:verify_email_change', kwargs={'token': token})
            )
            send_email_change_verification(request.user, new_email, verification_url)
            
            messages.success(
                request,
                'Please check your new email address to confirm the change.'
            )
            return redirect('users:profile')
    else:
        form = EmailChangeForm(request.user)
    
    return render(request, 'users/change_email.html', {'form': form})

@login_required
def verify_email_change(request, token):
    """Verify email change request"""
    verification = get_object_or_404(
        EmailVerification,
        token=token,
        is_used=False,
        expires_at__gt=timezone.now()
    )
    
    with transaction.atomic():
        user = verification.user
        new_email = verification.new_email
        
        # Update email
        user.email = new_email
        user.save()
        
        verification.is_used = True
        verification.save()
    
    messages.success(request, 'Email address changed successfully.')
    return redirect('users:profile')

def send_verification_email(user, verification_url):
    """Send email verification link"""
    subject = 'Verify your email address'
    message = render_to_string('users/emails/verify_email.html', {
        'user': user,
        'verification_url': verification_url
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_email_change_verification(user, new_email, verification_url):
    """Send email change verification link"""
    subject = 'Confirm your new email address'
    message = render_to_string('users/emails/verify_email_change.html', {
        'user': user,
        'verification_url': verification_url
    })
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [new_email],
        fail_silently=False,
    )

@login_required
def dashboard(request):
    """User dashboard view"""
    if request.user.is_vendor:
        return redirect('vendors:dashboard')
    elif request.user.is_customer:
        return redirect('customers:dashboard')
    else:
        return redirect('admins:dashboard')
