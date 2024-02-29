import os
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django_hashids import HashidsField

CHOICES = [
    ('ADMIN', 'ADMIN'),
    ('DEAN', 'DEAN'),
    ('HOD', 'HOD'),
    ('LECTURER', 'LECTURER'),
    ('STUDENT', 'STUDENT'),
    ('FINANCE', 'FINANCE'),
]


def directory_path(instance, filename):
    string = str(instance.username)
    username = string.replace('/', '')
    return 'Images/ProfilePictures/{0}/{1}'.format(username, filename)


class User(AbstractUser):
    hashid = HashidsField(real_field_name='id', min_length=5)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    middle_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to=directory_path, blank=True)
    usertype = models.CharField(max_length=100, choices=CHOICES, blank=True)
    has_profile = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def display_range(self):
        now = self.date_added
        seven_days = now + timedelta(days=7)
        return seven_days

    def delete(self, *args, **kwargs):
        if self.profile_pic != '':
            if os.path.isfile(self.profile_pic.path):
                os.remove(self.profile_pic.path)
        else:
            pass
        super(User, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            this = User.objects.get(id=self.id)
            if this.profile_pic != self.profile_pic:
                this.profile_pic.delete()
        except:
            pass
        super(User, self).save(*args, **kwargs)


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(blank=True, max_length=100)
    error = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
