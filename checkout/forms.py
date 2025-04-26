from django import forms

class AddressForm(forms.Form):
    address_line1 = forms.CharField(max_length=255)
    address_line2 = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    address_type = forms.ChoiceField(choices=[('billing', 'Billing'), ('shipping', 'Shipping')])

class PromoCodeForm(forms.Form):
    code = forms.CharField(max_length=50)
