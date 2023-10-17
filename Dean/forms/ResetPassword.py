from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ChangePassword(forms.ModelForm):
    password1 = forms.CharField(required=False, label='New Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'New Password'}))

    password2 = forms.CharField(required=False, label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['password1', 'password2']

        help_texts = {
            'password1': None,
            'password2': None,
        }
