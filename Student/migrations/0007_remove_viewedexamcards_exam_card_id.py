# Generated by Django 4.2.4 on 2023-09-30 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0006_viewedexamcards_exam_card_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='viewedexamcards',
            name='exam_card_id',
        ),
    ]