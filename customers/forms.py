from django import forms
from .models import CustomerProfile, AddressBook, SavedCards

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['full_name', 'date_of_birth', 'gender', 'profile_picture']

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressBook
        fields = ['address_line1', 'address_line2', 'city', 'state', 'country', 'postal_code', 'address_type', 'is_default']

class SavedCardForm(forms.ModelForm):
    class Meta:
        model = SavedCards
        fields = ['card_last4', 'card_type', 'expiry_month', 'expiry_year']
