from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """Custom user model with additional fields"""
    
    class UserType(models.TextChoices):
        CUSTOMER = 'customer', _('Customer')
        VENDOR = 'vendor', _('Vendor')
        ADMIN = 'admin', _('Admin')

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CUSTOMER,
    )
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        null=True,
        blank=True
    )
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return self.email

    @property
    def is_customer(self):
        return self.user_type == self.UserType.CUSTOMER

    @property
    def is_vendor(self):
        return self.user_type == self.UserType.VENDOR

    @property
    def is_admin_user(self):
        return self.user_type == self.UserType.ADMIN

class UserProfile(models.Model):
    """Extended profile information for users"""
    
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s profile"

class UserSession(models.Model):
    """Track user sessions for security"""
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    session_key = models.CharField(max_length=40)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)
    last_activity = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_activity']

    def __str__(self):
        return f"{self.user.email} - {self.ip_address}"

class EmailVerification(models.Model):
    """Email verification tokens"""
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='email_verifications'
    )
    token = models.CharField(max_length=64, unique=True)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Email verification for {self.user.email}"
