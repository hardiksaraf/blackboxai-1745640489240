from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class VenueType(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Venue(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues')
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    address = models.TextField()
    venue_type = models.ForeignKey(VenueType, on_delete=models.SET_NULL, null=True, related_name='venues')
    location = models.CharField(max_length=255, blank=True)  # Could be GeoDjango field
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Feature(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='features')
    feature_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.feature_name} ({self.venue.title})"

class Gallery(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='venue_images/')
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.venue.title}"

class AvailabilityCalendar(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('venue', 'date')

    def __str__(self):
        return f"{self.venue.title} - {self.date} - {'Available' if self.is_available else 'Unavailable'}"
