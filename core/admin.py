from django.contrib import admin
from django.utils.html import format_html
from .models import SiteConfiguration, ContactMessage, Testimonial, FAQ

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """Admin interface for SiteConfiguration model"""
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_description', 'maintenance_mode')
        }),
        ('Contact Information', {
            'fields': ('contact_email', 'phone_number', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_keywords', 'meta_description', 'google_analytics_id'),
            'classes': ('collapse',)
        }),
        ('Footer Content', {
            'fields': ('footer_text', 'copyright_text')
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent creating multiple instances
        return not SiteConfiguration.objects.exists()

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """Admin interface for ContactMessage model"""
    
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'created_at', 'is_resolved')
    list_filter = ('inquiry_type', 'is_resolved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'inquiry_type')
        }),
        ('Message Content', {
            'fields': ('subject', 'message')
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_by', 'resolution_notes')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if obj.is_resolved and not obj.resolved_by:
            obj.resolved_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    """Admin interface for Testimonial model"""
    
    list_display = ('name', 'company', 'rating_stars', 'is_featured', 'created_at')
    list_filter = ('rating', 'is_featured', 'created_at')
    search_fields = ('name', 'company', 'content')
    list_editable = ('is_featured',)
    
    def rating_stars(self, obj):
        """Display rating as stars in the admin list view"""
        stars = '★' * obj.rating + '☆' * (5 - obj.rating)
        return format_html(
            '<span style="color: #FFD700;">{}</span>',
            stars
        )
    rating_stars.short_description = 'Rating'

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """Admin interface for FAQ model"""
    
    list_display = ('question', 'category', 'order', 'is_published')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_published')
    
    fieldsets = (
        (None, {
            'fields': ('category', 'question', 'answer')
        }),
        ('Publishing', {
            'fields': ('order', 'is_published')
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
        js = ('admin/js/faq_order.js',)

# Register custom admin site header and title
admin.site.site_header = 'RentMyVenue Administration'
admin.site.site_title = 'RentMyVenue Admin'
admin.site.index_title = 'Welcome to RentMyVenue Admin Panel'
