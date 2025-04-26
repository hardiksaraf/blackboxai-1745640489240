from django import forms
from .models import ChannelPreference

class ChannelPreferenceForm(forms.ModelForm):
    class Meta:
        model = ChannelPreference
        fields = ['email_enabled', 'sms_enabled', 'push_enabled']
        widgets = {
            'email_enabled': forms.CheckboxInput(),
            'sms_enabled': forms.CheckboxInput(),
            'push_enabled': forms.CheckboxInput(),
        }
