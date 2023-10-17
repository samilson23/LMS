import logging
from io import BytesIO

from django.apps import apps
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files import File
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, CreateView, ListView, DetailView, DeleteView

from Dean.forms.CreateProfile import CreateDeanProfile, DeanProfilePicture, DeanDetails
from Dean.forms.CreateUserAccountForm import CreateUserAccount
from Dean.forms.ResetPassword import ChangePassword
from Dean.models import *
from Faculty.models import *
from Lecturer.models import *
from Student.models import Students, ProvisionalTranscripts
from utils.pdf_generator import render_to_pdf

db_logger = logging.getLogger('db')


class UpdateDean(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            faculty_id = request.POST['value']
            sch_id = Faculty.objects.get(id=faculty_id)
            _model = apps.get_model('Dean', request.POST['model'])
            _obj = _model.objects.filter(pk=request.POST['pk']).first()
            setattr(_obj, request.POST['name'], sch_id)
            _obj.save()
            _data = {'success': True}
            return JsonResponse(_data)
        except Exception as e:
            _data = {
                'success': False,
                'error_msg': f'Exception:{e}'
            }
            return JsonResponse(_data)


class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        queryset = Dean.objects.get(user=request.user.id)
        user = User.objects.get(id=request.user.id)
        user_form = DeanDetails(request.POST or None, instance=user)
        form = CreateDeanProfile(request.POST or None, instance=queryset)
        try:
            depts = Department.objects.filter(faculty=queryset.faculty.id).count()
            courses = Course.objects.filter(faculty=queryset.faculty.id).count()
            students = Students.objects.filter(faculty=queryset.faculty.id).count()
            lecturers = Lecturers.objects.filter(faculty=queryset.faculty.id).count()
        except Department.DoesNotExist:
            courses = 0
            students = 0
            lecturers = 0
            depts = 0
        return render(request, 'Dashboard/DeanDashboard.html',
                      {'queryset': queryset, 'profile_form': form, 'user_form': user_form,
                       'depts': depts, 'courses': courses, 'students': students, 'lecturers': lecturers
                       })


class UpdateProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        queryset = Dean.objects.get(user=request.user.id)
        queryset2 = User.objects.get(id=request.user.id)
        form = CreateDeanProfile(request.POST or None, instance=queryset)
        user_form = DeanDetails(request.POST, request.FILES, instance=queryset2)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            db_logger.info(f'{request.user.username} updated profile')
            messages.success(request, 'Profile Updated')
        else:
            db_logger.error(f'{request.user.username} failed to update profile')
            messages.error(request, 'Invalid input, Please ensure all fields are filled correctly')
        return redirect('DeanDashBoard')


class CreateProfile(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = CreateDeanProfile
        profile_form = DeanProfilePicture
        queryset = Faculty.objects.all()
        return render(request, 'DeanProfile/CreateProfile.html',
                      {'form': form, 'profile_form': profile_form, 'queryset': queryset})


class SaveProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = CreateDeanProfile(request.POST)
        profile_form = DeanProfilePicture(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)
        if form.is_valid() and profile_form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            id_no = form.cleaned_data['id_no']
            nationality = form.cleaned_data['nationality']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            faculty = request.POST.get('faculty')
            faculty_id = Faculty.objects.get(id=faculty)
            Dean.objects.create(user=user, phone_number=phone_number, id_no=id_no, nationality=nationality,
                                address=address, gender=gender, faculty=faculty_id
                                )
            profile_pic = profile_form.cleaned_data['profile_pic']
            user.profile_pic = profile_pic
            user.has_profile = True
            user.save()
            messages.success(request, 'Profile Created')
            messages.info(request, 'You can now access your account')
            db_logger.info(f'{request.user.username} created profile')
            return redirect('DeanDashBoard')
        else:
            db_logger.error(f'{request.user.username} failed to create profile')
            messages.error(request, 'Invalid input, Please ensure all fields are filled correctly')
            return redirect('DeanCreateProfile')


class UserManagement(LoginRequiredMixin, ListView):
    permission_required = 'User.view_user'
    permission_denied_message = 'Permission Denied'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanDashBoard')
        else:
            queryset = User.objects.all()
            return render(request, 'DeanUserManagement/usermanagement.html', {'object_list': queryset})


class CreateUser(LoginRequiredMixin, TemplateView):
    permission_denied_message = 'Permission Denied'

    def get(self, request, *args, **kwargs):
        if not self.request.user.has_perm('User.add_user'):
            db_logger.warning(f'Permission denied for {request.user.usertype}')
            messages.error(self.request, 'Permission Denied')
            return redirect('DeanUserManagement')
        else:
            form = CreateUserAccount
        return render(request, 'DeanUserManagement/createuseraccount.html', {'form': form})


class SaveUserAccount(LoginRequiredMixin, View):
    permission_required = 'User.add_user'
    permission_denied_message = 'Permission Denied'

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
        else:
            form = CreateUserAccount(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                usertype = form.cleaned_data['usertype']
                user = User(username=username, usertype=usertype)
                user.set_password(username)
                user.save()
                db_logger.info(f'{request.user.username} created user account')
                messages.success(request, 'User Account Created')
            else:
                db_logger.error(f'{request.user.username} failed to create user account')
                messages.error(request, 'Failed to create User Account')
        return redirect('DeanCreateUserAccount')


class ActivateDeactivate(LoginRequiredMixin, View):
    permission_required = 'User.change_user'
    permission_denied_message = 'Permission Denied'

    def get(self, request, pk):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
        else:
            acc = User.objects.get(hashid=pk)

            if not acc.is_active:
                acc.is_active = True
                messages.success(request, "User account has been activated")
                db_logger.info(f'{request.user.username} activated user account')
            elif acc.is_active:
                acc.is_active = False
                db_logger.info(f'{request.user.username} deactivated user account')
                messages.error(request, "User account has been Deactivated")
            acc.save()
        return redirect('DeanUserManagement')


class DeleteUserAccount(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'DeanUserManagement/deleteuser.html'


class ConfirmDelete(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = 'User Account Deleted'
    success_url = reverse_lazy('DeanUserManagement')

    def form_valid(self, form):
        db_logger.info(f'{self.request.user.username} deleted user account')
        return super().form_valid(form)

    def form_invalid(self, form):
        db_logger.error(f'{self.request.user.username} deleted user account')
        return super().form_valid(form)


class ResetPassword(LoginRequiredMixin, View):
    permission_required = 'User.change_user'
    permission_denied_message = 'Permission Denied'

    def get(self, request, pk):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanUserManagement')
        else:
            user = User.objects.get(hashid=pk)
            form = ChangePassword
            context = {
                'user': user,
                'form': form
            }
        return render(request, 'DeanUserManagement/resetpassword.html', context)


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
                    db_logger.info(f'{request.user.username} reset user password')
                    return redirect('DeanUserManagement')
                else:
                    messages.error(request, 'Cannot be null')
            else:
                messages.error(request, 'The passwords did not match')
                db_logger.error(f'{request.user.username} failed reset user password')
            return HttpResponseRedirect(reverse('DeanResetPassword', kwargs={'pk': user.hashid}))


class StudentsProfile(LoginRequiredMixin, ListView):
    permission_required = 'Dean.login'
    permission_denied_message = 'Permission Denied'

    def get(self, request, *args, **kwargs):
        queryset = Students.objects.all()
        return render(request, 'DeanUserManagement/liststudents.html', {'object_list': queryset})


class ListCourses(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        try:
            user_id = User.objects.get(id=request.user.id)
            dean_id = Dean.objects.get(user=user_id)
            sch_id = Faculty.objects.get(id=dean_id.faculty.id)
            queryset = Course.objects.filter(faculty=sch_id)
            return render(request, 'DeanFacultyManagement/ListCourses.html', {'queryset': queryset})
        except Department.DoesNotExist:
            return render(request, 'DeanFacultyManagement/ListCourses.html')


class ListDepartments(LoginRequiredMixin, View):

    @staticmethod
    def get(request):
        user_id = User.objects.get(id=request.user.id)
        dean_id = Dean.objects.get(user=user_id)
        sch_id = Faculty.objects.get(id=dean_id.faculty.id)
        queryset = Department.objects.filter(faculty=sch_id)
        return render(request, 'DeanFacultyManagement/listdepartments.html', {'queryset': queryset})


class ListUnits(LoginRequiredMixin, View):

    @staticmethod
    def get(request, pk):
        course = Course.objects.get(hashid=pk)
        queryset = Unit.objects.filter(course=course)
        return render(request, 'DeanFacultyManagement/listunits.html', {'queryset': queryset, 'course': course})


class ListStages(LoginRequiredMixin, View):
    permission_denied_message = 'Permission denied'

    @staticmethod
    def get(request):
        try:
            user_id = User.objects.get(id=request.user.id)
            dean_id = Dean.objects.get(user=user_id)
            dept_id = Faculty.objects.get(id=dean_id.faculty.id)
            queryset = Stage.objects.filter(faculty=dept_id)
            return render(request, 'DeanFacultyManagement/liststages.html',
                          {'queryset': queryset, 'dept_id': dept_id})
        except Department.DoesNotExist:
            return render(request, 'DeanFacultyManagement/liststages.html')


class CreateStage(LoginRequiredMixin, ListView):
    permission_required = 'Faculty.add_stage'
    permission_denied_message = 'Permission Denied'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanListStages')
        else:
            user_id = Dean.objects.get(user=request.user.id)
            faculty_id = Faculty.objects.get(id=user_id.faculty.id)
            queryset = Department.objects.filter(faculty=faculty_id)
            return render(request, 'DeanFacultyManagement/createstage.html', {'object_list': queryset})


class SaveStage(LoginRequiredMixin, View):
    permission_required = 'Faculty.add_stage'
    permission_denied_message = 'Permission Denied'

    def post(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanListStages')
        else:
            stage = request.POST.get('stage')
            dept = request.POST.get('dept')
            user_id = User.objects.get(id=request.user.id)
            dean_id = Dean.objects.get(user=user_id)
            sch_id = Faculty.objects.get(id=dean_id.faculty.id)
            dept_id = Department.objects.get(id=dept)
            Stage.objects.create(stage=stage, department=dept_id, faculty=sch_id)
            messages.success(request, 'Stage Created')
            db_logger.info(f'{request.user.username} created stage')
            return redirect('DeanCreateStage')


class EditStage(LoginRequiredMixin, View):
    permission_required = 'Faculty.change_stage'
    permission_denied_message = 'Permission Denied'

    def get(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanListStages')
        else:
            stage = Stage.objects.get(hashid=pk)
            queryset = Department.objects.all()
            context = {
                'stage': stage,
                'queryset': queryset,
                'pk': stage
            }
            return render(request, 'DeanFacultyManagement/editstage.html', context)


class UpdateStage(LoginRequiredMixin, View):
    permission_required = 'Faculty.change_stage'
    permission_denied_message = 'Permission Denied'

    def post(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
        else:
            sem = request.POST.get('stage')
            dept = request.POST.get('dept')
            print(dept)
            dept_id = Department.objects.get(id=dept)
            stage = Stage.objects.get(id=pk)
            stage.stage = sem
            stage.department = dept_id
            stage.save()
            messages.success(request, 'Stage updated')
            db_logger.info(f'{request.user.username} changed stage')
        return redirect('DeanListStages')


class CreateCourse(LoginRequiredMixin, View):
    permission_required = 'Faculty.add_course'
    permission_denied_message = 'Permission Denied'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanListCourses')
        else:
            user_id = Dean.objects.get(user=request.user.id)
            faculty_id = Faculty.objects.get(id=user_id.faculty.id)
            queryset = Department.objects.filter(faculty=faculty_id)
            return render(request, 'DeanFacultyManagement/createcourse.html', {'queryset': queryset})


class SaveCourse(LoginRequiredMixin, View):
    permission_required = 'Faculty.add_course'
    permission_denied_message = 'Permission Denied'

    def post(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanListCourses')
        else:
            name = request.POST.get('course')
            duration = request.POST.get('duration')
            dept = request.POST.get('dept')
            dept_id = Department.objects.get(id=dept)
            faculty_id = Faculty.objects.get(id=dept_id.faculty.id)
            Course.objects.create(name=name, department=dept_id, faculty=faculty_id, duration=duration)
            messages.success(request, 'Course Created')
            db_logger.info(f'{request.user.username} created course')
        return redirect('DeanCreateCourse')


class EditCourse(LoginRequiredMixin, View):
    permission_required = 'Faculty.change_course'
    permission_denied_message = 'Permission Denied'

    def get(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanListCourses')
        else:
            course = Course.objects.get(hashid=pk)
            user_id = Dean.objects.get(user=request.user.id)
            faculty_id = Faculty.objects.get(id=user_id.faculty.id)
            queryset = Department.objects.filter(faculty=faculty_id)
            context = {
                'course': course,
                'queryset': queryset,
                'pk': course
            }
            return render(request, 'DeanFacultyManagement/editcourse.html', context)


class UpdateCourse(LoginRequiredMixin, View):
    permission_required = 'Faculty.change_course'
    permission_denied_message = 'Permission Denied'

    def post(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
        else:
            name = request.POST.get('course')
            dept = request.POST.get('dept')
            print(dept)
            dept_id = Department.objects.get(id=dept)
            dept = Course.objects.get(id=pk)
            dept.name = name
            dept.department = dept_id
            dept.save()
            messages.success(request, 'Course updated')
            db_logger.info(f'{request.user.username} updated course')
        return redirect('DeanListCourses')


class StudentDetails(LoginRequiredMixin, View):
    permission_required = 'Student.view_students'
    permission_denied_message = 'Permission Denied'

    def get(self, request, pk, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.error(request, self.permission_denied_message)
            return redirect('DeanStudentsProfile')
        else:
            try:
                students = User.objects.get(hashid=pk)
                context = {
                    'user': students
                }
                return render(request, 'DeanUserManagement/StudentDetails.html', context)
            except PermissionError:
                no_permission_error = str('Permission Denied')
                messages.error(request, no_permission_error)
                return redirect('DeanStudentsProfile')


class ApplicationRequests(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        user_id = User.objects.get(id=request.user.id)
        dean_id = Dean.objects.get(user=user_id)
        queryset = UnitSelection.objects.filter(unit__course__faculty__id=dean_id.faculty.id)
        context = {
            'object_list': queryset,
        }
        return render(request, 'unit_application/Units.html', context)


class UnitApplication(LoginRequiredMixin, ListView):
    permission_required = 'Faculty.add_unitselection'
    permission_denied_message = 'Unit Application is closed at the moment'

    def get(self, request, *args, **kwargs):
        if not request.user.has_perm(self.permission_required):
            messages.info(request, self.permission_denied_message)
            return redirect('DeanApplicationRequests')
        else:
            queryset = Unit.objects.all()
            return render(request, 'unit_application/unit_application.html', {'object_list': queryset})


class SubmitApplication(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    def post(self, request, *args, **kwargs):
        unit = request.POST.get('unit')
        level_of_understanding = request.POST.get('lou')
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

        return redirect('DeanUnitApplication')


class MyUnits(LoginRequiredMixin, ListView):
    def get_queryset(self):
        return UnitSelection.objects.filter(instructor=self.request.user.id)

    def get_template_names(self):
        return 'unit_application/MyUnits.html'


class ApproveApplication(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        unit = UnitSelection.objects.get(hashid=pk)
        unit.approved = '2'
        unit.save()
        db_logger.info('Unit Application Approved')
        messages.success(request, 'Unit Application has been approved')
        return redirect('DeanApplicationRequests')


class RejectApplication(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        unit = UnitSelection.objects.get(hashid=pk)
        unit.approved = '3'
        unit.save()
        db_logger.info('Unit Application Rejected')
        messages.info(request, 'Unit Application has been Rejected')
        return redirect('DeanApplicationRequests')


class YearsOfStudy(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        dean_id = Dean.objects.get(user=request.user.id)
        faculty_id = Faculty.objects.get(id=dean_id.faculty.id)
        years = Year.objects.filter(faculty=faculty_id)
        context = {
            'object_list': years
        }

        return render(request, 'DeanResultsManagement/list_years.html', context)


class GenerateProvisionalTranscripts(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        dean_id = Dean.objects.get(user=request.user.id)
        faculty = Faculty.objects.get(id=dean_id.faculty.id)
        student = Students.objects.filter(faculty=faculty)
        for std in student:
            try:
                year = Year.objects.get(student=std.user.id, current=True)
                result = Results.objects.filter(student=std.user.id, year=year, hod_approved=True).order_by('unit__unit_code')
                user_id = User.objects.get(id=std.user.id)
                if result.count() > 0:
                    total = 0
                    for grade_value in result:
                        total += grade_value.grade_value
                        print(total)
                        credit_hours = 1 + (2 / 3)
                        average = total * credit_hours
                        grade_average = int(average)

                    count = Results.objects.filter(student=user_id, grade_points=0, year=year).count()
                    context = {
                        'queryset': result,
                        'user': user_id,
                        'student': std,
                        'year': year,
                        'grade_average': grade_average,
                        'count': count,
                        'count1': Results.objects.filter(student=user_id, grade_points=0).count()
                    }
                    pdf = render_to_pdf('pdf/provisional_transcript.html', context)
                    response = HttpResponse(pdf, content_type='application/pdf')
                    name = str(user_id.username)
                    username = name.replace('/', '')
                    filename = 'Transcript-%s.pdf' % username
                    content = 'attachment; filename=%s' % filename
                    response['Content-Disposition'] = content
                    transcript_file = BytesIO(pdf.content)
                    File_upload = File(transcript_file, filename)
                    try:
                        transcript = ProvisionalTranscripts.objects.get(user=user_id, year=year)
                        transcript.delete()
                        ProvisionalTranscripts.objects.create(user=user_id, transcript=File_upload, year=year)
                    except ProvisionalTranscripts.DoesNotExist:
                        ProvisionalTranscripts.objects.create(user=user_id, transcript=File_upload, year=year)
                    for result in result:
                        result.dean_approved = True
                        result.save()
                    db_logger.info(f'{request.user.username} approved all student results')
                    messages.success(request, 'All Results approved')
                else:
                    pass
            except Year.DoesNotExist:
                pass
        return redirect('DeanYearsOfStudy')


class ApproveResults(LoginRequiredMixin, View):
    @staticmethod
    def get(request, student, year_of_study):
        user_id = User.objects.get(hashid=student)
        stds = Students.objects.get(user=user_id)
        year = Year.objects.get(year=year_of_study, student=user_id)

        result = Results.objects.filter(year=year, student__hashid=user_id.hashid).order_by('unit__unit_code')
        if result.count() > 0:
            total = 0
            for grade_value in result:
                total += grade_value.grade_value
                credit_hours = 1 + (2 / 3)
                average = total * credit_hours
                grade_average = int(average)

            count = Results.objects.filter(student=user_id,
                                      grade_points=0, year=year).count()
            context = {
                'queryset': result,
                'user': user_id,
                'student': stds,
                'year': year,
                'grade_average': grade_average,
                'count': count,
                'count1': Results.objects.filter(student=user_id, grade_points=0).count()
            }
            pdf = render_to_pdf('pdf/provisional_transcript.html', context)
            response = HttpResponse(pdf, content_type='application/pdf')
            name = str(user_id.username)
            username = name.replace('/', '')
            filename = 'Transcript-%s.pdf' % username
            content = 'attachment; filename=%s' % filename
            response['Content-Disposition'] = content
            transcript_file = BytesIO(pdf.content)
            File_upload = File(transcript_file, filename)
            try:
                transcript = ProvisionalTranscripts.objects.get(user=user_id, year=year)
                transcript.delete()
                ProvisionalTranscripts.objects.create(user=user_id, transcript=File_upload, year=year)
            except ProvisionalTranscripts.DoesNotExist:
                ProvisionalTranscripts.objects.create(user=user_id, transcript=File_upload, year=year)
            for result in result:
                result.dean_approved = True
                result.hod_approved = True
                result.save()
            messages.success(request, f'Results for {user_id.username} have been updated')
        else:
            messages.warning(request, 'Results for this Year do not exist')
        return redirect('DeanYearsOfStudy')


class StudentResults(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        year = Year.objects.get(hashid=pk)
        results = Results.objects.filter(year=year.id)

        context = {
            'year': year,
            'results': results,
        }
        return render(request, 'DeanResultsManagement/list_results.html', context)


class TransferRequests(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        dean = Dean.objects.get(user=request.user.id)
        queryset = InterSchooltransfer.objects.filter(new_programme__faculty__id=dean.faculty.id)

        context = {
            'object_list': queryset
        }
        return render(request, 'Extras/transfer_requests.html', context)


class KsceResults(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        queryset = KCSEResults.objects.filter(student__hashid=pk)
        try:
            result_slip = ResultSlip.objects.get(student__hashid=pk)
        except ResultSlip.DoesNotExist:
            result_slip = None
        context = {
            'queryset': queryset,
            'result_slip': result_slip,
        }
        return render(request, 'Extras/Kcse_results.html', context)


class ApproveTransferRequest(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        trans_request = InterSchooltransfer.objects.get(student__hashid=pk)

        context = {
            'trans_request': trans_request
        }
        return render(request, 'Extras/confirm_approval.html', context)


class ConfirmTransApproval(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        trans_request = InterSchooltransfer.objects.get(student__hashid=pk)
        trans_request.status = 'approved'
        trans_request.save()
        messages.success(request, f'Transfer request for {trans_request.student.username} has been approved')
        return HttpResponseRedirect(reverse('KsceResults', kwargs={'pk': trans_request.student.hashid}))


class RejectTransferRequest(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        trans_request = InterSchooltransfer.objects.get(student__hashid=pk)

        context = {
            'trans_request': trans_request
        }
        return render(request, 'Extras/confirm_rejection.html', context)


class ConfirmTransRejection(LoginRequiredMixin, View):
    @staticmethod
    def post(request, pk):
        trans_request = InterSchooltransfer.objects.get(student__hashid=pk)
        trans_request.status = 'rejected'
        trans_request.save()
        messages.info(request, f'Transfer request for {trans_request.student.username} has been rejected')
        return HttpResponseRedirect(reverse('KsceResults', kwargs={'pk': trans_request.student.hashid}))


class LeaveRequest(LoginRequiredMixin, ListView):
    template_name = 'Extras/Dean_leave_requests.html'

    def get_queryset(self):
        return LeaveRequests.objects.filter(reliever__id=self.request.user.id)


class ApproveLeaveRequest(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        leave_request = LeaveRequests.objects.get(hashid=pk)
        leave_request.status = 'approved'
        leave_request.save()
        messages.info(request, 'Leave Request approved.')
        return redirect('DeanLeaveRequests')


class RejectLeaveRequest(LoginRequiredMixin, View):
    @staticmethod
    def get(request, pk):
        leave_request = LeaveRequests.objects.get(hashid=pk)
        leave_request.status = 'rejected'
        leave_request.save()
        messages.info(request, 'Leave Request rejected.')
        return redirect('DeanLeaveRequests')
