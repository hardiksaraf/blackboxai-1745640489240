from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationType(models.TextChoices):
    BOOKING = 'booking', 'Booking'
    PAYMENT = 'payment', 'Payment'
    SYSTEM = 'system', 'System'
    OTHER = 'other', 'Other'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.OTHER)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return f"Notification for {self.user.email} - {self.type}"

class ChannelPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='channel_preferences')
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Channel Preference"
        verbose_name_plural = "Channel Preferences"

    def __str__(self):
        return f"Channel Preferences for {self.user.email}"
