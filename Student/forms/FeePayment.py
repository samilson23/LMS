from django import forms


class FeePaymentForm(forms.Form):
    amount = forms.IntegerField(label='Amount', required=True)
