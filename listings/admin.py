from django.contrib import admin
from .models import Venue, VenueType, Feature, Gallery, AvailabilityCalendar

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor', 'venue_type', 'price_per_day', 'capacity', 'is_active', 'is_featured', 'created_at')
    list_filter = ('is_active', 'is_featured', 'venue_type')
    search_fields = ('title', 'vendor__business_name', 'address')
    ordering = ('-created_at',)

@admin.register(VenueType)
class VenueTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('feature_name', 'venue')
    search_fields = ('feature_name', 'venue__title')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('venue', 'is_primary')
    list_filter = ('is_primary',)

@admin.register(AvailabilityCalendar)
class AvailabilityCalendarAdmin(admin.ModelAdmin):
    list_display = ('venue', 'date', 'is_available')
    list_filter = ('is_available', 'date')
    search_fields = ('venue__title',)
