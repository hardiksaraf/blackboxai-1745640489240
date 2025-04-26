from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomerProfile, AddressBook, Wishlist, SavedCards
from .forms import CustomerProfileForm, AddressForm, SavedCardForm

@login_required
def dashboard(request):
    profile = CustomerProfile.objects.get(user=request.user)
    wishlist = Wishlist.objects.filter(customer=profile)
    saved_cards = SavedCards.objects.filter(customer=profile)
    context = {
        'profile': profile,
        'wishlist': wishlist,
        'saved_cards': saved_cards,
    }
    return render(request, 'customers/dashboard.html', context)

@login_required
def profile_view(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('customers:profile')
    else:
        form = CustomerProfileForm(instance=profile)
    return render(request, 'customers/profile.html', {'form': form})

@login_required
def address_list(request):
    profile = CustomerProfile.objects.get(user=request.user)
    addresses = AddressBook.objects.filter(customer=profile)
    return render(request, 'customers/address_list.html', {'addresses': addresses})

@login_required
def add_address(request):
    profile = CustomerProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.customer = profile
            address.save()
            messages.success(request, "Address added successfully.")
            return redirect('customers:address_list')
    else:
        form = AddressForm()
    return render(request, 'customers/add_address.html', {'form': form})

@login_required
def wishlist_view(request):
    profile = CustomerProfile.objects.get(user=request.user)
    wishlist = Wishlist.objects.filter(customer=profile)
    return render(request, 'customers/wishlist.html', {'wishlist': wishlist})

@login_required
def saved_cards_view(request):
    profile = CustomerProfile.objects.get(user=request.user)
    saved_cards = SavedCards.objects.filter(customer=profile)
    return render(request, 'customers/saved_cards.html', {'saved_cards': saved_cards})
