from django.urls import path
from .views import *

urlpatterns = [
    path('SubmitCatMark', SubmitCatMark.as_view(), name='submit_cat_mark'),
    path('SubmitExamMark', SubmitExamMark.as_view(), name='submit_exam_mark'),
    path('GenerateMarks/<unit_code>/', GenerateMarks.as_view(), name='generate_marks'),
    path('UpdateFaculty/', UpdateFaculty.as_view(), name='UpdateFaculty'),
    path('UpdateDepartment/', UpdateDepartment.as_view(), name='UpdateDepartments'),
    path('UpdateCourse/', UpdateCourse.as_view(), name='UpdateCourses'),
    path('GetFaculties/', GetFaculties.as_view(), name='GetFaculties'),
    path('GetDepartments/', GetDepartments.as_view(), name='GetDepartments'),
    path('UpdateUnit/', UpdateUnit.as_view(), name='UpdateUnit'),
    path('GetStages/', GetStages.as_view(), name='GetStages'),
    path('CalculateDuration/', CalculateDuration.as_view(), name='calculate_duration'),
    path('download_result_slip/<pk>', download_result_slip, name='download_result_slip'),
    path('leave_timer_countdown', leave_timer_countdown, name='leave_timer_countdown'),
    path('get_sem_reg_deadline', get_sem_reg_deadline, name='get_sem_reg_deadline'),
    path('RemovePermission', RemovePermission.as_view(), name='STDRemovePermission'),
    path('SubmitLeaveRequest', SubmitLeaveRequest.as_view(), name='SubmitLeaveRequest'),
    path('Event', Event.as_view(), name='Events')
]
