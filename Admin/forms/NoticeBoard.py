from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from Faculty.models import NoticeBoard


class NoticeBoardForm(forms.ModelForm):
    notice = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = NoticeBoard
        fields = ['addressed_to', 'notice_title', 'notice']
        widgets = {'addressed_to': forms.Select(attrs={'class': 'form-control'}),
                   'notice_title': forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'e.g Inviting all students to a graduation ceremony'}),
                   }
