from django.db import models
from django.contrib.auth import get_user_model
from listings.models import Venue
from bookings.models import Booking

User = get_user_model()

class Cart(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    items = models.ManyToManyField(Venue, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return f"Cart {self.id} for {self.customer.email}"

class OrderSummary(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='order_summaries')
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon_applied = models.ForeignKey('coupons.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    summary_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Order Summary"
        verbose_name_plural = "Order Summaries"

    def __str__(self):
        return f"Order Summary {self.id} for {self.customer.email}"
