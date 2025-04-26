from django import forms
from .models import UserReport

class UserReportForm(forms.ModelForm):
    class Meta:
        model = UserReport
        fields = ['reported_user', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4}),
        }
