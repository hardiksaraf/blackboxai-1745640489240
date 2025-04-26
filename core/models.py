from django.db import models
from django.utils.translation import gettext_lazy as _

class SiteConfiguration(models.Model):
    """Site-wide configuration settings"""
    
    site_name = models.CharField(max_length=100, default='RentMyVenue')
    site_description = models.TextField(blank=True)
    maintenance_mode = models.BooleanField(default=False)
    contact_email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    # Social Media Links
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # SEO Fields
    meta_keywords = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=255, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    
    # Footer Content
    footer_text = models.TextField(blank=True)
    copyright_text = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = _('Site Configuration')
        verbose_name_plural = _('Site Configuration')

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteConfiguration.objects.exists():
            return
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    """Store contact form submissions"""
    
    INQUIRY_TYPES = (
        ('general', _('General Inquiry')),
        ('support', _('Customer Support')),
        ('business', _('Business Partnership')),
        ('feedback', _('Feedback')),
        ('other', _('Other')),
    )
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_messages'
    )
    resolution_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Testimonial(models.Model):
    """Customer testimonials to be displayed on the site"""
    
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True)
    content = models.TextField()
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        default=5
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Testimonial')
        verbose_name_plural = _('Testimonials')

    def __str__(self):
        return f"{self.name} - {self.company}"

class FAQ(models.Model):
    """Frequently Asked Questions"""
    
    CATEGORIES = (
        ('general', _('General')),
        ('booking', _('Booking & Reservations')),
        ('payment', _('Payment & Pricing')),
        ('cancellation', _('Cancellation & Refunds')),
        ('venue', _('Venue Related')),
        ('account', _('Account & Profile')),
        ('other', _('Other')),
    )
    
    category = models.CharField(max_length=20, choices=CATEGORIES)
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['category', 'order']
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')

    def __str__(self):
        return self.question
