from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminAnalytics(models.Model):
    # Placeholder for admin analytics data
    date = models.DateField()
    total_users = models.PositiveIntegerField()
    total_vendors = models.PositiveIntegerField()
    total_bookings = models.PositiveIntegerField()
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Admin Analytics"
        verbose_name_plural = "Admin Analytics"

    def __str__(self):
        return f"Analytics for {self.date}"

class UserReport(models.Model):
    reported_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reports_made')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_resolved')

    class Meta:
        verbose_name = "User Report"
        verbose_name_plural = "User Reports"

    def __str__(self):
        return f"Report on {self.reported_user} by {self.reported_by}"
