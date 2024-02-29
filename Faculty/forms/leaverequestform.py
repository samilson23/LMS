import datetime

from django import forms

from Faculty.models import *


class LeaveApplicationForm(forms.ModelForm):
    start_date = forms.DateField(initial=datetime.date.today)

    class Meta:
        model = LeaveRequests
        fields = [
            'start_date', 'end_date', 'reason', 'duration'
        ]
