from django import forms
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from Student.models import CHOICES
from Student.models import Students

User = get_user_model()


class CreateSTDProfile(forms.ModelForm):
    phone_number = PhoneNumberField(widget=PhoneNumberPrefixWidget(initial='KE'))
    nationality = CountryField(blank_label='Select country').formfield(
        widget=CountrySelectWidget(
            attrs={'class': 'form-control'}
        )
    )

    gender = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)

    class Meta:
        model = Students
        fields = [
            'phone_number', 'id_no', 'nationality', 'address', 'gender'
        ]
        widgets = {
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Address', 'autocomplete': 'off'}),
            'id_no': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'ID Number', 'autocomplete': 'off'})
        }


class STDDetails(forms.ModelForm):
    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['profile_pic', 'first_name', 'middle_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'off'}),
            'middle_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Middle Name', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'off'}),
        }
