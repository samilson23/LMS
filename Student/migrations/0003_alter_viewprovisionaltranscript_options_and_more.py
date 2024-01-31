# Generated by Django 4.2.4 on 2023-09-30 18:41

import Student.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0002_viewprovisionaltranscript'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='viewprovisionaltranscript',
            options={'verbose_name_plural': 'Viewed Transcripts'},
        ),
        migrations.AlterField(
            model_name='viewprovisionaltranscript',
            name='transcript',
            field=models.FileField(upload_to='Pdf/'),
        ),
        migrations.CreateModel(
            name='ViewedExamCards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('view_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Student.examcards')),
            ],
            options={
                'verbose_name_plural': 'Viewed ExamCards',
            },
        ),
    ]