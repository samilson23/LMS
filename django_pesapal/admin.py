from django.contrib import admin

# Register your models here.
from django_pesapal.models import Transaction

admin.site.register(Transaction)
