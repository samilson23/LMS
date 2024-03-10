from random import randint

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from Faculty.models import Department, Faculty, Course, LecturerEvaluation, SemesterReg
from Student.models import Students, ExamCards
User = get_user_model()


@receiver(pre_save, sender=Students)
def create_profile(sender, instance, **kwargs):
    course_id = Course.objects.get(id=instance.course.id)
    dept_id = Department.objects.get(id=course_id.department.id)
    faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
    instance.department = dept_id
    instance.faculty = faculty_id


@receiver(pre_save, sender=SemesterReg)
def generate_exam_card_number(sender, instance, **kwargs):
    if not instance.card_number:
        is_unique = True
        while is_unique:
            exam_card_number = instance.card_number
            is_unique = SemesterReg.objects.filter(card_number=exam_card_number).exists()
        instance.exam_card_number = exam_card_number