from django.contrib import admin
from .models import Notification, ChannelPreference

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'message', 'read', 'created_at')
    list_filter = ('type', 'read', 'created_at')
    search_fields = ('user__email', 'message')

@admin.register(ChannelPreference)
class ChannelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_enabled', 'sms_enabled', 'push_enabled')
    search_fields = ('user__email',)
