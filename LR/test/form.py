from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(_("Passwords do not match"))
        if len(password2) < 8:
            raise ValidationError(_("Password is too short"))
        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
   
        self.fields['username'].error_messages = {
            'unique': 'Change username.',
        }
        self.fields['email'].error_messages = {
            'invalid': 'Enter a valid email address.',
            'required': 'This field is required.',
            'unique': 'A user already exists.',
        }
        self.fields['password2'].error_messages = {
            'password_mismatch': 'Passwords do not match.',
        }
