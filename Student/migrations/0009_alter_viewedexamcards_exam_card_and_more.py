# Generated by Django 4.2.4 on 2023-10-01 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0008_remove_viewedexamcards_stage_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewedexamcards',
            name='exam_card',
            field=models.FileField(upload_to='Pdf/DownloadedPdfs/'),
        ),
        migrations.AlterField(
            model_name='viewprovisionaltranscript',
            name='transcript',
            field=models.FileField(upload_to='Pdf/DownloadedPdfs/'),
        ),
    ]