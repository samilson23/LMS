from django import forms
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from Dean.models import Dean, CHOICES

User = get_user_model()


class DeanProfile(forms.ModelForm):
    class Meta:
        model = Dean
        fields = [
            'faculty'
        ]
        widgets = {
            'faculty': forms.Select(attrs={'class': 'form-control'})
        }
