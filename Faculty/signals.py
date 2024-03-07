from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from Faculty.models import Course, Department, Faculty, Unit, Results, Stage


@receiver(pre_save, sender=Course)
def assign_faculty(sender, instance, **kwargs):
    dept_id = Department.objects.get(id=instance.department.id)
    faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
    instance.faculty = faculty_id


@receiver(pre_save, sender=Unit)
def create_unit(sender, instance, **kwargs):
    course_id = Course.objects.get(id=instance.course.id)
    dept_id = Department.objects.get(id=course_id.department.id)
    instance.department = dept_id


@receiver(pre_save, sender=Results)
def grade_point(sender, instance, **kwargs):
    if instance.grade == 'A':
        instance.grade_points = 4
    elif instance.grade == 'B':
        instance.grade_points = 3
    elif instance.grade == 'C':
        instance.grade_points = 2
    elif instance.grade == 'D':
        instance.grade_points = 1
    elif instance.grade == 'E' or instance.grade == 'X':
        instance.grade_points = 0


@receiver(pre_save, sender=Stage)
def create_year(sender, instance, **kwargs):
    parts = instance.stage.split()
    for i in range(len(parts) - 1):
        if parts[i] == "Year" and parts[i + 1].isdigit():
            year = f"{parts[i]} {parts[i + 1]}"
            instance.year = year
