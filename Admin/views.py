
import json
from datetime import timedelta

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.core.cache import cache
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, UpdateView

from Admin.forms.CreateProfile import CreateAdminProfile, AdminDetails
from Admin.forms.CreateUserAccountForm import CreateUserAccount
from Admin.forms.DeanProfile import DeanProfile
from Admin.forms.EditUserAccount import EditUserAccounts
from Admin.forms.NoticeBoard import NoticeBoardForm
from Admin.forms.ResetPassword import ChangePassword
from Admin.models import Admin
from Dean.models import Dean
from Faculty.forms.createfaculty import CreateFaculties
from Faculty.forms.createunit import CreateUnits
from Faculty.models import Faculty, Department, Course, Stage, Unit, NoticeBoard, Deadlines, Year, Results, SemesterReg, \
    RegistrationReport
from Student.models import Students
from User.models import UserActivity

User = get_user_model()


class Dashboard(LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        queryset = Admin.objects.get(user=request.user.id)
        user = User.objects.get(pk=request.user.id)
        user_form = AdminDetails(request.POST or None, instance=user)
        form = CreateAdminProfile(request.POST or None, instance=queryset)
        users = User.objects.all()
        now = timezone.now()
        notices = NoticeBoard.objects.filter(addressed_to='ADMIN').order_by('-id')
        active_user_count = cache.get('active_users', 0)
        try:
            deadline = Deadlines.objects.get(active=True)
            dept = deadline.departments.all()
            departments = Department.objects.exclude(id__in=dept)
        except Deadlines.DoesNotExist:
            departments = Department.objects.all()
            dept = None
        context = {'queryset': queryset, 'profile_form': form, 'user_form': user_form, 'count': users.count(),
                   'faculty_count': Faculty.objects.all().count(), 'dept_count': Department.objects.all().count(), 'now': now,
                   'users': users,'notices': notices, "departments": departments, 'depts': dept,
                  'active_users': active_user_count
        }
        return render(request, 'Dashboard/AdminDashboard.html', context)


class CreateProfile(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = CreateAdminProfile
        return render(request, 'Profile/CreateProfile.html', {'form': form})


class SaveProfile(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = CreateAdminProfile(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            id_no = form.cleaned_data['id_no']
            nationality = form.cleaned_data['nationality']
            gender = form.cleaned_data['gender']
            phone_number = form.cleaned_data['phone_number']
            user = User.objects.get(id=request.user.id)
            Admin.objects.create(user=user, nationality=nationality, gender=gender,
                                 phone_number=phone_number, address=address, id_no=id_no)
            user.has_profile = True
            user.save()
            messages.success(request, 'Profile Created')
            messages.info(request, 'You can now access your account')
            return redirect('AdminDashboard')
        else:
            messages.error(request, 'Failed to create profile')
            return redirect('AdminCreateProfile')


class UpdateProfile(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        queryset = Admin.objects.get(user=request.user.id)
        queryset2 = User.objects.get(id=request.user.id)
        form = CreateAdminProfile(request.POST or None, instance=queryset)
        user_form = AdminDetails(request.POST, request.FILES, instance=queryset2)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, 'Profile Updated')
        else:
            messages.error(request, 'Please check that all fields are filled correctly')
        return redirect('AdminDashboard')


class UserManagement(LoginRequiredMixin, ListView):
    template_name = 'AdminUserManagement/usermanagement.html'

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        elif self.request.user.usertype == 'ADMIN':
            return User.objects.filter(usertype__in=['STUDENT', 'DEAN', 'HOD', 'LECTURER', 'FINANCE'])


class CreateUser(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = CreateUserAccount
        return render(request, 'AdminUserManagement/createuseraccount.html', {'form': form})


class SaveUserAccount(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        form = CreateUserAccount(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            usertype = form.cleaned_data['usertype']
            user = User(username=username, usertype=usertype)
            user.set_password(username)
            user.save()
            messages.success(request, 'User Account Created')
        else:
            messages.error(request, 'Failed to create User Account')
        return redirect('AdminCreateUserAccount')


class DeleteUserAccount(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        user = User.objects.get(hashid=pk)
        return render(request, 'AdminUserManagement/deleteuser.html', {'user': user})


class ConfirmDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'User Account Deleted'
    success_url = reverse_lazy('AdminUserManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_valid(form)


class ActivateDeactivate(LoginRequiredMixin, View):

    @staticmethod
    def get(request, pk):
        acc = User.objects.get(hashid=pk)

        if not acc.is_active:
            acc.is_active = True
            messages.success(request, "User account has been activated")
        elif acc.is_active:
            acc.is_active = False
            messages.error(request, "User account has been Deactivated")
        acc.save()

        return redirect('AdminUserManagement')


class EditUserAccount(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        queryset = User.objects.get(hashid=pk)
        form = EditUserAccounts(request.POST or None, instance=queryset)
        return render(request, 'AdminUserManagement/userprofile.html', {'form': form, 'queryset': queryset})


class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'middle_name', 'last_name', 'email', 'profile_pic', 'usertype']
    success_url = reverse_lazy('AdminUserManagement')

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Profile Updated')
        user = User.objects.get(id=self.kwargs['pk'])
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR,
                             'Invalid Input, Please check that all fields are filled correctly')
        user_id = User.objects.get(id=self.kwargs['pk'])
        return HttpResponseRedirect(reverse('AdminUserProfile', kwargs={'pk': user_id.hashid}))


class FacultyManagement(LoginRequiredMixin, ListView):
    model = Faculty
    template_name = 'FacultyManagement/facultymanagement.html'


class CreateFaculty(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        form = CreateFaculties
        return render(request, 'FacultyManagement/createfaculty.html', {'form': form})


class AdminSaveUserFaculty(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Faculty
    fields = ['name']
    success_url = reverse_lazy('AdminCreateFaculty')
    success_message = 'Faculty Created'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ResetPassword(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        user = User.objects.get(hashid=pk)
        form = ChangePassword
        context = {
            'user': user,
            'form': form
        }
        return render(request, 'AdminUserManagement/resetpassword.html', context)


class SavePassword(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        user = User.objects.get(id=pk)
        form = ChangePassword(request.POST or None)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            if password1 == password2:
                if password1 != '' and password2 != '':
                    user.set_password(password2)
                    user.save()
                    messages.success(request, 'Password Reset Successful')
                    return redirect('AdminUserManagement')
                else:
                    messages.error(request, 'Cannot be null')
            else:
                messages.error(request, 'Password did not match')
                return HttpResponseRedirect(reverse('AdminResetPassword', kwargs={'pk': user.hashid}))
        else:
            return HttpResponseRedirect(reverse('AdminResetPassword', kwargs={'pk': user.hashid}))


class EditFaculty(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        faculty = Faculty.objects.get(hashid=pk)
        form = CreateFaculties(request.POST or None, instance=faculty)
        return render(request, 'FacultyManagement/editfaculty.html', {'form': form, 'pk': faculty})


class UpdateFaculty(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Faculty
    fields = ['name']
    success_message = 'Faculty Updated'
    success_url = reverse_lazy('FacultyManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DeleteFaculty(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        faculty = Faculty.objects.get(hashid=pk)
        return render(request, 'FacultyManagement/deletefaculty.html', {'faculty': faculty})


class ConfirmDeleteFaculty(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Faculty
    success_message = 'Faculty Deleted'
    success_url = reverse_lazy('FacultyManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class DepartmentManagement(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'FacultyManagement/departmentmanagement.html'


class CreateDepartment(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        queryset = Faculty.objects.all()
        return render(request, 'FacultyManagement/createdepartment.html', {'queryset': queryset})


class SaveDepartment(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        dept = request.POST.get('dept')
        faculty = request.POST.get('faculty')
        sch_id = Faculty.objects.get(id=faculty)
        if dept != '':
            Department.objects.create(name=dept, faculty=sch_id)
            messages.success(request, 'Department created')
        else:
            messages.error(request, 'Cannot be Null')
        return redirect('CreateDepartment')


class DeleteDepartment(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        dept = Department.objects.get(hashid=pk)
        return render(request, 'FacultyManagement/deletedepartment.html', {'dept': dept})


class ConfirmDeleteDepartment(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Department
    success_message = 'Department Deleted'
    success_url = reverse_lazy('DepartmentManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class EditDepartment(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        dept = Department.objects.get(hashid=pk)
        queryset = Faculty.objects.all()
        context = {
            'dept': dept,
            'queryset': queryset,
            'pk': dept
        }
        return render(request, 'FacultyManagement/editdepartment.html', context)


class UpdateDepartment(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        name = request.POST.get('dept')
        faculty = request.POST.get('faculty')
        sch_id = Faculty.objects.get(id=faculty)
        dept = Department.objects.get(id=pk)
        dept.name = name
        dept.faculty = sch_id
        dept.save()
        messages.success(request, 'Department updated')
        return redirect('DepartmentManagement')


class CourseManagement(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'FacultyManagement/coursemanagement.html'


class CreateCourse(LoginRequiredMixin, View):
    @staticmethod
    def get(request, *args, **kwargs):
        queryset = Department.objects.all()
        return render(request, 'FacultyManagement/createcourse.html', {'queryset': queryset})


class SaveCourse(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        name = request.POST.get('course')
        duration = request.POST.get('duration')
        dept = request.POST.get('dept')
        dept_id = Department.objects.get(id=dept)
        faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
        Course.objects.create(name=name, department=dept_id, faculty=faculty_id, duration=duration)
        messages.success(request, 'Course Created')
        return redirect('CreateCourse')


class EditCourse(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        course = Course.objects.get(hashid=pk)
        queryset = Department.objects.all()
        context = {
            'course': course,
            'queryset': queryset,
            'pk': course
        }
        return render(request, 'FacultyManagement/editcourse.html', context)


class UpdateCourse(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        name = request.POST.get('course')
        dept = request.POST.get('dept')
        print(dept)
        dept_id = Department.objects.get(id=dept)
        dept = Course.objects.get(id=pk)
        dept.name = name
        dept.department = dept_id
        dept.save()
        messages.success(request, 'Course updated')
        return redirect('CourseManagement')


class DeleteCourse(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        course = Course.objects.get(hashid=pk)
        return render(request, 'FacultyManagement/deletecourse.html', {'course': course})


class ConfirmDeleteCourse(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Course
    success_message = 'Course Deleted'
    success_url = reverse_lazy('CourseManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ListStages(LoginRequiredMixin, generic.ListView):
    template_name = 'FacultyManagement/liststages.html'

    def get_queryset(self):
        return Stage.objects.filter(department__hashid=self.kwargs['department'])


class CreateStage(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'FacultyManagement/createstage.html'


class SaveStage(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        stage = request.POST.get('stage')
        dept = request.POST.get('dept')
        dept_id = Department.objects.get(id=dept)
        faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
        Stage.objects.create(stage=stage, department=dept_id, faculty=faculty_id)
        messages.success(request, 'Stage Created')
        return redirect('CreateStage')


class EditStage(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        stage = Stage.objects.get(hashid=pk)
        queryset = Department.objects.all()
        context = {
            'stage': stage,
            'queryset': queryset,
            'pk': stage
        }
        return render(request, 'FacultyManagement/editstage.html', context)


class UpdateStage(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        sem = request.POST.get('stage')
        dept = request.POST.get('dept')
        print(dept)
        dept_id = Department.objects.get(id=dept)
        stage = Stage.objects.get(hashid=pk)
        stage.stage = sem
        stage.department = dept_id
        stage.save()
        messages.success(request, 'Stage updated')
        return HttpResponseRedirect(reverse('ListStages', kwargs={'department': stage.department.hashid}))


class DeleteStage(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        stage = Stage.objects.get(hashid=pk)
        return render(request, 'FacultyManagement/deletestage.html', {'stage': stage})


class ConfirmDeleteStage(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Stage
    success_message = 'Stage Deleted'
    success_url = reverse_lazy('DepartmentManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ListUnits(LoginRequiredMixin, View):
    @staticmethod
    def get(request, course):
        course_id = Course.objects.get(hashid=course)
        queryset = Unit.objects.filter(course__hashid=course)

        context = {
            'object_list': queryset,
            'course_id': course_id
        }
        return render(request, 'FacultyManagement/listunits.html', context)


class CreateUnit(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        queryset = Department.objects.all()
        queryset2 = Stage.objects.all()
        queryset3 = Course.objects.all()
        form = CreateUnits(request.POST)

        context = {
            'queryset': queryset,
            'queryset2': queryset2,
            'queryset3': queryset3,
            'form': form
        }
        return render(request, 'FacultyManagement/createunit.html', context)


class SaveUnit(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        form = CreateUnits(request.POST)
        code = request.POST.get('code')
        name = request.POST.get('name')
        stage = request.POST.get('stage')
        course = request.POST.get('course')
        stage_id = Stage.objects.get(id=stage)
        course_id = Course.objects.get(id=course)
        try:
            Unit.objects.get(unit_code=code)
            messages.warning(request, 'Unit code has to be unique')
        except Unit.DoesNotExist:
            if form.is_valid():
                global_unit = form.cleaned_data['global_unit']
            Unit.objects.create(unit_code=code, stage_name=stage_id.stage, name=name, stage=stage_id,
                                course=course_id, global_unit=global_unit)
            messages.success(request, 'Unit Created')
        return redirect('CreateUnit')


class EditUnit(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        unit = Unit.objects.get(hashid=pk)
        queryset = Department.objects.all()
        queryset2 = Stage.objects.all()
        queryset3 = Course.objects.all()
        context = {
            'unit': unit,
            'queryset': queryset,
            'queryset2': queryset2,
            'queryset3': queryset3,
        }
        return render(request, 'FacultyManagement/editunit.html', context)


class UpdateUnit(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        code = request.POST.get('code')
        name = request.POST.get('name')
        stage = request.POST.get('stage')
        course = request.POST.get('course')
        dept = request.POST.get('dept')
        dept_id = Department.objects.get(id=dept)
        stage_id = Stage.objects.get(id=stage)
        course_id = Course.objects.get(id=course)
        unit = Unit.objects.get(id=pk)
        unit.code = code
        unit.name = name
        unit.stage = stage_id
        unit.department = dept_id
        unit.course = course_id
        unit.save()
        messages.success(request, 'Unit Updated')
        return HttpResponseRedirect(reverse('ListUnits', kwargs={'course': unit.course.hashid}))


class DeleteUnit(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        unit = Unit.objects.get(hashid=pk)
        return render(request, 'FacultyManagement/deleteunit.html', {'unit': unit})


class ConfirmDeleteUnit(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Unit
    success_message = 'Unit Deleted'
    success_url = reverse_lazy('CourseManagement')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class ListDeans(LoginRequiredMixin, ListView):
    model = Dean
    template_name = 'AdminUserManagement/listdeans.html'


class CreateDeanProfile(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        form = DeanProfile
        queryset = User.objects.filter(usertype='DEAN')
        queryset1 = Faculty.objects.all()
        return render(request, 'AdminUserManagement/createdeanprofile.html',
                      {'form': form, 'queryset': queryset, 'queryset1': queryset1})


class SaveDeanProfile(LoginRequiredMixin, View):
    @staticmethod
    def post(request, *args, **kwargs):
        dean = request.POST.get('dean')
        faculty = request.POST.get('faculty')
        user_id = User.objects.get(id=dean)
        sch_id = Faculty.objects.get(id=faculty)
        try:
            Dean.objects.get(user=dean)
            messages.warning(request, 'This Users profile exists')
        except Dean.DoesNotExist:
            if Dean.objects.filter(faculty=sch_id).exists():
                messages.info(request, 'This faculty already has a dean assigned to it')
                pass
            else:
                user_id.has_profile = True
                user_id.save()
                Dean.objects.create(user=user_id, faculty=sch_id)
                messages.success(request, 'Dean Profile Created')
        return redirect('AdminCreateDeanProfile')


class Compose(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = NoticeBoardForm
        return render(request, 'AdminNoticeBoard/compose.html', {'form': form})


class PostNotice(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = NoticeBoardForm(request.POST)
        if form.is_valid():
            user_id = User.objects.get(id=request.user.id)
            addressed_to = form.cleaned_data['addressed_to']
            notice_title = form.cleaned_data['notice_title']
            notice = form.cleaned_data['notice']
            NoticeBoard.objects.create(written_by=user_id, addressed_to=addressed_to, notice_title=notice_title,
                                       notice=notice)
            messages.success(request, 'Notice posted')
        return redirect('AdminCompose')


class SentNotices(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        user_id = User.objects.get(id=request.user.id)
        notices = NoticeBoard.objects.filter(written_by=user_id)
        return render(request, 'AdminNoticeBoard/list_notices.html', {'notices': notices})


class Inbox(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        notices = NoticeBoard.objects.filter(addressed_to='ADMIN').order_by('-id')
        now = timezone.now()
        return render(request, 'AdminNoticeBoard/inbox.html', {'notices': notices, 'now': now})


class UserId(View):
    @staticmethod
    def get(request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        return user.hashid


class ReadNotice(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        notice = NoticeBoard.objects.get(hashid=pk)
        return render(request, 'AdminNoticeBoard/read.html', {'notice': notice})


class DeleteNotice(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        notice = NoticeBoard.objects.get(hashid=pk)
        return render(request, 'AdminNoticeBoard/delete.html', {'notice': notice})


class ConfirmDeleteNotice(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = NoticeBoard
    success_message = 'Notice Deleted'
    success_url = reverse_lazy('AdminSentNotices')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class EditNotice(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        notice_id = NoticeBoard.objects.get(hashid=pk)
        form = NoticeBoardForm(request.POST or None, instance=notice_id)
        return render(request, 'AdminNoticeBoard/edit.html', {'form': form, 'notice_id': notice_id})


class UpdateNotice(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = NoticeBoard
    fields = ['addressed_to', 'notice_title', 'notice']
    success_message = 'Notice Updated'
    success_url = reverse_lazy('AdminSentNotices')

    def form_valid(self, form):
        return super().form_valid(form)



@method_decorator(csrf_exempt, name='dispatch')
class FetchPermissions(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        all_permissions = list(Permission.objects.values_list('name', flat=True))
        return JsonResponse({'all_permissions': all_permissions})


@method_decorator(csrf_exempt, name='dispatch')
class UserPermissions(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        groups = Group.objects.all()
        group_data = []
        for group in groups:
            permissions = group.permissions.all()
            permission_list = [permission.name for permission in permissions]
            all_permissions = list(Permission.objects.values_list('name', flat=True))
            group_data.append({'name': group.name, 'permissions': permission_list, 'all_permissions': all_permissions})
        return JsonResponse(group_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UpdatePermissions(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        group_name = request.POST.get('SelectedGroup')
        SelectedPerms = request.POST.get('SelectedPerms')
        RemovedPerms = request.POST.get('RemovedPerms')
        json_data = json.loads(RemovedPerms)
        json_data1 = json.loads(SelectedPerms)
        group = Group.objects.get(name=group_name)
        if group_name != '':
            for selected_perms in json_data1:
                selected_permission = Permission.objects.filter(name=selected_perms)
                for selected_permission in selected_permission:
                    group.permissions.add(selected_permission)
            for removed_perms in json_data:
                removed_permission = Permission.objects.filter(name=removed_perms)
                for removed_permission in removed_permission:
                    group.permissions.remove(removed_permission)
            return HttpResponse('success')
        else:
            return HttpResponse('Failed')



class UserGroupsAndPermissions(LoginRequiredMixin, TemplateView):
    template_name = 'AdminUserManagement/groups.html'


class ViewPermissions(LoginRequiredMixin, View):
    @staticmethod
    def get(request, name):
        permissions = Permission.objects.all()
        group = Group.objects.get(name=name)
        group_permissions = group.permissions.all()
        return render(request, 'AdminUserManagement/permissions.html',
                      {'name': name, 'group': group, 'group_permissions': group_permissions, 'permissions': permissions})


class RemovePermission(LoginRequiredMixin, View):
    @staticmethod
    def get(request, name, pk):
        group = Group.objects.get(name=name)
        permission = group.permissions.get(id=pk)
        return render(request, 'AdminUserManagement/removepermission.html', {'group': group, 'permission': permission})


class ConfirmRemoval(LoginRequiredMixin, View):
    @staticmethod
    def post(request, name, pk):
        group = Group.objects.get(name=name)
        print(group)
        permission = group.permissions.get(id=pk)
        group.permissions.remove(permission)
        group.save()
        messages.success(request, 'Permission Removed')
        return HttpResponseRedirect(reverse('ViewPermissions', kwargs={'name': name}))


class AssignPermission(LoginRequiredMixin, View):
    @staticmethod
    def get(request, name, pk):
        group = Group.objects.get(name=name)
        permission = Permission.objects.get(id=pk)
        return render(request, 'AdminUserManagement/assignpermission.html', {'group': group, 'permission': permission})


class ConfirmAssignment(LoginRequiredMixin, View):
    @staticmethod
    def post(request, name, pk):
        group = Group.objects.get(name=name)
        permission = Permission.objects.get(id=pk)
        group.permissions.add(permission)
        group.save()
        messages.success(request, 'Permission Assigned')
        return HttpResponseRedirect(reverse('ViewPermissions', kwargs={'name': name}))


class UserLog(LoginRequiredMixin, ListView):
    template_name = 'userlogs.html'

    def get_queryset(self):
        return UserActivity.objects.exclude(user__usertype__in=[""]).order_by('-timestamp')


@method_decorator(csrf_exempt, name='dispatch')
class OpenSemesterRegistration(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        depts = request.POST.get('SelectedDepts')
        remdepts = request.POST.get('RemovedDepts')
        no_of_days = request.POST.get('days')
        json_data = json.loads(depts)
        json_data1 = json.loads(remdepts)
        deadline = timezone.now() + timedelta(days=30)
        try:
            deadlines = Deadlines.objects.get(active=True)
            if no_of_days != '':
                extend = timezone.now() + timedelta(days=int(no_of_days))
                deadlines.sem_reg_deadline = extend
            else:
                deadlines.sem_reg_deadline = deadline
            deadlines.save()
            for dept in json_data:
                departments = Department.objects.get(hashid=dept)
                deadlines.departments.add(departments)
            for dept in json_data1:
                departments = Department.objects.get(hashid=dept)
                deadlines.departments.remove(departments)
        except Deadlines.DoesNotExist:
            Deadlines.objects.create(active=True, sem_reg_deadline=deadline)
            deadlines = Deadlines.objects.get(active=True)
            for dept in json_data:
                departments = Department.objects.get(hashid=dept)
                deadlines.departments.add(departments)
            for dept in json_data1:
                departments = Department.objects.get(hashid=dept)
                deadlines.departments.remove(departments)
        try:
            student_group = Group.objects.get(name='Student_group')
            permission = Permission.objects.get(codename='add_semesterreg')
            student_group.permissions.add(permission)
        except Group.DoesNotExist:
            pass
        except Permission.DoesNotExist:
            pass
        return HttpResponse('success')


class SaveStatusLog(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            # if not 'msg' in request.POST or not 'pk' in request.POST or not 'value' in request.POST:
            #     _data = {'success': False, 'error_msg': 'Error missing POST parameter'}
            #     return JsonResponse(_data)
            _model = apps.get_model('UserLogs', request.POST['model'])
            _obj = _model.objects.filter(pk=request.POST['pk']).first()
            setattr(_obj, request.POST['name'], request.POST['value'])
            _obj.save()
            _data = {'success': True}
            return JsonResponse(_data)
        except Exception as e:
            _data = {
                'success': False,
                'error_msg': f'Exception:{e}'
            }
            return JsonResponse(_data)


class UpdateUser(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            # if not 'msg' in request.POST or not 'pk' in request.POST or not 'value' in request.POST:
            #     _data = {'success': False, 'error_msg': 'Error missing POST parameter'}
            #     return JsonResponse(_data)
            _model = apps.get_model('User', request.POST['model'])
            _obj = _model.objects.filter(pk=request.POST['pk']).first()
            setattr(_obj, request.POST['name'], request.POST['value'])
            _obj.save()
            _data = {'success': True}
            return JsonResponse(_data)
        except Exception as e:
            _data = {
                'success': False,
                'error_msg': f'Exception:{e}'
            }
            return JsonResponse(_data)


class YearsOfStudy(LoginRequiredMixin, ListView):
    model = Year
    template_name = 'ResultsManagement/list_years.html'


class ApproveResults(LoginRequiredMixin, View):
    @staticmethod
    def get(request, student, year_of_study):
        user_id = User.objects.get(hashid=student)
        year = Year.objects.get(year=year_of_study, student=user_id)

        result = Results.objects.filter(year=year, hod_approved = True, student__hashid=user_id.hashid).order_by('unit__unit_code')
        if result.count() > 0:
            for result in result:
                result.admin_approved = True
                result.save()
            messages.success(request, f'Results for {user_id.username} have been updated')
        else:
            messages.warning(request, 'Results for this Year do not exist')
        return redirect('YearsOfStudy')


class StudentResults(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        year = Year.objects.get(hashid=pk)
        results = Results.objects.filter(year=year.id)

        context = {
            'year': year,
            'results': results,
        }
        return render(request, 'ResultsManagement/list_results.html', context)


class StudentRegistrations(LoginRequiredMixin, ListView):
    model = SemesterReg
    template_name = 'ResultsManagement/list_regs.html'


class RegisteredUnits(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk, stage):
        student = User.objects.get(hashid=pk)
        stage = Stage.objects.get(hashid=stage)
        reg_sems = SemesterReg.objects.filter(student=student, stage=stage, current=True)
        queryset = RegistrationReport.objects.filter(student=student.id, unit__stage__id=stage.id)

        return render(request, 'ResultsManagement/list_reg_units.html',
                      {'queryset': queryset, 'stage': stage, 'student': student, 'reg_sems': reg_sems.count()})


class Deregister(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        queryset = RegistrationReport.objects.get(id=pk)
        return render(request, 'ResultsManagement/confirm_deregistration.html', {'queryset': queryset})


class ConfirmDeregistration(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        queryset = RegistrationReport.objects.get(id=pk)
        student = User.objects.get(id=queryset.student.id)
        unit = Unit.objects.get(id=queryset.unit.id)
        result = Results.objects.get(student=student, unit=unit)
        result.delete()
        queryset.status = False
        queryset.submitted = False
        queryset.save()
        messages.success(request, 'Unit deregistration successful')
        return redirect('StudentRegistrations')


class GenerateProvisionalTranscripts(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        student = Students.objects.all()
        for std in student:
            try:
                year = Year.objects.get(student=std.user.id, current=True)
                result = Results.objects.filter(student=std.user.id, year=year, hod_approved=True).order_by('unit__unit_code')
                if result.count() > 0:
                    for result in result:
                        result.admin_approved = True
                        result.save()
                    messages.success(request, 'All Results approved')
                else:
                    pass
            except Year.DoesNotExist:
                pass
        return redirect('YearsOfStudy')
