from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VendorProfile, KYC, VendorAnalytics
from .forms import VendorProfileForm, KYCForm

@login_required
def dashboard(request):
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)
    analytics = VendorAnalytics.objects.filter(vendor=vendor_profile).first()
    context = {
        'vendor_profile': vendor_profile,
        'analytics': analytics,
    }
    return render(request, 'vendors/dashboard.html', context)

@login_required
def profile_edit(request):
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Vendor profile updated successfully.")
            return redirect('vendors:dashboard')
    else:
        form = VendorProfileForm(instance=vendor_profile)
    return render(request, 'vendors/profile_edit.html', {'form': form})

@login_required
def kyc_upload(request):
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.vendor = vendor_profile
            kyc.save()
            messages.success(request, "KYC document uploaded successfully.")
            return redirect('vendors:dashboard')
    else:
        form = KYCForm()
    return render(request, 'vendors/kyc_upload.html', {'form': form})

@login_required
def listing_management(request):
    vendor_profile = get_object_or_404(VendorProfile, user=request.user)
    listings = vendor_profile.venues.all()
    return render(request, 'vendors/listing_management.html', {'listings': listings})
