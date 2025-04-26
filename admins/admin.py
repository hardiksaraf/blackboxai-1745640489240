from django.contrib import admin
from .models import AdminAnalytics, UserReport

@admin.register(AdminAnalytics)
class AdminAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_users', 'total_vendors', 'total_bookings', 'total_revenue')
    ordering = ('-date',)

@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ('reported_user', 'reported_by', 'reason', 'created_at', 'resolved')
    list_filter = ('resolved', 'created_at')
    search_fields = ('reported_user__email', 'reported_by__email', 'reason')
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(resolved=True)
    mark_resolved.short_description = "Mark selected reports as resolved"
