# Generated by Django 4.2.4 on 2024-03-15 18:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Finance', '0003_paymentdetails_payment_no'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PaymentDetails',
        ),
    ]