# Generated by Django 4.2.4 on 2023-09-30 18:43

import Student.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Faculty', '0007_alter_kcseresults_grade_alter_kcseresults_subject_and_more'),
        ('Student', '0003_alter_viewprovisionaltranscript_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewedexamcards',
            name='stage',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Faculty.stage'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='viewedexamcards',
            name='exam_card',
            field=models.FileField(upload_to='Pdf/'),
        ),
    ]