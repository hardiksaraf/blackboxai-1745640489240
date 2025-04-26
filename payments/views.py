from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Transaction, Refund, PaymentMethod
from bookings.models import Booking

@login_required
def payment_gateway(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        # Placeholder for payment processing logic
        messages.success(request, "Payment processed successfully.")
        return redirect('payments:receipt', booking_id=booking.id)
    return render(request, 'payments/payment_gateway.html', {'booking': booking})

@login_required
def payment_receipt(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    transaction = Transaction.objects.filter(booking=booking).last()
    return render(request, 'payments/receipt.html', {'transaction': transaction})

@login_required
def refund_request(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, customer=request.user)
    if request.method == 'POST':
        # Placeholder for refund request logic
        messages.success(request, "Refund request submitted.")
        return redirect('payments:receipt', booking_id=transaction.booking.id)
    return render(request, 'payments/refund_request.html', {'transaction': transaction})

@login_required
def saved_cards(request):
    payment_methods = PaymentMethod.objects.filter(customer=request.user)
    return render(request, 'payments/saved_cards.html', {'payment_methods': payment_methods})
