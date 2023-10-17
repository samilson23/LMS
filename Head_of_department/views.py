from datetime import date

from datatableview.views import DatatableView
from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, UpdateView

from Faculty.models import *
from Head_of_department.forms.CreateProfile import CreateHODProfile, HODProfilePicture, HODDetails
from Head_of_department.models import HOD
from Lecturer.models import Lecturers
from Student.models import Students

User = get_user_model()


class Dashboard(LoginRequiredMixin, TemplateView):
    permission_denied_message = 'Permission denied'

    def get(self, request, *args, **kwargs):
        queryset = HOD.objects.get(user=request.user.id)
        user = User.objects.get(id=request.user.id)
        user_form = HODDetails(request.POST or None, instance=user)
        form = CreateHODProfile(request.POST or None, instance=queryset)
        dept_id = Department.objects.get(id=queryset.department.id)
        students = Students.objects.filter(department=dept_id).count()
        courses = Course.objects.filter(department=dept_id).count()
        units = Unit.objects.filter(department=dept_id).count()
        return render(request, 'Dashboard/HODDashboard.html',
                      {'queryset': queryset, 'profile_form': form, 'user_form': user_form,
                       'students': students, 'courses': courses, 'units': units,
                       'lecs': Lecturers.objects.filter(department=dept_id).count(),
                       'leave_count': LeaveRequests.objects.filter(user=user, status='approved').count(),
                       })


class CreateProfile(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = CreateHODProfile
        profile_form = HODProfilePicture
        queryset = Department.objects.all()
        return render(request, 'HODProfile/CreateProfile.html',
                      {'form': form, 'profile_form': profile_form, 'queryset': queryset})


class SaveProfile(LoginRequiredMixin, CreateView):

    def post(self, request, *args, **kwargs):
        form = CreateHODProfile(request.POST)
        profile_form = HODProfilePicture(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            id_no = form.cleaned_data['id_no']
            nationality = form.cleaned_data['nationality']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            dept = request.POST.get('dept')
            dept_id = Department.objects.get(id=dept)
            HOD.objects.create(user=user, phone_number=phone_number, id_no=id_no, nationality=nationality,
                               address=address, gender=gender, department=dept_id
                               )
        if profile_form.is_valid():
            profile_pic = profile_form.cleaned_data['profile_pic']
            user.profile_pic = profile_pic
            user.has_profile = True
            user.save()
        messages.success(request, 'Profile Created')
        messages.info(request, 'You can now access your account')
        return redirect('HODDashboard')


class UpdateProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        queryset = HOD.objects.get(user=request.user.id)
        queryset2 = User.objects.get(id=request.user.id)
        form = CreateHODProfile(request.POST or None, instance=queryset)
        user_form = HODDetails(request.POST, request.FILES, instance=queryset2)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Profile Updated')
        else:
            messages.error(request, 'Invalid input, Please ensure all fields are filled correctly')
        return redirect('HODDashboard')


class ListUnits(LoginRequiredMixin, ListView):
    template_name = 'HODFacultyManagement/ListUnits.html'

    def get_queryset(self):
        user_id = HOD.objects.get(user=self.request.user.id)
        return Unit.objects.filter(department=user_id.department.id)


class ResultsManagement(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        unit = Unit.objects.get(hashid=pk)
        try:
            results = Results.objects.filter(unit=unit.id)
        except Results.DoesNotExist:
            results = None
        context = {
            'unit': unit,
            'results': results,
        }
        return render(request, 'ResultsMgmt/result_mgmt.html', context)


class ApproveDisapproveResults(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        result = Results.objects.get(hashid=pk)
        if result.hod_approved:
            result.hod_approved = False
            messages.info(request, 'Result Disapproved')
        else:
            result.hod_approved = True
            messages.success(request, 'Result Approved')
        result.save()
        return HttpResponseRedirect(reverse('HODResultsManagement', kwargs={'pk': result.unit.hashid}))


class Appraisal(LoginRequiredMixin, TemplateView):
    template_name = 'Extras/HOD_Appraisal.html'


class Leaves(LoginRequiredMixin, ListView):
    template_name = 'Extras/hod_leaves.html'

    def get_queryset(self):
        return LeaveRequests.objects.filter(user__id=self.request.user.id)


class RequestLeave(LoginRequiredMixin, ListView):
    template_name = 'Extras/hod_leave_request.html'

    def get_queryset(self):
        return User.objects.filter(usertype='DEAN')
