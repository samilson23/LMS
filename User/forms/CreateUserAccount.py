from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CreateUserAccount(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}), required=True)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}), required=True)
    email = forms.CharField(required=False, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'middle_name', 'last_name',
                  'password1', 'password2', 'is_active']
        help_texts = {
            'is_active': None,
            'username': None,
            'password1': None,
            'password2': None,
        }
        labels = {'email': 'Email', 'is_active': ''}
        widgets = {'username': forms.TextInput(
            attrs={'class': 'form-control', 'id': 'id_username', 'placeholder': 'Username', 'autocomplete': 'off'}),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'First Name', 'autocomplete': 'off'}),
            'middle_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Middle Name', 'autocomplete': 'off'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Last Name', 'autocomplete': 'off'}),
            'is_active': forms.CheckboxInput(attrs={'disabled': 'disabled', 'hidden': 'hidden'}),
        }
