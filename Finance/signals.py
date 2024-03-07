from django.db.models.signals import pre_save
from django.dispatch import receiver

from Student.models import FeeStructure


@receiver(pre_save, sender=FeeStructure)
def sum_total(sender, instance, **kwargs):
    total_sum = float(instance.tuition + instance.student_activity +
                      instance.student_id_card + instance.computer_fee +
                      instance.examination_fee + instance.internet_connectivity +
                      instance.kuccps_placement_fee + instance.library_fee +
                      instance.maintenance_fee + instance.medical_fee +
                      instance.student_organization + instance.quality_assurance_fee +
                      instance.registration_fee + instance.amenity_fee +
                      instance.attachment)
    instance.total = total_sum
