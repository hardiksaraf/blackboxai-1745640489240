from django.contrib import admin
from .models import Transaction, Refund, PaymentMethod

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'customer', 'amount', 'currency', 'status', 'gateway', 'payment_time')
    list_filter = ('status', 'gateway', 'payment_time')
    search_fields = ('customer__email', 'booking__id')
    ordering = ('-payment_time',)

@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('id', 'transaction', 'amount', 'status', 'processed_at')
    list_filter = ('status', 'processed_at')
    search_fields = ('transaction__id',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'method_type', 'is_active')
    list_filter = ('method_type', 'is_active')
    search_fields = ('customer__email', 'gateway_reference')
