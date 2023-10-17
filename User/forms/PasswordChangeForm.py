from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class PasswordChange(PasswordChangeForm):
    old_password = forms.CharField(label="Old Password", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'auto-focus': True, 'class': 'form-control',
               'placeholder': 'Current Password'}))
    new_password1 = forms.CharField(label="New Password", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label="Confirm Password", strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        help_texts = {
            'old_password': None,
            'password1': None,
            'password2': None,
        }
