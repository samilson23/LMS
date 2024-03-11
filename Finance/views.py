from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, ListView
from django.views.generic.base import View

from Finance.forms.CreateFeeStructureForm import CreateFeeStructureForm
from Finance.models import *
from Finance.forms.CreateProfile import *
from Faculty.models import *
from Pesapal import pesapal_ops3
from Pesapal.models import STDTransaction
from Student.models import FeeStructure, Students, FeeStatement


class Dashboard(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        queryset = Finance.objects.get(user=request.user.id)
        context = {
            'queryset': queryset,
            'user_form': FinanceDetails(request.POST or None, instance=request.user),
            'profile_form': CreateFinanceProfile(request.POST or None, instance=queryset)
        }
        return render(request, 'Dashboard/FinanceDashboard.html', context)


class CreateProfile(LoginRequiredMixin, FormView):
    form_class = CreateFinanceProfile
    template_name = 'FinanceCreateProfile/CreateProfile.html'


class SaveProfile(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = CreateFinanceProfile(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            id_no = form.cleaned_data['id_no']
            nationality = form.cleaned_data['nationality']
            gender = form.cleaned_data['gender']
            phone_number = form.cleaned_data['phone_number']
            user = User.objects.get(id=request.user.id)
            Finance.objects.create(user=user, nationality=nationality, gender=gender,
                                   phone_number=phone_number, address=address, id_no=id_no)
            user.has_profile = True
            user.save()
            messages.success(request, 'Profile Created')
            messages.info(request, 'You can now access your account')
            return redirect('FinanceDashboard')
        else:
            messages.error(request, 'Failed to create profile')
            return redirect('FinanceCreateProfile')


class UpdateProfile(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        queryset = Finance.objects.get(user=request.user.id)
        queryset2 = User.objects.get(id=request.user.id)
        form = CreateFinanceProfile(request.POST or None, instance=queryset)
        user_form = FinanceDetails(request.POST, request.FILES, instance=queryset2)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Profile Updated')
        else:
            messages.error(request, 'Please check that all fields are filled correctly')
        return redirect('FinanceDashboard')


class Departments(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'Finance/List_depts.html'


class CreateFeeStructure(LoginRequiredMixin, View):
    @staticmethod
    def get(request, department):
        dept = Department.objects.get(hashid=department)
        stage = Stage.objects.filter(department=dept.id)
        context = {
            'dept': dept,
            'stages': stage,
            'form': CreateFeeStructureForm(request.POST or None)
        }
        return render(request, 'Finance/CreateFeeStructure.html', context)


class SubmitFeeStructure(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        stage = request.POST.get('stage')
        dept = request.POST.get('dept')
        dept_id = Department.objects.get(hashid=dept)
        stage_id = Stage.objects.get(stage=stage, department=dept_id.id)
        stages = Stage.objects.filter(department=dept_id.id)
        form = CreateFeeStructureForm(request.POST or None)
        try:
            feestructure = FeeStructure.objects.get(id=stage_id.id)
            update_form = CreateFeeStructureForm(request.POST or None, instance=feestructure)
            if update_form.is_valid():
                update_form.save()
                messages.success(request, 'FeeStructure Updated')
        except FeeStructure.DoesNotExist:
            if form.is_valid():
                FeeStructure.objects.create(
                    tuition=form.cleaned_data['tuition'],
                    student_activity=form.cleaned_data['student_activity'],
                    student_id_card=form.cleaned_data['student_id_card'],
                    computer_fee=form.cleaned_data['computer_fee'],
                    examination_fee=form.cleaned_data['examination_fee'],
                    internet_connectivity=form.cleaned_data['internet_connectivity'],
                    kuccps_placement_fee=form.cleaned_data['kuccps_placement_fee'],
                    library_fee=form.cleaned_data['library_fee'],
                    maintenance_fee=form.cleaned_data['maintenance_fee'],
                    medical_fee=form.cleaned_data['medical_fee'],
                    student_organization=form.cleaned_data['student_organization'],
                    quality_assurance_fee=form.cleaned_data['quality_assurance_fee'],
                    registration_fee=form.cleaned_data['registration_fee'],
                    amenity_fee=form.cleaned_data['amenity_fee'],
                    attachment=form.cleaned_data['attachment'],
                    stage=stage_id
                )
                messages.success(request, 'FeeStructure Created')
            else:
                messages.error(request, 'Failed')
        context = {
            'form': form,
            'dept': dept_id,
            'stages': stages,
        }
        return render(request, 'Finance/CreateFeeStructure.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class FetchData(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        stage = request.GET.get('stage')
        dept = request.GET.get('dept')
        try:
            dept_id = Department.objects.get(hashid=dept)
            stage_id = Stage.objects.get(stage=stage, department=dept_id)
            fee_structure = FeeStructure.objects.get(stage__id=stage_id.id)

            data = {
                'tuition': fee_structure.tuition,
                'student_activity': fee_structure.student_activity,
                'student_id_card': fee_structure.student_id_card,
                'computer_fee': fee_structure.computer_fee,
                'examination_fee': fee_structure.examination_fee,
                'internet_connectivity': fee_structure.internet_connectivity,
                'kuccps_placement_fee': fee_structure.kuccps_placement_fee,
                'library_fee': fee_structure.library_fee,
                'maintenance_fee': fee_structure.maintenance_fee,
                'medical_fee': fee_structure.medical_fee,
                'student_organization': fee_structure.student_organization,
                'quality_assurance_fee': fee_structure.quality_assurance_fee,
                'registration_fee': fee_structure.registration_fee,
                'amenity_fee': fee_structure.amenity_fee,
                'attachment': fee_structure.attachment,
            }
        except FeeStructure.DoesNotExist:
            data = {
                'tuition': 0.0,
                'student_activity': 0.0,
                'student_id_card': 0.0,
                'computer_fee': 0.0,
                'examination_fee': 0.0,
                'internet_connectivity': 0.0,
                'kuccps_placement_fee': 0.0,
                'library_fee': 0.0,
                'maintenance_fee': 0.0,
                'medical_fee': 0.0,
                'student_organization': 0.0,
                'quality_assurance_fee': 0.0,
                'registration_fee': 0.0,
                'amenity_fee': 0.0,
                'attachment': 0.0,
            }
        return JsonResponse(data)


class ListFeeStructures(LoginRequiredMixin, ListView):
    template_name = 'Finance/ListFeeStructures.html'
    model = FeeStructure


class ListStudents(LoginRequiredMixin, ListView):
    model = Students
    template_name = 'Finance/ListStudents.html'


class StudentStatement(LoginRequiredMixin, ListView):
    template_name = 'Finance/FeeStatements.html'

    def get_queryset(self):
        return FeeStatement.objects.filter(user__hashid=self.kwargs['student'])


class StudentReceipts(LoginRequiredMixin, ListView):
    template_name = 'Finance/Receipts.html'

    def get_queryset(self):
        return STDTransaction.objects.filter(paid_by__hashid=self.kwargs['student'])


class Receipts(LoginRequiredMixin, ListView):
    template_name = 'Finance/AllReceipts.html'

    def get_queryset(self):
        return STDTransaction.objects.all()


@method_decorator(csrf_exempt, name='dispatch')
class PaymentDetails(LoginRequiredMixin, View):
    @staticmethod
    def get(request, reference):
        trans = STDTransaction.objects.get(reference=reference)
        param = trans.reference
        payment_status = pesapal_ops3.get_payment_status_by_mercharnt_ref(param).decode('utf-8')
        print(payment_status)
        status = str(payment_status).split('=')
        if len(status) >= 2:
            p_status = str(payment_status).split('=')[1]
            if p_status == 'COMPLETED':
                transaction_tracking_id = request.GET.get('pesapal_transaction_tracking_id')
                print(transaction_tracking_id)
                detailed_data = pesapal_ops3.get_detailed_order_status(param, transaction_tracking_id).decode(
                    'utf-8')
                payment_method = str(detailed_data).split(',')[1]
                user = User.objects.get(id=trans.paid_by.id)
                description = f'{trans.timestamp} Fee Collection {trans.reference}'
                trans.description = description
                trans.status = 'COMPLETED'
                trans.payment_method = payment_method
                trans.mercharnt_reference = transaction_tracking_id
                trans.save()
                student = Students.objects.get(user=user)
                student.total_paid += float(trans.amount)
                student.fee_balance -= float(trans.amount)
                student.save()
                FeeStatement.objects.create(user=user, doc_no=trans.reference, description=description,
                                            credit=trans.amount,
                                            balance=student.fee_balance)
            return render(request, 'Finance/status.html', {'status': payment_status})
        else:
            messages.error(request, 'Transaction Does not exist')
            return render(request, 'Finance/Receipts.html', {'student': trans.paid_by.hashid})

