# Generated by Django 4.2.4 on 2024-02-24 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Student', '0011_delete_viewedexamcards'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='fee_balance',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='students',
            name='total_billed',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='students',
            name='total_paid',
            field=models.FloatField(default=0.0),
        ),
    ]
