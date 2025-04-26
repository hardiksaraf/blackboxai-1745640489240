from django.contrib import admin
from .models import VendorProfile, KYC, VendorAnalytics

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'business_name', 'verification_status')
    search_fields = ('user__email', 'business_name')
    list_filter = ('verification_status',)

@admin.register(KYC)
class KYCAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'document_type', 'status', 'verified_by', 'created_at')
    search_fields = ('vendor__business_name', 'document_number')
    list_filter = ('status',)

@admin.register(VendorAnalytics)
class VendorAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'total_listings', 'total_bookings', 'total_revenue')
    search_fields = ('vendor__business_name',)
