from django import forms

from Student.models import FeeStructure


class CreateFeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = [
            'tuition', 'student_activity', 'student_id_card', 'computer_fee',
            'examination_fee', 'internet_connectivity', 'kuccps_placement_fee',
            'library_fee', 'maintenance_fee', 'medical_fee', 'student_organization',
            'quality_assurance_fee', 'registration_fee', 'amenity_fee', 'attachment'
        ]
