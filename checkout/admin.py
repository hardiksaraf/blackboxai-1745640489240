from django.contrib import admin
from .models import Cart, OrderSummary

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'created_at')
    search_fields = ('customer__email',)
    ordering = ('-created_at',)

@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'booking', 'final_price', 'coupon_applied', 'summary_time')
    search_fields = ('customer__email', 'booking__id')
    ordering = ('-summary_time',)
