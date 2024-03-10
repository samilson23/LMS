from django.urls import path

from Student.views import *


urlpatterns = [
    path('Dashboard', Dashboard.as_view(), name='STDDashboard'),
    path('UpdateProfile', UpdateProfile.as_view(), name='STDUpdateProfile'),
    path('CreateProfile', CreateProfile.as_view(), name='STDCreateProfile'),
    path('SaveProfile', SaveProfile.as_view(), name='STDSaveProfile'),
    path('SemesterRegistration', SemesterRegistration.as_view(), name='SemesterRegistration'),
    path('SubmitSemReg', SubmitSemReg.as_view(), name='SubmitSemReg'),
    path('RegisteredSemesters', RegisteredSemesters.as_view(), name='RegisteredSemesters'),
    path('UnitRegistration', UnitsRegistration.as_view(), name='UnitRegistration'),
    path('FetchUnits', FetchUnits.as_view(), name='get_units'),
    path('SubmitUnits', SubmitUnits.as_view(), name='submit_units'),
    path('SupplementaryExamRegistration', SupplementaryExamRegistration.as_view(), name='SupplementaryExamRegistration'),
    path('FetchPendingUnits', FetchPendingUnits.as_view(), name='fetch_pending_units'),
    path('SubmitPendingUnits', SubmitPendingUnits.as_view(), name='submit_pending_units'),
    path('DownloadSupCard', DownloadSupCard.as_view(), name='DownloadSupCard'),
    path('Submit', Submit.as_view(), name='Submit'),
    path('ExamCard', ExamCard.as_view(), name='ExamCard'),
    path('fetch_exam_card', fetch_exam_card, name='fetch_exam_card'),
    path('ResitExamRegistration', ResitExamRegistration.as_view(), name='ResitExamRegistration'),
    path('FetchFailedUnits', FetchFailedUnits.as_view(), name='get_failed_units'),
    path('SubmitFailedUnits', SubmitFailedUnits.as_view(), name='submit_failed_units'),
    path('SaveFailedUnits', SaveFailedUnits.as_view(), name='SaveFailedUnits'),
    path('DownloadResitCard', DownloadResitCard.as_view(), name='DownloadResitCard'),
    path('DeregisterResit/<pk>', DeregisterResit.as_view(), name='DeregisterResit'),
    path('ProvisionalTranscript', ProvisionalTranscript.as_view(), name='ProvisionalTranscript'),
    path('FetchTranscript', FetchTranscript.as_view(), name='FetchTranscript'),
    path('get_transcript/<year>', get_transcript, name='get_transcript'),
    path('Deregister/<pk>', Deregister.as_view(), name='Deregister'),
    path('FetchInstructor/', FetchInstructor.as_view(), name='FetchInstructor'),
    path('SkipLecEvaluation/', SkipLecEvaluation.as_view(), name='SkipLecEvaluation'),
    path('LecturerEvaluation/', LecturersEvaluation.as_view(), name='LecturerEvaluation'),
    path('SubmitEvaluation/', SubmitEvaluation.as_view(), name='SubmitEvaluation'),
    path('InterSchoolTransfer/', InterSchoolTransfer.as_view(), name='InterSchoolTransfer'),
    path('AddSubject/', AddSubject.as_view(), name='AddSubject'),
    path('UploadResultSlip/', UploadResultSlip.as_view(), name='UploadResultSlip'),
    path('SubmitTransferRequest/', SubmitTransferRequest.as_view(), name='SubmitTransferRequest'),
    path('DeleteSubject/<pk>', DeleteSubject.as_view(), name='DeleteSubject'),
    path('ConfirmDeleteSubject/<pk>', ConfirmDeleteSubject.as_view(), name='ConfirmDeleteSubject'),
    path('FeePayment/', FeePayment.as_view(), name='FeePayment'),
    path('SubmitPayment/', SubmitPayment.as_view(), name='SubmitPayment'),
    path('Checkout/', Checkout.as_view(), name='Checkout'),
    path('CompleteTransaction/', CompleteTransaction.as_view(), name='CompleteTransaction'),
    path('FeeStructure/', FeeStructures.as_view(), name='FeeStructure'),
    path('FeeStatement/', FeeStatements.as_view(), name='FeeStatement'),
    path('PaymentReceipts/', PaymentReceipts.as_view(), name='PaymentReceipts'),
    path('get_fee_structure/<department>/', get_fee_structure, name='get_fee_structure'),
    path('get_fee_statement/<student>/', get_fee_statement, name='get_fee_statement'),
    path('create_fee_statement/<stage_id>/', create_fee_statement, name='create_fee_statement'),
]
