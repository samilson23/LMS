from django.contrib import admin

# Register your models here.
from Student.models import *

admin.site.register(Students)
admin.site.register(ExamCards)
admin.site.register(ProvisionalTranscripts)
