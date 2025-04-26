from django.contrib import admin
from .models import Booking, CancellationPolicy

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'venue', 'start_date', 'end_date', 'status', 'total_amount', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'start_date', 'end_date')
    search_fields = ('customer__email', 'venue__title')
    ordering = ('-created_at',)

@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = ('venue', 'refund_percentage')
    search_fields = ('venue__title',)
