from django import forms

from Faculty.models import *


class CreateUnits(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'global_unit'
        ]
        widgets = {
            'global_unit': forms.CheckboxInput(),
        }
