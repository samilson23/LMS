from django import forms

from Faculty.models import InterSchooltransfer, ResultSlip, KCSEResults


class InterSchoolTransfersForm(forms.ModelForm):
    class Meta:
        model = InterSchooltransfer
        fields = ['new_programme', 'reason', 'aggregate']
        widgets = {
            'aggregate': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'i.e A- (78 points)', 'autocomplete': 'off'}),
        }


class KCSEResultsForm(forms.ModelForm):
    class Meta:
        model = KCSEResults
        fields = ['subject', 'grade']


class ResultSlipForm(forms.ModelForm):
    class Meta:
        model = ResultSlip
        fields = ['kcse_result_slip']
