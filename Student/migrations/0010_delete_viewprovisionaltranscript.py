# Generated by Django 4.2.4 on 2023-10-01 22:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0009_alter_viewedexamcards_exam_card_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ViewProvisionalTranscript',
        ),
    ]
