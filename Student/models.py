import os.path
from random import randint

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django_countries.fields import CountryField
from django_hashids import HashidsField
from phonenumber_field.modelfields import PhoneNumberField

from Faculty.models import Department, Course, Faculty, Year, Stage

User = get_user_model()

CHOICES = [
    ('MALE', 'MALE'),
    ('FEMALE', 'FEMALE'),
    ('Prefer not to say', 'Prefer not to say'),
    ('Other', 'Other'),
]


class Students(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    nationality = CountryField(blank=False)
    address = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(unique=True, blank=False)
    id_no = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(auto_now_add=False)
    gender = models.CharField(max_length=100, blank=True, choices=CHOICES)
    total_paid = models.FloatField(default=0.0)
    total_billed = models.FloatField(default=0.0)
    fee_balance = models.FloatField(default=0.0)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username


def directory_path(instance, filename):
    now = timezone.now().strftime("%Y-%m-%d at %H-%M-%S")
    stage = instance.stage.stage
    string = str(instance.user.username)
    username = string.replace('/', '')
    return 'Pdf/ExamCards/ExamCard-{0}/{1}/{2}'.format(username, stage, filename)


class ExamCards(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_card = models.FileField(upload_to=directory_path)
    exam_card_number = models.CharField(max_length=100, unique=True)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.exam_card != '':
            if os.path.isfile(self.exam_card.path):
                os.remove(self.exam_card.path)
        else:
            pass
        super(ExamCards, self).delete(*args, **kwargs)

    def __str__(self):
        return self.user.username + ' ' + self.stage.stage

    class Meta:
        verbose_name_plural = 'ExamCards'


def transcript_directory_path(instance, filename):
    now = timezone.now().strftime("%Y-%m-%d at %H-%M-%S")
    year = str(instance.year.year)
    string = str(instance.user.username)
    username = string.replace('/', '')
    return 'Pdf/ProvisionalTranscripts/Transcript-{0}/{1}/{2}'.format(username, year, filename)


class ProvisionalTranscripts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transcript = models.FileField(upload_to=transcript_directory_path)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        if self.transcript != '':
            if os.path.isfile(self.transcript.path):
                os.remove(self.transcript.path)
        else:
            pass
        super(ProvisionalTranscripts, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            this = ProvisionalTranscripts.objects.get(id=self.id)
            if this.transcript != self.transcript:
                this.transcript.delete()
        except:
            pass
        super(ProvisionalTranscripts, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username + ' ' + self.year.year

    class Meta:
        verbose_name_plural = 'Transcripts'


class FeeStatement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doc_no = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=100, blank=False)
    debit = models.FloatField(default=0.0)
    credit = models.FloatField(default=0.0)
    balance = models.FloatField(default=0.0)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.doc_no


class FeeStructure(models.Model):
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    tuition = models.FloatField(default=0.0, blank=False)
    student_activity = models.FloatField(default=0.0, blank=False)
    student_id_card = models.FloatField(default=0.0, blank=False)
    computer_fee = models.FloatField(default=0.0, blank=False)
    examination_fee = models.FloatField(default=0.0, blank=False)
    internet_connectivity = models.FloatField(default=0.0, blank=False)
    kuccps_placement_fee = models.FloatField(default=0.0, blank=False)
    library_fee = models.FloatField(default=0.0, blank=False)
    maintenance_fee = models.FloatField(default=0.0, blank=False)
    medical_fee = models.FloatField(default=0.0, blank=False)
    student_organization = models.FloatField(default=0.0, blank=False)
    quality_assurance_fee = models.FloatField(default=0.0, blank=False)
    registration_fee = models.FloatField(default=0.0, blank=False)
    amenity_fee = models.FloatField(default=0.0, blank=False)
    attachment = models.FloatField(default=0.0, blank=False)
    total = models.FloatField(default=0.0, blank=False)

    def __float__(self):
        return self.tuition
