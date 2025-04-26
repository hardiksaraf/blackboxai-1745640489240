from django import forms
from .models import VendorProfile, KYC

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ['business_name', 'gst_number', 'business_license', 'logo', 'about']

class KYCForm(forms.ModelForm):
    class Meta:
        model = KYC
        fields = ['document_type', 'document_number', 'file_upload']
