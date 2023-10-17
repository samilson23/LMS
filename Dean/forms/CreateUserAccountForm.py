from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateUserAccount(forms.ModelForm):
    CHOICES = [
        ('HOD', 'HOD'),
        ('LECTURER', 'LECTURER'),
        ('STUDENT', 'STUDENT'),
    ]
    password1 = forms.CharField(required=False, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'hidden': 'hidden'}))

    password2 = forms.CharField(required=False, label='', widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'hidden': 'hidden'}))

    usertype = forms.ChoiceField(widget=forms.RadioSelect(), choices=CHOICES)

    class Meta:
        model = User
        fields = ['username', 'usertype']

        help_texts = {
            'username': None,
            'password1': None,
            'password2': None,
        }

        widgets = {'username': forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': 'Username', 'autocomplete': 'off'}),
        }
