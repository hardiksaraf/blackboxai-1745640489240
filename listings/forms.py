from django import forms
from .models import Venue, Feature, Gallery

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['title', 'description', 'price_per_day', 'capacity', 'address', 'venue_type', 'location', 'is_active', 'is_featured']

class FeatureForm(forms.ModelForm):
    class Meta:
        model = Feature
        fields = ['feature_name']

class GalleryForm(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['image_file', 'is_primary']
