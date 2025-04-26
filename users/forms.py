from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users"""
    
    user_type = forms.ChoiceField(
        choices=CustomUser.UserType.choices,
        widget=forms.RadioSelect,
        initial=CustomUser.UserType.CUSTOMER
    )
    
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input rounded-md shadow-sm mt-1 block w-full'})
    )
    
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
        })
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'user_type', 'phone_number', 'date_of_birth')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

class CustomUserChangeForm(UserChangeForm):
    """Form for updating users"""
    
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'phone_number', 'date_of_birth')

class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information"""
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'location', 'website', 'company_name')
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-textarea rounded-md shadow-sm mt-1 block w-full'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
            })
        }

class ProfilePictureForm(forms.ModelForm):
    """Form for updating profile picture"""
    
    class Meta:
        model = CustomUser
        fields = ('profile_picture',)
        widgets = {
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-input rounded-md shadow-sm mt-1 block w-full',
                'accept': 'image/*'
            })
        }

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            # Validate file size (max 5MB)
            if profile_picture.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size must be less than 5MB.')
            
            # Validate file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif']
            if profile_picture.content_type not in allowed_types:
                raise ValidationError('Please upload a valid image file (JPEG, PNG, or GIF).')
        
        return profile_picture

class EmailChangeForm(forms.Form):
    """Form for changing email address"""
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input rounded-md shadow-sm mt-1 block w-full'
        })
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email']
        if email == self.user.email:
            raise ValidationError('This is your current email address.')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if not self.user.check_password(password):
            raise ValidationError('Invalid password.')
        return password
