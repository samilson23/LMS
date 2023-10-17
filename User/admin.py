from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from User.models import User

admin.site.register(User)
admin.site.register(Permission)
admin.site.register(ContentType)
