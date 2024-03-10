from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.

class STDTransaction(models.Model):
    PESAPAL_STATUS_CHOICES = (
        ('PENDING', 'PENDING'),
        ('COMPLETED', 'COMPLETED'),
        ('FAILED', 'FAILED'),
        ('INVALID', 'INVALID'),
    )
    amount = models.FloatField()
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100)
    mercharnt_reference = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    status = models.CharField(choices=PESAPAL_STATUS_CHOICES, max_length=100)
    payment_method = models.CharField(max_length=24)
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = (("mercharnt_reference", "reference"),)
