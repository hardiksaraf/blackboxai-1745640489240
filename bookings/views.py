from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, BookingStatus
from listings.models import Venue
from datetime import date

@login_required
def create_booking(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id, is_active=True)
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        # Validate dates
        if not start_date or not end_date:
            messages.error(request, "Please provide both start and end dates.")
            return redirect('listings:detail', venue_id=venue.id)
        if start_date > end_date:
            messages.error(request, "End date must be after start date.")
            return redirect('listings:detail', venue_id=venue.id)
        # Check availability (simplified)
        # TODO: Implement proper availability check
        booking = Booking.objects.create(
            customer=request.user,
            venue=venue,
            start_date=start_date,
            end_date=end_date,
            status=BookingStatus.PENDING,
            total_amount=venue.price_per_day  # Simplified, should calculate based on days
        )
        messages.success(request, "Booking created successfully. Please proceed to payment.")
        return redirect('bookings:detail', booking_id=booking.id)
    return render(request, 'bookings/create_booking.html', {'venue': venue})

@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if booking.status == BookingStatus.CANCELLED:
        messages.info(request, "Booking is already cancelled.")
    else:
        booking.status = BookingStatus.CANCELLED
        booking.save()
        messages.success(request, "Booking cancelled successfully.")
    return redirect('bookings:detail', booking_id=booking.id)

@login_required
def reschedule_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        new_start_date = request.POST.get('start_date')
        new_end_date = request.POST.get('end_date')
        # Validate dates
        if not new_start_date or not new_end_date:
            messages.error(request, "Please provide both new start and end dates.")
            return redirect('bookings:reschedule', booking_id=booking.id)
        if new_start_date > new_end_date:
            messages.error(request, "End date must be after start date.")
            return redirect('bookings:reschedule', booking_id=booking.id)
        # TODO: Check availability
        booking.start_date = new_start_date
        booking.end_date = new_end_date
        booking.status = BookingStatus.PENDING
        booking.save()
        messages.success(request, "Booking rescheduled successfully.")
        return redirect('bookings:detail', booking_id=booking.id)
    return render(request, 'bookings/reschedule_booking.html', {'booking': booking})
