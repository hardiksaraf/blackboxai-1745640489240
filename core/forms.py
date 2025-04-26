from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """Form for contact page submissions"""
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Your full name'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'your.email@example.com'
        })
    )
    
    phone = forms.CharField(
        validators=[phone_regex],
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': '+1234567890'
        })
    )
    
    inquiry_type = forms.ChoiceField(
        choices=ContactMessage.INQUIRY_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select rounded-md shadow-sm mt-1 block w-full'
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Brief subject of your inquiry'
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full',
            'rows': 5,
            'placeholder': 'Please provide details about your inquiry...'
        })
    )
    
    # Add honeypot field for spam prevention
    honeypot = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none;',
            'tabindex': '-1',
            'autocomplete': 'off'
        })
    )

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'inquiry_type', 'subject', 'message']

    def clean_honeypot(self):
        """Check if honeypot field is empty (spam prevention)"""
        honeypot = self.cleaned_data['honeypot']
        if honeypot:
            raise forms.ValidationError(
                _('Spam detection triggered. Please try again.')
            )
        return honeypot

class NewsletterSubscriptionForm(forms.Form):
    """Form for newsletter subscriptions"""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Enter your email address'
        })
    )
    
    consent = forms.BooleanField(
        required=True,
        label=_('I agree to receive marketing emails and can unsubscribe at any time.'),
        widget=forms.CheckboxInput(attrs={
            'class': 'form-checkbox h-4 w-4 text-indigo-600'
        })
    )

class SearchForm(forms.Form):
    """Form for the main search functionality"""
    
    SORT_CHOICES = (
        ('relevance', _('Relevance')),
        ('price_low', _('Price: Low to High')),
        ('price_high', _('Price: High to Low')),
        ('rating', _('Rating')),
        ('newest', _('Newest')),
    )
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Search venues...',
            'x-model': 'searchQuery'
        })
    )
    
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Enter location',
            'x-model': 'location'
        })
    )
    
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'x-model': 'date'
        })
    )
    
    guests = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
            'placeholder': 'Number of guests',
            'x-model': 'guests'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select rounded-md shadow-sm mt-1 block w-full',
            'x-model': 'sortBy'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        # Add any cross-field validation if needed
        return cleaned_data
