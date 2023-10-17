from django import forms
from django.contrib.auth import get_user_model

from User.models import CHOICES

User = get_user_model()


class EditUserAccounts(forms.ModelForm):
    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    usertype = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 'profile_pic', 'usertype']

        widgets = {'username': forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'off'}),
            'middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'Middle Name', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'off'})
        }
