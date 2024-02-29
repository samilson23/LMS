from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


@receiver(post_save, sender=User)
def assign_user_group(sender, created, instance, **kwargs):
    content_type = ContentType.objects.get(app_label='User', model='user')
    if instance.usertype == 'DEAN':
        try:
            permission = Permission.objects.get(codename='login')
            Dean_group = Group.objects.get(name='Dean_group')
            Dean_group.user_set.add(instance)
            Dean_group.permissions.add(permission)
        except Group.DoesNotExist:
            Dean_group = Group.objects.create(name='Dean_group')
            Dean_group.user_set.add(instance)
        except Permission.DoesNotExist:
            permission = Permission.objects.create(codename='login', name='Can login', content_type=content_type)
            Dean_group = Group.objects.get(name='Dean_group')
            Dean_group.permissions.add(permission)
    elif instance.usertype == 'HOD':
        try:
            permission = Permission.objects.get(codename='login')
            Hod_group = Group.objects.get(name='Hod_group')
            Hod_group.user_set.add(instance)
            Hod_group.permissions.add(permission)
        except Group.DoesNotExist:
            Hod_group = Group.objects.create(name='Hod_group')
            Hod_group.user_set.add(instance)
        except Permission.DoesNotExist:
            permission = Permission.objects.create(codename='login', name='Can login', content_type=content_type)
            Hod_group = Group.objects.get(name='Hod_group')
            Hod_group.permissions.add(permission)
    elif instance.usertype == 'LECTURER':
        try:
            permission = Permission.objects.get(codename='login')
            Lec_group = Group.objects.get(name='Lecturer_group')
            Lec_group.user_set.add(instance)
            Lec_group.permissions.add(permission)
        except Group.DoesNotExist:
            Lec_group = Group.objects.create(name='Lecturer_group')
            Lec_group.user_set.add(instance)
        except Permission.DoesNotExist:
            permission = Permission.objects.create(codename='login', name='Can login', content_type=content_type)
            Lec_group = Group.objects.get(name='Lecturer_group')
            Lec_group.permissions.add(permission)
    elif instance.usertype == 'STUDENT':
        try:
            permission = Permission.objects.get(codename='login')
            student_group = Group.objects.get(name='Student_group')
            student_group.user_set.add(instance)
            student_group.permissions.add(permission)
        except Group.DoesNotExist:
            student_group = Group.objects.create(name='Student_group')
            student_group.user_set.add(instance)
        except Permission.DoesNotExist:
            permission = Permission.objects.create(codename='login', name='Can login', content_type=content_type)
            student_group = Group.objects.create(name='Student_group')
            student_group.permissions.add(permission)
