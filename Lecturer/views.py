from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, FormView

from Faculty.forms.leaverequestform import LeaveApplicationForm
from Faculty.models import *
from Lecturer.forms.CreateProfile import LECProfilePicture, CreateLECProfile, LECDetails
from Lecturer.models import Lecturers

User = get_user_model()


class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        my_units = UnitSelection.objects.filter(instructor=request.user.id, approved='2')
        unique_students = set()
        students = 0
        for unit in my_units:
            student_ids = RegistrationReport.objects.filter(unit=unit.unit.id).values_list('student', flat=True).distinct()
            unique_students.update(student_ids)
            unique_student_count = len(unique_students)
            students += unique_student_count
        queryset = Lecturers.objects.get(user=request.user.id)
        user = User.objects.get(id=request.user.id)
        user_form = LECDetails(request.POST or None, instance=user)
        form = CreateLECProfile(request.POST or None, instance=queryset)
        return render(request, 'Dashboard/LECDashboard.html',
                      {'queryset': queryset, 'profile_form': form, 'user_form': user_form,
                       'my_units': my_units.count(), 'students': students,
                       'leave_count': LeaveRequests.objects.filter(user=request.user.id, status='approved').count()
                       })


class UpdateProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        queryset = Lecturers.objects.get(user=request.user.id)
        queryset2 = User.objects.get(id=request.user.id)
        form = CreateLECProfile(request.POST or None, instance=queryset)
        user_form = LECDetails(request.POST, request.FILES, instance=queryset2)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Profile Updated')
        else:
            messages.error(request, 'Invalid input, Please ensure all fields are filled correctly')
        return redirect('LECDashboard')


class CreateProfile(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = CreateLECProfile
        profile_form = LECProfilePicture
        queryset = Department.objects.all()
        return render(request, 'LECProfile/CreateProfile.html',
                      {'form': form, 'profile_form': profile_form, 'queryset': queryset})


class SaveProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = CreateLECProfile(request.POST)
        profile_form = LECProfilePicture(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            id_no = form.cleaned_data['id_no']
            nationality = form.cleaned_data['nationality']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            dept = request.POST.get('dept')
            dept_id = Department.objects.get(id=dept)
            print(dept_id)
            faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
            print(faculty_id)
            Lecturers.objects.create(user=user, phone_number=phone_number, id_no=id_no, nationality=nationality,
                                     address=address, gender=gender, department=dept_id, faculty=faculty_id
                                     )
        if profile_form.is_valid():
            profile_pic = profile_form.cleaned_data['profile_pic']
            user.profile_pic = profile_pic
            user.has_profile = True
            user.save()
        messages.success(request, 'Profile Created')
        messages.info(request, 'You can now access your account')
        return redirect('LECDashboard')


class Units(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return UnitSelection.objects.filter(instructor=self.request.user.id)

    def get_template_names(self):
        return 'lec_unit_application/MyUnits.html'


class UnitApplication(LoginRequiredMixin, ListView):
    permission_required = 'Faculty.add_unitselection'
    permission_denied_message = 'Unit Application is closed at the moment'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.info(request, self.permission_denied_message)
            return redirect('LECUnits')
        else:
            queryset = Unit.objects.all()
            return render(request, 'lec_unit_application/unit_application.html', {'object_list': queryset})


class SubmitApplication(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    def post(self, request, *args, **kwargs):
        unit = request.POST.get('unit')
        level_of_understanding = request.POST.get('lou')
        print(level_of_understanding)
        unit_id = Unit.objects.get(id=unit)
        user_id = User.objects.get(id=request.user.id)
        try:
            UnitSelection.objects.get(unit=unit_id, approved=2)
            messages.info(request, 'This unit already has an instructor assigned to it')
        except UnitSelection.DoesNotExist:
            try:
                UnitSelection.objects.get(instructor=user_id, approved=1, unit=unit_id)
                messages.warning(request, 'You have already submitted an application for this unit')
            except UnitSelection.DoesNotExist:
                UnitSelection.objects.create(instructor=user_id, level_of_understanding=level_of_understanding,
                                             unit=unit_id)
                messages.success(request, 'Application submitted')

        return redirect('LECUnitApplication')


class UploadResults(LoginRequiredMixin, View):
    permission_required = 'Faculty.add_results'
    permission_denied_message = 'Uploading of results has been disabled for now'

    def get(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.info(request, self.permission_denied_message)
            return redirect('LECUnits')
        else:
            queryset = UnitSelection.objects.get(hashid=pk)
            students = Results.objects.filter(unit=queryset.unit.id, current=True)
            context = {
                'queryset': queryset,
                'students': students,
                'check': students.exists(),
            }
            return render(request, 'Resultsmgt/upload_results.html', context)


class Appraisal(LoginRequiredMixin, TemplateView):
    template_name = 'Extras/Appraisal.html'


class Leaves(LoginRequiredMixin, ListView):
    template_name = 'Extras/lec_leaves.html'

    def get_queryset(self):
        return LeaveRequests.objects.filter(user__id=self.request.user.id)


class RequestLeave(LoginRequiredMixin, ListView):
    template_name = 'Extras/leave_request.html'

    def get_queryset(self):
        return User.objects.filter(usertype='DEAN')


