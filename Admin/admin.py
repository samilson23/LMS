from django.contrib import admin
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry

from Admin.models import Admin

admin.site.register(Admin)
admin.site.register(Session)
admin.site.register(LogEntry)
