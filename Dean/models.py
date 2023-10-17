import uuid

from django.db import models

from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from django_hashids import HashidsField
from phonenumber_field.modelfields import PhoneNumberField

from Faculty.models import Faculty

User = get_user_model()

CHOICES = [
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('Prefer not to say', 'Prefer not to say'),
    ('Other', 'Other'),
]


class Dean(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    faculty = models.OneToOneField(Faculty, on_delete=models.CASCADE)
    nationality = CountryField(blank=True)
    address = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(unique=True, blank=True)
    id_no = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True, choices=CHOICES)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.username

