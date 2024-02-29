import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django_countries.fields import CountryField
from django_hashids import HashidsField
from phonenumber_field.modelfields import PhoneNumberField

from Faculty.models import Department, Course, Faculty, Unit

User = get_user_model()

CHOICES = [
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('Prefer not to say', 'Prefer not to say'),
    ('Other', 'Other'),
]


class Lecturers(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    nationality = CountryField(blank=False)
    address = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(unique=True, blank=False)
    id_no = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True, choices=CHOICES)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Lecturers'

    def __str__(self):
        return self.user.username
