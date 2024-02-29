import json
from datetime import date
from io import BytesIO

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.core import serializers
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from Student.models import Students
from Faculty.models import *
from utils.pdf_generator import render_to_pdf

User = get_user_model()


def leave_timer_countdown(request):
    leave_request = LeaveRequests.objects.filter(end_date__gte=timezone.now(), user=request.user.id).order_by('-start_date').first()
    if leave_request:
        now = timezone.now()
        if leave_request.start_date <= now <= leave_request.end_date:
            remaining_time = (leave_request.end_date - now).total_seconds()
        else:
            remaining_time = 0
    else:
        remaining_time = 0
    return JsonResponse({'remaining_time': remaining_time})


def get_sem_reg_deadline(request):
    try:
        try:
            students = Students.objects.get(user=request.user.id)
            sem_reg = Deadlines.objects.get(sem_reg_deadline__gte=timezone.now())
            # for student in students:
            if students.department in sem_reg.departments.all():
                now = timezone.now()
                remaining_time = (sem_reg.sem_reg_deadline - now).total_seconds()
                deadline = sem_reg.sem_reg_deadline
                return JsonResponse({'remaining_time': remaining_time, 'deadline': deadline})
            else:
                return HttpResponse('None')
        except Students.DoesNotExist:
            return HttpResponse('Error')
    except Deadlines.DoesNotExist:
        remaining_time = 0
        deadline = None
        return JsonResponse({'remaining_time': remaining_time, 'deadline': deadline})


@method_decorator(csrf_exempt, name='dispatch')
class RemovePermission(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            codename = request.POST.get('codename')
            group_name = request.POST.get('group_name')
            student_group = Group.objects.get(name=group_name)
            permission = Permission.objects.get(codename=codename)
            student_group.permissions.remove(permission)
            return HttpResponse('success')
        except Group.DoesNotExist:
            pass
            return HttpResponse('failed', status=404)
        except Permission.DoesNotExist:
            pass
            return HttpResponse('failed', status=404)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitCatMark(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        user_id = request.POST.get('user_id')
        unit_id = request.POST.get('unit')
        cat_mark = request.POST.get('cat_mark')
        print(cat_mark)
        if cat_mark != '' and 30 >= int(cat_mark) >= 0:
            result = Results.objects.get(student=user_id, unit=unit_id)
            result.cat_mark = cat_mark
            result.save()
        return HttpResponse('success')


@method_decorator(csrf_exempt, name='dispatch')
class SubmitExamMark(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        user_id = request.POST.get('user_id')
        unit_id = request.POST.get('unit')
        exam_mark = request.POST.get('exam_mark')
        result = Results.objects.get(student=user_id, unit=unit_id)
        if 70 >= int(exam_mark) >= 0 and exam_mark != '':
            result.exam_mark = exam_mark
            result.save()
        else:
            pass
        return HttpResponse('success')


class GenerateMarks(LoginRequiredMixin, View):
    @staticmethod
    def get(request, unit_code):
        unit = Unit.objects.get(unit_code=unit_code)
        if request.user.usertype == 'LECTURER':
            results = Results.objects.filter(unit=unit.id, current=True)
        else:
            results = Results.objects.filter(unit=unit.id)
        context = {
            'unit': unit,
            'results': results,
        }
        pdf = render_to_pdf('pdf/exam_marks.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        name = str(unit.unit_code)
        name1 = name.replace('/', '')
        filename = 'Exam_Marks-%s.pdf' % name1
        content = 'attachment; filename=%s' % filename
        response['Content-Disposition'] = content
        if request.user.usertype == 'LECTURER':
            for unit in results:
                unit.current = False
                unit.resit = False
                unit.save()
        return response


class UpdateFaculty(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            _model = apps.get_model('Faculty', request.POST['model'])
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


class UpdateDepartment(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            faculty_id = request.POST['value']
            sch_id = Faculty.objects.get(id=faculty_id)
            _model = apps.get_model('Faculty', request.POST['model'])
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


class UpdateCourse(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            dept_id = request.POST['value']
            dept = Department.objects.get(id=dept_id)
            _model = apps.get_model('Faculty', request.POST['model'])
            _obj = _model.objects.filter(pk=request.POST['pk']).first()
            setattr(_obj, request.POST['name'], dept)
            _obj.save()
            _data = {'success': True}
            return JsonResponse(_data)
        except Exception as e:
            _data = {
                'success': False,
                'error_msg': f'Exception:{e}'
            }
            return JsonResponse(_data)


class UpdateUnit(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            stage_id = request.POST['value']
            stage = Stage.objects.get(id=stage_id)
            _model = apps.get_model('Faculty', request.POST['model'])
            _obj = _model.objects.filter(pk=request.POST['pk']).first()
            setattr(_obj, request.POST['name'], stage)
            _obj.save()
            _data = {'success': True}
            return JsonResponse(_data)
        except Exception as e:
            _data = {
                'success': False,
                'error_msg': f'Exception:{e}'
            }
            return JsonResponse(_data)


@method_decorator(csrf_exempt, name='dispatch')
class GetFaculties(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        faculty = Faculty.objects.all()
        list_data = []
        for faculty_data in faculty:
            data_small = {"id": faculty_data.id, "name": faculty_data.name}
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GetStages(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        course_id = request.POST.get('course')
        course = Course.objects.get(id=course_id)
        dept_id = Department.objects.get(id=course.department.id)
        stage = Stage.objects.filter(department=dept_id)
        list_data = []
        for sem in stage:
            data_small = {"id": sem.id, "stage": sem.stage}
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GetDepartments(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        dept = Department.objects.all()
        list_data = []
        for dept_data in dept:
            data_small = {"id": dept_data.id, "name": dept_data.name}
            list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


def download_result_slip(request, pk):
    try:
        instance = ResultSlip.objects.get(student__hashid=pk)
        pdf_file = instance.kcse_result_slip
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        file_name = os.path.split(instance.kcse_result_slip.name)[-1]
        response['Content-Disposition'] = f'attachment; filename="' + file_name + '"'
        return response
    except ResultSlip.DoesNotExist:
        return HttpResponse('File not Found', status=404)


class CalculateDuration(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        end = datetime.strptime(end_date, '%Y-%m-%d')
        start = datetime.strptime(start_date, '%Y-%m-%d')
        delta = end - start

        list_data = []
        data_small = {'duration': delta.days}
        list_data.append(data_small)
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitLeaveRequest(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        user = request.POST.get('user_id')
        user_id = User.objects.get(id=user)
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        duration = request.POST.get('duration')
        reliever = request.POST.get('reliever')
        dean_id = User.objects.get(hashid=reliever, usertype='DEAN')

        try:
            LeaveRequests.objects.get(user=user_id, status='pending')
            return HttpResponse('Exists')
        except LeaveRequests.DoesNotExist:
            if LeaveRequests.objects.filter(user=user_id, status='approved', end_date__gte=timezone.now()).exists():
                return HttpResponse('Active')
            else:
                if duration != '' and duration is not None and int(duration) > 0 and end_date != '' and start_date != '' and date.fromisoformat(start_date) > date.today():
                    leave_request = LeaveRequests(user=user_id, start_date=start_date, duration=duration, end_date=end_date, reason=reason, status='pending', reliever=dean_id)
                    leave_request.save()
                    return HttpResponse('Submitted')
                else:
                    return HttpResponse('Failed')


@method_decorator(csrf_exempt, name='dispatch')
class Event(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        usertype = request.user.usertype
        events = Events.objects.filter(addressed_to=usertype)
        list_data = []
        for event in events:
            data = {
                'title': event.title,
                'start_time': event.start_time.isoformat(),
                'end_time': event.end_time.isoformat()
            }
            list_data.append(data)
        return JsonResponse(list_data, safe=False)
