from string import Template

from django import forms
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe

from User.models import CHOICES

User = get_user_model()


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""<>""")
        return mark_safe(html)


class CreateUserAccount(forms.ModelForm):
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
