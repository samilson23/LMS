import os

import uuid
from datetime import timedelta

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import math
from django.utils import timezone
from django_hashids import HashidsField

User = get_user_model()


# Create your models here.

class Faculty(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    name = models.CharField(max_length=100, blank=False, unique=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name


class Department(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    duration = models.IntegerField(default=4)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Stage(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    stage = models.CharField(max_length=100, blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.stage


class Deadlines(models.Model):
    sem_reg_deadline = models.DateTimeField(auto_now_add=False, blank=True)
    departments = models.ManyToManyField(Department)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Deadlines'


class Unit(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    unit_code = models.CharField(max_length=100, blank=False, unique=True)
    name = models.CharField(max_length=100, blank=False)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    global_unit = models.BooleanField(default=False)
    stage_name = models.CharField(blank=False, max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.unit_code


class UnitRegistration(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.student.username + ' ' + self.stage.stage


class RegistrationReport(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_id = models.ForeignKey(UnitRegistration, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    submitted = models.BooleanField(default=False)
    evaluated = models.BooleanField(default=False)
    resit = models.BooleanField(default=False)
    supplementary = models.BooleanField(default=False)

    def __bool__(self):
        return self.status

    def __str__(self):
        return self.student.username + ' ' + self.unit.stage.stage


class Year(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.CharField(max_length=10)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.student.username + '  ' + self.year


CHOICES = {
    ('ADMIN', 'ADMIN'),
    ('DEAN', 'DEAN'),
    ('HOD', 'HOD'),
    ('LECTURER', 'LECTURER'),
    ('STUDENT', 'STUDENT'),
    ('FINANCE', 'FINANCE'),
}


class NoticeBoard(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    written_by = models.ForeignKey(User, on_delete=models.CASCADE)
    addressed_to = models.CharField(max_length=100, choices=CHOICES, default='STUDENT')
    notice_title = models.CharField(max_length=100)
    notice = RichTextUploadingField(default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.notice_title

    def display_range(self):
        now = self.created_at
        seven_days = now + timedelta(days=7)
        return seven_days

    def expiry_date(self):
        now = self.created_at
        thirty_days = now + timedelta(days=30)
        return thirty_days

    def whenposted(self):
        now = timezone.now()
        diff = now - self.created_at
        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds
            if seconds == 1:
                return str(seconds) + " second ago"
            else:
                return str(seconds) + " seconds ago"
        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)
            if minutes == 1:
                return str(minutes) + " minute ago"
            else:
                return str(minutes) + " minutes ago"
        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)
            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
        if 1 <= diff.days < 30:
            days = diff.days
            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
        if 30 <= diff.days < 366:
            months = math.floor(diff.days / 30)
            if months == 1:
                return str(months) + " month ago"
            else:
                return str(months) + " months ago"
        if diff.days >= 366:
            years = math.floor(diff.days / 366)
            if years == 1:
                return str(years) + " year ago"
            else:
                return str(years) + " years ago"


class SemesterReg(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=100, unique=True)
    end_date = models.DateTimeField(auto_now_add=False)
    current = models.BooleanField(default=False)

    def __str__(self):
        return self.student.username + ' ' + self.stage.stage


class Results(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=10)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    grade_points = models.IntegerField(default=0)
    exam_mark = models.IntegerField(default=0, validators=
    [
        MinValueValidator(70),
        MaxValueValidator(0),
    ])
    cat_mark = models.IntegerField(default=0, validators=
    [
        MinValueValidator(30),
        MaxValueValidator(0),
    ])
    year = models.ForeignKey(Year, on_delete=models.CASCADE)
    admin_approved = models.BooleanField(default=False)
    dean_approved = models.BooleanField(default=False)
    hod_approved = models.BooleanField(default=False)
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.student.username + '   ' + self.unit.unit_code

    @property
    def total(self):
        return int(self.cat_mark) + int(self.exam_mark)

    @property
    def grade(self):
        if self.total == 0:
            return 'X'
        elif self.total < 40:
            return 'E'
        elif self.total < 50:
            return 'D'
        elif self.total < 60:
            return 'C'
        elif self.total < 70:
            return 'B'
        elif self.total < 100:
            return 'A'

    def save(self, *args, **kwargs):
        if 0 > int(self.exam_mark) or 70 < int(self.exam_mark):
            raise ValidationError('Exam score must range from 0 to 70')
        elif int(self.cat_mark) < 0 or int(self.cat_mark) > 30:
            raise ValidationError('Cat mark must range from 0 to 30')
        super(Results, self).save(*args, **kwargs)

    @property
    def grade_value(self):
        if self.grade == 'A':
            return 4
        elif self.grade == 'B':
            return 3
        elif self.grade == 'C':
            return 2
        elif self.grade == 'D':
            return 1
        elif self.grade == 'E' or self.grade == 'X':
            return 0

    class Meta:
        verbose_name_plural = 'Results'


choices = {
    ('Excellent', 'Excellent'),
    ('Good', 'Good'),
    ('Adequate', 'Adequate'),
    ('Poor', 'Poor'),
    ('Too Much', 'Too Much'),
}


class LecturerEvaluation(models.Model):
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    promotes_critical_thinking = models.CharField(max_length=100, blank=False, choices=choices)
    ties_in_primary_objectives_of_the_course = models.CharField(max_length=100, blank=False, choices=choices)
    explains_concepts_clearly = models.CharField(max_length=100, blank=False, choices=choices)
    uses_concrete_examples_of_concepts = models.CharField(max_length=100, blank=False, choices=choices)
    gives_multiple_examples = models.CharField(max_length=100, blank=False, choices=choices)
    points_out_practical_applications = models.CharField(max_length=100, blank=False, choices=choices)
    stresses_important_concepts = models.CharField(max_length=100, blank=False, choices=choices)
    repeats_difficult_ideas = models.CharField(max_length=100, blank=False, choices=choices)
    encourages_questions_and_comments = models.CharField(max_length=100, blank=False, choices=choices)
    answers_questions_clearly = models.CharField(max_length=100, blank=False, choices=choices)
    available_to_students_after_class = models.CharField(max_length=100, blank=False, choices=choices)
    asks_questions_of_class = models.CharField(max_length=100, blank=False, choices=choices)
    facilitates_discussions_during_lecture = models.CharField(max_length=100, blank=False, choices=choices)
    proceeds_at_good_pace_for_topic = models.CharField(max_length=100, blank=False, choices=choices)
    stays_on_theme_of_lecture = models.CharField(max_length=100, blank=False, choices=choices)
    states_lecture_objectives = models.CharField(max_length=100, blank=False, choices=choices)
    gives_preliminary_overview_of_lecture = models.CharField(max_length=100, blank=False, choices=choices)
    signals_transition_to_new_topic = models.CharField(max_length=100, blank=False, choices=choices)
    explains_how_each_topic_fits_in = models.CharField(max_length=100, blank=False, choices=choices)
    projects_confidence = models.CharField(max_length=100, blank=False, choices=choices)
    speaks_expressively_or_emphatically = models.CharField(max_length=100, blank=False, choices=choices)
    moves_about_while_lecturing = models.CharField(max_length=100, blank=False, choices=choices)
    gestures_while_speaking = models.CharField(max_length=100, blank=False, choices=choices)
    shows_facial_expression = models.CharField(max_length=100, blank=False, choices=choices)
    uses_humor = models.CharField(max_length=100, blank=False, choices=choices)


subjects = {
    ('Agriculture', 'Agriculture'),
    ('Building and Construction', 'Building and Construction'),
    ('Business Studies', 'Business Studies'),
    ('Biology', 'Biology'),
    ('Chemistry', 'Chemistry'),
    ('Computer Studies', 'Computer Studies'),
    ('Christian Religious Education', 'Christian Religious Education'),
    ('Drawing and Design', 'Drawing and Design'),
    ('English', 'English'),
    ('French', 'French'),
    ('Geography', 'Geography'),
    ('Kiswahili', 'Kiswahili'),
    ('Mathematics', 'Mathematics'),
    ('Physics', 'Physics'),
    ('Home Science', 'Home Science'),
}

grades = {
    ('A', 'A'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B', 'B'),
    ('B-', 'B-'),
    ('C+', 'C+'),
    ('C', 'C'),
    ('C-', 'C-'),
    ('D+', 'D+'),
    ('D', 'D'),
    ('D-', 'D-'),
    ('E', 'E'),
}


class KCSEResults(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, choices=subjects)
    grade = models.CharField(max_length=100, choices=grades)

    def __str__(self):
        return self.subject + ' ' + self.grade

    class Meta:
        verbose_name_plural = 'KCSE Results'


class ResultSlip(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    kcse_result_slip = models.FileField(upload_to='Pdf/KCSEResultSlips')

    def __str__(self):
        return self.student.username

    def delete(self, *args, **kwargs):
        if self.kcse_result_slip != '':
            if os.path.isfile(self.kcse_result_slip.path):
                os.remove(self.kcse_result_slip.path)
        else:
            pass
        super(ResultSlip, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        try:
            this = ResultSlip.objects.get(id=self.id)
            if this.ksce_result_slip != self.kcse_result_slip:
                this.ksce_result_slip.delete()
        except:
            pass
        super(ResultSlip, self).save(*args, **kwargs)

    @property
    def filename(self):
        return os.path.basename(self.kcse_result_slip.name)


class InterSchooltransfer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    new_programme = models.ForeignKey(Course, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50)
    kcse_results = models.ManyToManyField(KCSEResults)
    kcse_resultslip = models.ManyToManyField(ResultSlip)
    aggregate = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='pending')

    def __str__(self):
        return self.student.username


class UnitSelection(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=5)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    level_of_understanding = models.IntegerField(blank=False)
    approved = models.CharField(max_length=1, default='1')

    @property
    def level_of_understanding_percentage(self):
        return f'{self.level_of_understanding}%'

    def __int__(self):
        return self.level_of_understanding

    def __str__(self):
        return self.instructor.username + ' ' + self.unit.unit_code


class LeaveRequests(models.Model):
    hashid = HashidsField(real_field_name='id', min_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    start_date = models.DateTimeField(auto_now=False)
    end_date = models.DateTimeField(auto_now=False)
    duration = models.IntegerField()
    reason = models.TextField()
    reliever = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reliever')
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Leave Requests'


class Events(models.Model):
    title = models.CharField(max_length=300)
    description = RichTextUploadingField()
    addressed_to = models.CharField(choices=CHOICES, max_length=100, default='STUDENT')
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()

    def __str__(self):
        return self.title
