from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    payment_method = forms.CharField(max_length=50)
    # Additional fields as needed

class RefundForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    reason = forms.CharField(widget=forms.Textarea)
