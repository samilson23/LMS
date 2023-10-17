# Generated by Django 4.2.4 on 2023-09-29 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Faculty', '0004_alter_kcseresults_grade_alter_kcseresults_subject_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UnitSelection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_of_understanding', models.IntegerField()),
                ('approved', models.CharField(default='1', max_length=1)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Faculty.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Lecturers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('address', models.CharField(blank=True, max_length=100)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('id_no', models.CharField(blank=True, max_length=100)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('Prefer not to say', 'Prefer not to say'), ('Other', 'Other')], max_length=100)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Faculty.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Faculty.faculty')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Lecturers',
            },
        ),
    ]
