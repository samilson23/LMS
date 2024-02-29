from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class EditUserAccounts(forms.ModelForm):
    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 'profile_pic']

        widgets = {'username': forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off', 'disabled': 'disabled'}),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'off'}),
            'middle_name': forms.TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'Middle Name', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'off'}),
        }
