from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from listings.models import Venue
from .models import Cart, OrderSummary
from .forms import AddressForm, PromoCodeForm

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(customer=request.user)
    return render(request, 'checkout/cart.html', {'cart': cart})

@login_required
def add_to_cart(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id, is_active=True)
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart.items.add(venue)
    messages.success(request, f"{venue.title} added to your cart.")
    return redirect('checkout:cart')

@login_required
def remove_from_cart(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    cart = get_object_or_404(Cart, customer=request.user)
    cart.items.remove(venue)
    messages.success(request, f"{venue.title} removed from your cart.")
    return redirect('checkout:cart')

@login_required
def address_selection(request):
    # Placeholder for address selection logic
    return render(request, 'checkout/address_selection.html')

@login_required
def order_summary(request):
    # Placeholder for order summary logic
    return render(request, 'checkout/order_summary.html')

@login_required
def apply_promo_code(request):
    if request.method == 'POST':
        form = PromoCodeForm(request.POST)
        if form.is_valid():
            # Placeholder for promo code application logic
            messages.success(request, "Promo code applied successfully.")
        else:
            messages.error(request, "Invalid promo code.")
    return redirect('checkout:cart')
