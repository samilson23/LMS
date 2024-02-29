from django import forms

from Faculty.models import *


class CreateFaculties(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = [
            'name'
        ]
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Faculty Name', 'autocomplete': 'off'}),
        }
