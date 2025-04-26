from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor_profile')
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=50, blank=True)
    business_license = models.FileField(upload_to='vendor_licenses/', blank=True, null=True)
    verification_status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending')
    logo = models.ImageField(upload_to='vendor_logos/', blank=True, null=True)
    about = models.TextField(blank=True)

    def __str__(self):
        return self.business_name

class KYC(models.Model):
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=100)
    document_number = models.CharField(max_length=100)
    file_upload = models.FileField(upload_to='kyc_documents/')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_kyc_documents')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} - {self.document_number}"

class VendorAnalytics(models.Model):
    vendor = models.OneToOneField(VendorProfile, on_delete=models.CASCADE, related_name='analytics')
    total_listings = models.PositiveIntegerField(default=0)
    total_bookings = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Analytics for {self.vendor.business_name}"
