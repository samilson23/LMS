from random import randint

from django.db.models.signals import pre_save
from django.dispatch import receiver

from Faculty.models import Department, Faculty, Course, LecturerEvaluation
from Student.models import Students, ExamCards
from Student.views import ExamCard


@receiver(pre_save, sender=Students)
def create_profile(sender, instance, **kwargs):
    course_id = Course.objects.get(id=instance.course.id)
    dept_id = Department.objects.get(id=course_id.department.id)
    faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
    instance.department = dept_id
    instance.faculty = faculty_id


@receiver(pre_save, sender=ExamCards)
def generate_exam_card_number(sender, instance, **kwargs):
    if not instance.exam_card_number:
        is_unique = True
        while is_unique:
            exam_card_number = instance.exam_card_number
            is_unique = ExamCards.objects.filter(exam_card_number=exam_card_number).exists()
        instance.exam_card_number = exam_card_number
