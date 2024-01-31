import io
import json
import logging
from io import BytesIO

import PyPDF3
from PyPDF3 import PdfFileReader, PdfFileWriter
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, CreateView, ListView, DeleteView, DetailView
from django.core.files import File
from reportlab.pdfgen import canvas

from Faculty.models import *
from Lecturer.models import *
from Student.forms.CreateProfile import STDDetails, CreateSTDProfile
from Student.forms.InterSchoolTransferForm import InterSchoolTransfersForm, KCSEResultsForm, ResultSlipForm
from Student.forms.LecturerEvaluationForm import LecEvaluationForm
from Student.models import *
from django.http import HttpResponse

from utils.pdf_generator import render_to_pdf

User = get_user_model()
db_logger = logging.getLogger('db')


def calculate_position_of_last_line(page, timestamp):
    last_line = 0

    for obj in page:
        if isinstance(obj, PyPDF3.pdf.PageObject):
            text_content = obj.extractText().strip()
            if text_content:
                y_coord = obj['y']
                if y_coord > last_line:
                    last_line = y_coord
    return last_line + 20


def generate_exam_card(original_pdf):
    timestamp = timezone.now()
    with open(original_pdf.path, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        pdf_writer = PdfFileWriter()
        page = pdf_reader.getPage(0)
        page_width = page.mediaBox.getUpperRight_x()
        page_height = page.mediaBox.getUpperRight_y()
        packet = io.BytesIO()
        y_position = calculate_position_of_last_line(page, timestamp)
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        c.setFont("Helvetica", 10)
        c.drawString(page_width - 360, y_position, f"Printed at: {timestamp}")
        c.save()
        packet.seek(0)
        watermark = PdfFileReader(packet)
        page.mergeTranslatedPage(watermark.getPage(0), 0, 0)
        pdf_writer.addPage(page)
        pdf_writer.write(packet)
        packet.seek(0)
    return packet


def generate_transcript(original_pdf):
    timestamp = timezone.now().strftime("%A, %d, %B, %Y")
    with open(original_pdf.path, 'rb') as pdf_file:
        pdf_reader = PdfFileReader(pdf_file)
        pdf_writer = PdfFileWriter()
        page = pdf_reader.getPage(0)
        page_width = page.mediaBox.getUpperRight_x()
        page_height = page.mediaBox.getUpperRight_y()
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=(page_width, page_height))
        c.setFont("Helvetica", 10)
        c.drawString(page_width - 360, 20, f"Date Printed: {timestamp}")
        c.save()
        packet.seek(0)
        watermark = PdfFileReader(packet)
        page.mergeTranslatedPage(watermark.getPage(0), 0, 0)
        pdf_writer.addPage(page)
        pdf_writer.write(packet)
        packet.seek(0)
    return packet


def get_stage(request):
    return SemesterReg.objects.get(current=True, student=request.user.id)


class Dashboard(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        list_submitted_unit = RegistrationReport.objects.filter(submitted=True, status=True,
                                                                student=request.user.id)
        queryset = Students.objects.get(user=request.user.id)
        form = CreateSTDProfile(request.POST or None, instance=queryset)
        try:
            stage = get_stage(request)
            sem = str(stage.stage.stage)
            strng = sem.replace(' ', '')
            strng1 = ""
            c1 = str(strng[0])
            c2 = str(strng[4])
            c3 = str(strng[5])
            c4 = str(strng[13])
            name = [c1, c2, c3, c4]
            semester = strng1.join(name)
        except SemesterReg.DoesNotExist:
            semester = None
        context = {'queryset': queryset, 'profile_form': form,
                   'stage': semester,
                   'list_submitted_unit': list_submitted_unit
                   }
        return render(request, 'STDDashboard/Dashboard.html', context)


class UpdateProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        queryset = Students.objects.get(user=request.user.id)
        form = CreateSTDProfile(request.POST or None, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile Updated')
        else:
            messages.error(request, 'Failed to update profile')
        return redirect('STDDashboard')


class CreateProfile(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        form = CreateSTDProfile
        profile_form = STDDetails
        queryset = Course.objects.all()
        return render(request, 'STDProfile/CreateProfile.html',
                      {'form': form, 'profile_form': profile_form, 'queryset': queryset})


class SaveProfile(LoginRequiredMixin, CreateView):
    def post(self, request, *args, **kwargs):
        form = CreateSTDProfile(request.POST)
        profile_form = STDDetails(request.POST, request.FILES)
        user = User.objects.get(id=request.user.id)
        if form.is_valid() and profile_form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            id_no = form.cleaned_data['id_no']
            nationality = form.cleaned_data['nationality']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            course = request.POST.get('course')
            dob = request.POST.get('dob')
            course_id = Course.objects.get(id=course)
            dept_id = Department.objects.get(id=course_id.department.id)
            try:
                Students.objects.get(phone_number=phone_number)
                messages.error(request, 'Phone number exists, please provide a different phone number')
                return redirect('STDCreateProfile')
            except Students.DoesNotExist:
                Students.objects.create(user=user, phone_number=phone_number, id_no=id_no, nationality=nationality,
                                        address=address, gender=gender, course=course_id,
                                        date_of_birth=dob
                                        )
                profile_pic = profile_form.cleaned_data['profile_pic']
                first_name = profile_form.cleaned_data['first_name']
                middle_name = profile_form.cleaned_data['middle_name']
                last_name = profile_form.cleaned_data['last_name']
                email = profile_form.cleaned_data['email']
                user.profile_pic = profile_pic
                user.first_name = first_name
                user.middle_name = middle_name
                user.last_name = last_name
                user.email = email
                user.has_profile = True
                user.save()
                messages.success(request, 'Profile Created')
                messages.info(request, 'You can now access your account')
                db_logger.info(f'{request.user.username} created profile successfully')
                return redirect('STDDashboard')
        else:
            messages.error(request, 'Invalid input, Please check that all fields are filled correctly')
            db_logger.error(f'{request.user.username} failed to create profile')
            return redirect('STDCreateProfile')


class SemesterRegistration(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        if not request.user.has_perm('Faculty.add_semesterreg'):
            messages.info(self.request, 'Semester registration is closed')
            return redirect('STDDashboard')
        else:
            student = Students.objects.get(user=request.user.id)
            semester = Stage.objects.filter(department=student.department.id).last()
            if SemesterReg.objects.filter(stage=semester, student=request.user.id).exists():
                messages.warning(request, 'Your Semester is not defined, Please contact the system admin')
                return redirect('STDDashboard')
            else:
                try:
                    SemesterReg.objects.get(end_date__gt=timezone.now(), student=request.user.id)
                    messages.info(request, 'You are currently in session, please contact '
                                           'system administrator if you registered for the wrong semester')
                    return redirect('STDDashboard')
                except SemesterReg.DoesNotExist:
                    user_id = Students.objects.get(user=self.request.user.id)
                    dept_id = Department.objects.get(id=user_id.department.id)
                    context = {'queryset': Stage.objects.filter(department=dept_id.id),

                               }
                    return render(request, 'registration/sem_reg.html', context)


class SubmitSemReg(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        user_id = User.objects.get(id=request.user.id)
        stage = request.POST.get('stage')
        stage_id = Stage.objects.get(id=stage)
        sem = str(stage_id.stage)
        student = Students.objects.get(user=user_id)
        now = timezone.now()
        end_date = now + timedelta(days=120)
        parts = sem.split()
        for i in range(len(parts) - 1):
            if parts[i] == "Year" and parts[i + 1].isdigit():
                year = f"{parts[i]} {parts[i + 1]}"
        try:
            Year.objects.get(student=user_id, year=year)
            pass
        except Year.DoesNotExist:
            current_yr = Year.objects.filter(student=user_id, current=True)
            for current_yr in current_yr:
                current_yr.current = False
                current_yr.save()
            faculty_id = Faculty.objects.get(id=student.faculty.id)
            Year.objects.create(student=user_id, year=year, stage=stage_id, faculty=faculty_id)
        try:
            reg = SemesterReg.objects.get(student=user_id, current=True)
            reg.current = False
            reg.save()
            unit_reg = UnitRegistration.objects.get(active=True, student=user_id)
            unit_reg.active = False
            unit_reg.save()
            reg_report = RegistrationReport.objects.filter(registration_id=unit_reg, status=True)
            for units in reg_report:
                units.status = False
                units.save()
            resit_reg_report = RegistrationReport.objects.filter(student=request.user.id, resit=True)
            for units in resit_reg_report:
                units.resit = False
                units.save()
            exam_card = ExamCards.objects.get(user=user_id, current=True)
            exam_card.current = False
            exam_card.save()
            SemesterReg.objects.get(stage=stage_id, student=user_id)
            db_logger.info(f'{request.user.username} registered for a semester successfully')
            messages.success(request, f'You have successfully registered for {stage_id.stage}')
        except ObjectDoesNotExist:
            SemesterReg.objects.get_or_create(student=user_id, stage=stage_id, current=True, end_date=end_date)
            db_logger.info(f'{request.user.username} registered for a semester successfully')
            messages.success(request, f'You have successfully registered for {stage_id.stage}')
        return redirect('STDDashboard')


class RegisteredSemesters(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        context = {
            'check_exists': SemesterReg.objects.filter(current=True, student=request.user.id).exists(),
            'object_list': SemesterReg.objects.filter(student=request.user.id),

        }
        return render(request, 'registration/registered_sems.html', context)


class UnitsRegistration(LoginRequiredMixin, View):

    def get(self, request):
        if not request.user.has_perm('Faculty.add_unitregistration'):
            messages.warning(self.request, 'Unit Registration is closed')
            return redirect('STDDashboard')
        else:
            try:
                stage = SemesterReg.objects.get(current=True, student=request.user.id)
                pending_units = RegistrationReport.objects.filter(submitted=False, status=True, student=request.user.id)
                list_submitted_unit = RegistrationReport.objects.filter(submitted=True, status=True,
                                                                        student=request.user.id)
            except SemesterReg.DoesNotExist:
                stage = None
                pending_units = None
                list_submitted_unit = None
            context = {

                'stage': stage,
                'pending_units': pending_units,
                'list_submitted_unit': list_submitted_unit,
                'reg_exists': RegistrationReport.objects.filter(submitted=False, status=True,
                                                                student=request.user.id).exists(),
                'user': Students.objects.get(user=request.user.id),
            }
        return render(request, 'registration/unit_registration.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class FetchUnits(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        stage_id = request.POST.get("stage")
        list_data = []
        if stage_id != "":
            user_id = User.objects.get(id=request.user.id)
            course_id = Students.objects.get(user=user_id.id)
            unit = Unit.objects.filter(course=course_id.course.id, stage=stage_id)
            semester = Stage.objects.get(id=stage_id)
            units = Unit.objects.filter(global_unit=True, stage_name=semester.stage)
            try:
                unit_id = UnitRegistration.objects.get(stage=stage_id, active=True, student=request.user.id)
                reg_report = RegistrationReport.objects.filter(registration_id=unit_id, status=False,
                                                               student=request.user.id)
                for reg_units in reg_report:
                    data_small = {"id": reg_units.unit.id, "code": reg_units.unit.unit_code,
                                  "name": reg_units.unit.name + "",
                                  'status': reg_units.status}
                    list_data.append(data_small)
            except UnitRegistration.DoesNotExist:
                for Units in units:
                    data_small = {"id": Units.id, "code": Units.unit_code, "name": Units.name + ""}
                    list_data.append(data_small)
                for Units in unit:
                    data_small = {"id": Units.id, "code": Units.unit_code, "name": Units.name + ""}
                    list_data.append(data_small)
        else:
            list_data = []
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitUnits(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        unit_data = request.POST.get("unit_data")
        stage_id = request.POST.get("stage_id")
        semester = Stage.objects.get(id=stage_id)
        student = User.objects.get(id=request.user.id)
        json_student = json.loads(unit_data)
        try:
            unit_id = UnitRegistration.objects.get(stage=stage_id, active=True, student=request.user.id)
            for stud in json_student:
                units_id = Unit.objects.get(id=stud['id'])
                reg_report = RegistrationReport.objects.get(unit=units_id.id, registration_id=unit_id,
                                                            student=request.user.id)
                reg_report.status = stud['status']
                reg_report.save()
            return HttpResponse('Updated')
        except UnitRegistration.DoesNotExist:
            unit_registration = UnitRegistration(student=student, stage=semester)
            unit_registration.save()
            for stud in json_student:
                units_id = Unit.objects.get(id=stud['id'])
                registration_report = RegistrationReport(unit=units_id, status=stud['status'], student=student,
                                                         registration_id=unit_registration)
                registration_report.save()
            return HttpResponse("OK")


class Deregister(LoginRequiredMixin, SuccessMessageMixin, View):
    @staticmethod
    def get(request, pk):
        queryset = RegistrationReport.objects.get(hashid=pk)
        queryset.status = False
        queryset.save()
        messages.success(request, 'Unit deregistration successful')
        return redirect('UnitRegistration')


class Submit(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        reg_report = RegistrationReport.objects.filter(status=True, submitted=False, student=request.user.id)
        user_id = User.objects.get(id=request.user.id)
        student = Students.objects.get(user=request.user.id)
        stage = SemesterReg.objects.get(current=True, student=request.user.id)
        semesters = Stage.objects.get(id=stage.stage.id)
        year = Year.objects.get(current=True, student=user_id)
        for unit in reg_report:
            units = Unit.objects.get(id=unit.unit.id)
            unit.submitted = True
            unit.save()
            try:
                Results.objects.get(student=user_id, unit=units)
                pass
            except Results.DoesNotExist:
                Results.objects.create(student=user_id, stage=semesters, unit=units, year=year)
            db_logger.info(f'{request.user.username} registered for units successfully')
            messages.success(request, 'Units registration successful')
        reg_units = RegistrationReport.objects.filter(submitted=True, status=True,
                                                      student=request.user.id).order_by('unit__unit_code')
        sem = str(stage.stage.stage)
        strng = sem.replace(' ', '')
        _len = len(strng)
        c1 = str(strng[0])
        c2 = str(strng[4])
        c3 = str(strng[5])
        c5 = str(strng[6])
        c6 = str(strng[7])
        c4 = str(strng[13])
        strng1 = ""
        sem1 = [c1, c2, c3, c4]
        sem2 = [c3, c5, c6, ' ', c4]
        semester = strng1.join(sem1)
        semester2 = strng1.join(sem2)
        exam_card_number = randint(10000, 999999)
        context = {
            'reg_units': reg_units,
            'student': student,
            'stage': semester,
            'semester': semester2,
            'exam_card_number': exam_card_number
        }
        pdf = render_to_pdf('pdf/exam_card.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'ExamCard-%s.pdf' % request.user.username.replace('/', '')
        content = 'inline; filename=%s' % filename
        response['Content-Disposition'] = content
        exam_card_file = BytesIO(pdf.content)
        File_upload = File(exam_card_file, filename)
        try:
            exam_cards = ExamCards.objects.get(user=request.user.id, current=True)
            exam_cards.delete()
            ExamCards.objects.create(user=user_id, stage=semesters, exam_card=File_upload, current=True,
                                     exam_card_number=exam_card_number)
        except ExamCards.DoesNotExist:
            upload_exam_card = ExamCards(user=user_id, stage=semesters, exam_card=File_upload, current=True,
                                         exam_card_number=exam_card_number)
            upload_exam_card.save()
        return redirect('UnitRegistration')


def fetch_exam_card(request):
    try:
        exam_card = ExamCards.objects.get(user=request.user.id, current=True)
        modified_pdf = generate_exam_card(exam_card.exam_card)

        response = HttpResponse(modified_pdf, content_type='application/pdf')
        filename = 'ExamCard-%s.pdf' % request.user.username.replace('/', '')
        content = 'inline; filename=%s' % filename
        response['Content-Disposition'] = content
        return response
    except ExamCards.DoesNotExist:
        return HttpResponse('File not found, contact system administrator', status=404)


class ExamCard(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        fetch_exam_card(request)
        reg_report = RegistrationReport.objects.filter(evaluated=False, status=True, student=request.user.id)
        context = {
            'check_exists': SemesterReg.objects.filter(current=True, student=request.user.id).exists(),

            'count': reg_report.count(),
            'queryset': reg_report
        }
        return render(request, 'registration/exam_card.html', context)


class ProvisionalTranscript(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        year = Year.objects.filter(student=request.user.id)
        context = {

            'year': year
        }
        return render(request, 'registration/provisional_transcript.html', context)


def get_transcript(request, user, year):
    try:
        trans_obj = ProvisionalTranscripts.objects.get(user__hashid=user, year__hashid=year)
        modified_pdf = generate_transcript(trans_obj.transcript)

        response = HttpResponse(modified_pdf, content_type='application/pdf')
        filename = 'Transcript-%s.pdf' % request.user.username.replace('/', '')
        content = 'inline; filename=%s' % filename
        response['Content-Disposition'] = content
        return response
    except ProvisionalTranscripts.DoesNotExist:
        return HttpResponse('File not found, contact system administrator', status=404)


@method_decorator(csrf_exempt, name='dispatch')
class FetchTranscript(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        year = request.POST.get('select_year')
        if year != '':
            user = request.POST.get('user_id')
            user_id = User.objects.get(id=user)
            year_id = Year.objects.get(id=year)
            get_transcript(request, user, year)
            list_data = []
            data = {'user': user_id.hashid, 'year': year_id.hashid}
            list_data.append(data)
        else:
            list_data = []
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


class ResitExamRegistration(LoginRequiredMixin, View):

    def get(self, request):
        if not request.user.has_perm('Faculty.add_unitregistration'):
            messages.warning(self.request, 'Resit exam Registration is closed')
            return redirect('STDDashboard')
        else:
            queryset = SemesterReg.objects.filter(student=request.user.id)
            year = Year.objects.filter(student=request.user.id)
            user = Students.objects.get(user=request.user.id)
            pending_units = RegistrationReport.objects.filter(submitted=False, resit=True,
                                                              student=request.user.id)
            list_submitted_unit = RegistrationReport.objects.filter(submitted=True, resit=True,
                                                                    student=request.user.id)

            context = {

                'pending_units': pending_units,
                'list_submitted_unit': list_submitted_unit,
                'reg_exists': RegistrationReport.objects.filter(submitted=False, resit=True,
                                                                student=request.user.id).exists(),
                'queryset': queryset,
                'user': user,
                'year': year,
                'count': RegistrationReport.objects.filter(submitted=True, resit=True,
                                                           student=request.user.id).count()
            }
        return render(request, 'registration/resit_exam_registration.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class FetchFailedUnits(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        stage_id = request.POST.get("stage")
        year_id = request.POST.get("year")
        if stage_id != "" and year_id != "":
            user_id = User.objects.get(id=request.user.id)
            unit = Results.objects.filter(student=user_id, stage=stage_id, year=year_id)
            list_data = []
            for Units in unit:
                report = RegistrationReport.objects.filter(unit=Units.unit.id, supplementary=False, student=user_id)
                if Units.grade == 'E' and report.exists():
                    data_small = {"id": Units.unit.id, "code": Units.unit.unit_code, "name": Units.unit.name + ""}
                    list_data.append(data_small)
        else:
            list_data = []
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitFailedUnits(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        unit_data = request.POST.get("unit_data")
        json_student = json.loads(unit_data)
        for stud in json_student:
            unit_id = Unit.objects.get(id=stud['id'])
            reg_report = RegistrationReport.objects.get(unit=unit_id, student=request.user.id)
            reg_report.resit = True
            reg_report.current = True
            reg_report.save()
        return HttpResponse('OK')


class DeregisterResit(LoginRequiredMixin, SuccessMessageMixin, View):
    @staticmethod
    def get(request, pk):
        queryset = RegistrationReport.objects.get(hashid=pk)
        queryset.status = False
        queryset.save()
        messages.success(request, 'Unit deregistration successful')
        return redirect('ResitExamRegistration')


class SaveFailedUnits(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        reg_report = RegistrationReport.objects.filter(status=True, submitted=False, student=request.user.id)
        user_id = User.objects.get(id=request.user.id)
        for unit in reg_report:
            units = Unit.objects.get(id=unit.unit.id)
            unit.submitted = True
            unit.save()
            result = Results.objects.get(student=user_id, unit=units)
            result.current = True
            result.hod_approved = False
            result.admin_approved = False
            result.save()
            db_logger.info(f'{request.user.username} registered for units successfully')
            messages.success(request, 'Units registration successful')
        return redirect('ResitExamRegistration')


class SupplementaryExamRegistration(LoginRequiredMixin, View):

    def get(self, request):
        if not request.user.has_perm('Faculty.change_unitregistration'):
            messages.warning(self.request, 'Supplementary exam Registration is closed')
            return redirect('STDDashboard')
        else:
            queryset = SemesterReg.objects.filter(student=request.user.id)
            year = Year.objects.filter(student=request.user.id)
            user = Students.objects.get(user=request.user.id)
            pending_units = RegistrationReport.objects.filter(submitted=False, supplementary=True,
                                                              student=request.user.id)
            list_submitted_unit = RegistrationReport.objects.filter(submitted=True, supplementary=True,
                                                                    student=request.user.id)

            context = {

                'pending_units': pending_units,
                'list_submitted_unit': list_submitted_unit,
                'reg_exists': RegistrationReport.objects.filter(submitted=False, supplementary=True,
                                                                student=request.user.id).exists(),
                'queryset': queryset,
                'user': user,
                'year': year,
                'count': RegistrationReport.objects.filter(submitted=True, supplementary=True,
                                                           student=request.user.id).count()
            }
        return render(request, 'registration/special_exam_registration.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class FetchPendingUnits(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        stage_id = request.POST.get("stage")
        year_id = request.POST.get("year")
        if stage_id != "" and year_id != "":
            user_id = User.objects.get(id=request.user.id)
            unit = Results.objects.filter(student=user_id, stage=stage_id, year=year_id)
            list_data = []
            for Units in unit:
                report = RegistrationReport.objects.filter(unit=Units.unit.id, supplementary=False, student=user_id)
                if Units.grade == 'X' and report.exists():
                    data_small = {"id": Units.unit.id, "code": Units.unit.unit_code, "name": Units.unit.name + ""}
                    list_data.append(data_small)
        else:
            list_data = []
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitPendingUnits(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        unit_data = request.POST.get("unit_data")
        json_student = json.loads(unit_data)
        for stud in json_student:
            unit_id = Unit.objects.get(id=stud['id'])
            reg_report = RegistrationReport.objects.get(unit=unit_id, student=request.user.id)
            reg_report.supplementary = True
            reg_report.current = True
            reg_report.save()
        return HttpResponse('OK')


class DownloadSupCard(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        student = Students.objects.get(user=request.user.id)
        name = [str(student.user.middle_name), ', ', str(student.user.first_name), ' ', str(student.user.last_name)]
        stage = SemesterReg.objects.get(current=True, student=request.user.id)
        reg_units = RegistrationReport.objects.filter(submitted=True, supplementary=True,
                                                      student=request.user.id)
        sem = str(stage.stage.stage)
        strng = sem.replace(' ', '')
        _len = len(strng)
        c1 = str(strng[0])
        c2 = str(strng[4])
        c3 = str(strng[5])
        c5 = str(strng[6])
        c6 = str(strng[7])
        c4 = str(strng[13])
        strng1 = ""
        sem1 = [c1, c2, c3, c4]
        sem2 = [c3, c5, c6, ' ', c4]
        semester = strng1.join(sem1)
        semester2 = strng1.join(sem2)
        full_name = strng1.join(name)
        upper_case = semester2.upper()
        upper_case1 = full_name.upper()
        context = {
            'reg_units': reg_units,
            'student': student,
            'stage': semester,
            'semester': upper_case,
            'full_name': upper_case1
        }
        pdf = render_to_pdf('pdf/supplementary_card.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'SupCard-%s.pdf' % request.user.username.replace('/', '')
        content = 'inline; filename=%s' % filename
        response['Content-Disposition'] = content
        return response


class DownloadResitCard(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        student = Students.objects.get(user=request.user.id)
        name = [str(student.user.middle_name), ', ', str(student.user.first_name), ' ', str(student.user.last_name)]
        stage = SemesterReg.objects.get(current=True, student=request.user.id)
        reg_units = RegistrationReport.objects.filter(submitted=True, resit=True,
                                                      student=request.user.id)
        sem = str(stage.stage.stage)
        strng = sem.replace(' ', '')
        _len = len(strng)
        c1 = str(strng[0])
        c2 = str(strng[4])
        c3 = str(strng[5])
        c5 = str(strng[6])
        c6 = str(strng[7])
        c4 = str(strng[13])
        strng1 = ""
        sem1 = [c1, c2, c3, c4]
        sem2 = [c3, c5, c6, ' ', c4]
        semester = strng1.join(sem1)
        semester2 = strng1.join(sem2)
        full_name = strng1.join(name)
        upper_case = semester2.upper()
        upper_case1 = full_name.upper()
        context = {
            'reg_units': reg_units,
            'student': student,
            'stage': semester,
            'semester': upper_case,
            'full_name': upper_case1
        }
        pdf = render_to_pdf('pdf/resit_card.html', context)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'ResitCard-%s.pdf' % request.user.username.replace('/', '')
        content = 'inline; filename=%s' % filename
        response['Content-Disposition'] = content
        return response


class LecturersEvaluation(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        if not request.user.has_perm('Faculty.add_lecturerevaluation'):
            messages.info(request, 'Lecturer Evaluation is closed')
            return redirect('STDDashboard')
        else:
            units = RegistrationReport.objects.filter(student=request.user.id, status=True, evaluated=False)
            form = LecEvaluationForm

            context = {
                'units': units,
                'form': form,

            }
            return render(request, 'Extras/lec_evaluation.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class FetchInstructor(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        unit_id = request.POST.get('unit')
        list_data = []
        if unit_id != '':
            instructor = UnitSelection.objects.get(unit=unit_id, approved='2')
            data_small = {"id": instructor.instructor.id,
                          "full_name": instructor.instructor.first_name + ' ' + instructor.instructor.last_name}
            list_data.append(data_small)
        else:
            list_data = []
        return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class SubmitEvaluation(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        lec = request.POST.get('lec')
        unit = request.POST.get('unit')
        unit_id = Unit.objects.get(id=unit)
        if lec != "":
            instructor_id = User.objects.get(id=lec)
            promotes_critical_thinking = request.POST.get("a")
            ties_in_primary_objectives_of_the_course = request.POST.get("b")
            explains_concepts_clearly = request.POST.get("c")
            uses_concrete_examples_of_concepts = request.POST.get("d")
            gives_multiple_examples = request.POST.get("e")
            points_out_practical_applications = request.POST.get("f")
            stresses_important_concepts = request.POST.get("g")
            repeats_difficult_ideas = request.POST.get("h")
            encourages_questions_and_comments = request.POST.get("i")
            answers_questions_clearly = request.POST.get("j")
            available_to_students_after_class = request.POST.get("k")
            asks_questions_of_class = request.POST.get("m")
            facilitates_discussions_during_lecture = request.POST.get("l")
            proceeds_at_good_pace_for_topic = request.POST.get("n")
            stays_on_theme_of_lecture = request.POST.get("o")
            states_lecture_objectives = request.POST.get("p")
            gives_preliminary_overview_of_lecture = request.POST.get("q")
            signals_transition_to_new_topic = request.POST.get("r")
            explains_how_each_topic_fits_in = request.POST.get("s")
            projects_confidence = request.POST.get("t")
            speaks_expressively_or_emphatically = request.POST.get("u")
            moves_about_while_lecturing = request.POST.get("v")
            gestures_while_speaking = request.POST.get("w")
            shows_facial_expression = request.POST.get("x")
            uses_humor = request.POST.get("y")
            LecturerEvaluation.objects.create(
                instructor=instructor_id, unit=unit_id, promotes_critical_thinking=promotes_critical_thinking,
                ties_in_primary_objectives_of_the_course=ties_in_primary_objectives_of_the_course,
                explains_concepts_clearly=explains_concepts_clearly,
                uses_concrete_examples_of_concepts=uses_concrete_examples_of_concepts,
                gives_multiple_examples=gives_multiple_examples,
                points_out_practical_applications=points_out_practical_applications,
                stresses_important_concepts=stresses_important_concepts,
                repeats_difficult_ideas=repeats_difficult_ideas,
                encourages_questions_and_comments=encourages_questions_and_comments,
                answers_questions_clearly=answers_questions_clearly,
                available_to_students_after_class=available_to_students_after_class,
                asks_questions_of_class=asks_questions_of_class,
                facilitates_discussions_during_lecture=facilitates_discussions_during_lecture,
                proceeds_at_good_pace_for_topic=proceeds_at_good_pace_for_topic,
                stays_on_theme_of_lecture=stays_on_theme_of_lecture,
                states_lecture_objectives=states_lecture_objectives,
                gives_preliminary_overview_of_lecture=gives_preliminary_overview_of_lecture,
                signals_transition_to_new_topic=signals_transition_to_new_topic,
                explains_how_each_topic_fits_in=explains_how_each_topic_fits_in,
                projects_confidence=projects_confidence,
                speaks_expressively_or_emphatically=speaks_expressively_or_emphatically,
                moves_about_while_lecturing=moves_about_while_lecturing,
                gestures_while_speaking=gestures_while_speaking, shows_facial_expression=shows_facial_expression,
                uses_humor=uses_humor
            )
            reg_report = RegistrationReport.objects.get(student=request.user.id, unit=unit_id)
            reg_report.evaluated = True
            reg_report.save()
            return HttpResponse('Evaluated')
        else:
            return HttpResponse('Null')


class InterSchoolTransfer(LoginRequiredMixin, View):
    @staticmethod
    def get(request):
        form = InterSchoolTransfersForm
        form2 = KCSEResultsForm
        form3 = ResultSlipForm
        student = Students.objects.get(user=request.user.id)
        queryset = KCSEResults.objects.filter(student=request.user.id)
        my_applications = InterSchooltransfer.objects.filter(student=request.user.id)
        try:
            result_slip = ResultSlip.objects.get(student=request.user.id)
        except ResultSlip.DoesNotExist:
            result_slip = None

        context = {
            'form': form,
            'form2': form2,
            'form3': form3,
            'student': student,
            'queryset': queryset,
            'my_applications': my_applications,
            'result_slip': result_slip,

        }
        return render(request, 'Extras/inter_school_transfer.html', context)


class AddSubject(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        form = KCSEResultsForm(request.POST)
        user_id = User.objects.get(id=request.user.id)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            grade = form.cleaned_data['grade']
            try:
                kcse_result = KCSEResults.objects.get(student=user_id, subject=subject)
                kcse_result.grade = grade
                kcse_result.save()
            except KCSEResults.DoesNotExist:
                KCSEResults.objects.get_or_create(student=user_id, subject=subject, grade=grade)
            messages.success(request, 'Subject added')
        return redirect('InterSchoolTransfer')


class UploadResultSlip(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        form = ResultSlipForm(request.POST or None, request.FILES)
        if form.is_valid():
            user_id = User.objects.get(id=request.user.id)
            kcse_result_slip = form.cleaned_data['kcse_result_slip']
            try:
                result_slip = ResultSlip.objects.get(student=user_id)
                result_slip.kcse_result_slip = kcse_result_slip
                result_slip.save()
            except ResultSlip.DoesNotExist:
                ResultSlip.objects.get_or_create(student=user_id, kcse_result_slip=kcse_result_slip)
            messages.success(request, 'ResultSlip Uploaded')
        return redirect('InterSchoolTransfer')


class SubmitTransferRequest(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        reason = request.POST.get('reason')
        new_programme = request.POST.get('new_programme')
        aggregate = request.POST.get('aggregate')

        if reason != "" and aggregate != "" and new_programme != "":
            course_id = Course.objects.get(id=new_programme)
            user_id = User.objects.get(id=request.user.id)
            student = Students.objects.get(user=user_id)
            if course_id.id == student.course.id:
                return HttpResponse("Exists")
            else:
                try:
                    trans_request = InterSchooltransfer.objects.get(student=request.user.id, new_programme=course_id,
                                                                    status='pending')
                    trans_request.reason = reason
                    trans_request.save()
                except InterSchooltransfer.DoesNotExist:
                    trans_request = InterSchooltransfer(reason=reason, student=user_id, new_programme=course_id,
                                                        aggregate=aggregate)
                    trans_request.save()
                    result_slip = ResultSlip.objects.filter(student=user_id)
                    results = KCSEResults.objects.filter(student=user_id)
                    trans_request.kcse_resultslip.add(*result_slip)
                    trans_request.kcse_results.add(*results)
                db_logger.info(f'{request.user} Submitted a transfer request')
                return HttpResponse("Submitted")
        else:
            return HttpResponse("Failed")


class DeleteSubject(LoginRequiredMixin, DetailView):
    model = KCSEResults
    context_object_name = 'result'
    template_name = 'Extras/confirm_subject_remove.html'


class ConfirmDeleteSubject(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    success_url = reverse_lazy('InterSchoolTransfer')
    success_message = 'Subject removed'
    model = KCSEResults


class SkipLecEvaluation(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        reg_report = RegistrationReport.objects.filter(student=request.user.id, evaluated=False, submitted=True)
        for evaluated in reg_report:
            evaluated.evaluated = True
            evaluated.save()
        return redirect('ExamCard')