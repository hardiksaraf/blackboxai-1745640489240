from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Venue

User = get_user_model()

class BookingStatus(models.TextChoices):
    BOOKED = 'booked', 'Booked'
    CANCELLED = 'cancelled', 'Cancelled'
    PENDING = 'pending', 'Pending'

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __str__(self):
        return f"Booking {self.id} - {self.venue.title} by {self.customer.email}"

class CancellationPolicy(models.Model):
    venue = models.OneToOneField(Venue, on_delete=models.CASCADE, related_name='cancellation_policy')
    policy_text = models.TextField()
    refund_percentage = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Cancellation Policy"
        verbose_name_plural = "Cancellation Policies"

    def __str__(self):
        return f"Cancellation Policy for {self.venue.title}"
