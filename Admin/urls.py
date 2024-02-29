from django.urls import path

from Admin.views import *

urlpatterns = [
    path('Dashboard/', Dashboard.as_view(), name='AdminDashboard'),
    path('CreateProfile/', CreateProfile.as_view(), name='AdminCreateProfile'),
    path('SaveProfile/', SaveProfile.as_view(), name='AdminSaveProfile'),
    path('UserLogs/', UserLog.as_view(), name='UserLog'),
    path('UpdateProfile/', UpdateProfile.as_view(), name='AdminUpdateProfile'),
    path('UserManagement/', UserManagement.as_view(), name='AdminUserManagement'),
    path('Groups/', Groups.as_view(), name='Groups'),
    path('ViewPermissions/<name>', ViewPermissions.as_view(), name='ViewPermissions'),
    path('RemovePermission/<name>/<pk>', RemovePermission.as_view(), name='RemovePermission'),
    path('ConfirmRemoval/<name>/<pk>', ConfirmRemoval.as_view(), name='ConfirmRemoval'),
    path('AssignPermission/<name>/<pk>', AssignPermission.as_view(), name='AssignPermission'),
    path('ConfirmAssignment/<name>/<pk>', ConfirmAssignment.as_view(), name='ConfirmAssignment'),
    path('CreateUserAccount/', CreateUser.as_view(), name='AdminCreateUserAccount'),
    path('SaveUserAccount/', SaveUserAccount.as_view(), name='AdminSaveUserAccount'),
    path('DeleteUserAccount/<pk>', DeleteUserAccount.as_view(), name='AdminDeleteUserAccount'),
    path('ConfirmDelete/<pk>', ConfirmDelete.as_view(), name='AdminConfirmDelete'),
    path('ResetPassword/<pk>', ResetPassword.as_view(), name='AdminResetPassword'),
    path('SavePassword/<pk>', SavePassword.as_view(), name='AdminSavePassword'),
    path('ActivateDeactivateUser/<pk>', ActivateDeactivate.as_view(), name='AdminActivateDeactivateUser'),
    path('UserProfile/<pk>', EditUserAccount.as_view(), name='AdminUserProfile'),
    path('UpdateUserProfile/<pk>', UpdateUserProfile.as_view(), name='AdminUpdateUserProfile'),
    path('FacultyManagement/', FacultyManagement.as_view(), name='FacultyManagement'),
    path('DepartmentManagement/', DepartmentManagement.as_view(), name='DepartmentManagement'),
    path('CreateDepartment/', CreateDepartment.as_view(), name='CreateDepartment'),
    path('SaveDepartment/', SaveDepartment.as_view(), name='SaveDepartment'),
    path('UpdateFaculty/<pk>', UpdateFaculty.as_view(), name='AdminUpdateFaculty'),
    path('DeleteDepartment/<pk>', DeleteDepartment.as_view(), name='DeleteDepartment'),
    path('EditDepartment/<pk>', EditDepartment.as_view(), name='EditDepartment'),
    path('UpdateDepartment/<pk>', UpdateDepartment.as_view(), name='UpdateDepartment'),
    path('ConfirmDeleteDepartment/<pk>', ConfirmDeleteDepartment.as_view(), name='ConfirmDeleteDepartment'),
    path('EditFaculty/<pk>', EditFaculty.as_view(), name='AdminEditFaculty'),
    path('DeleteFaculty/<pk>', DeleteFaculty.as_view(), name='AdminDeleteFaculty'),
    path('ConfirmDeleteFaculty/<pk>', ConfirmDeleteFaculty.as_view(), name='AdminConfirmDeleteFaculty'),
    path('EditCourse/<pk>', EditCourse.as_view(), name='EditCourse'),
    path('UpdateCourse/<pk>', UpdateCourse.as_view(), name='UpdateCourse'),
    path('DeleteCourse/<pk>', DeleteCourse.as_view(), name='DeleteCourse'),
    path('ConfirmDeleteCourse/<pk>', ConfirmDeleteCourse.as_view(), name='ConfirmDeleteCourse'),
    path('CreateFaculty/', CreateFaculty.as_view(), name='AdminCreateFaculty'),
    path('SaveFaculty/', AdminSaveUserFaculty.as_view(), name='AdminSaveUserFaculty'),
    path('CourseManagement/', CourseManagement.as_view(), name='CourseManagement'),
    path('CreateCourse/', CreateCourse.as_view(), name='CreateCourse'),
    path('SaveCourse/', SaveCourse.as_view(), name='SaveCourse'),
    path('ListStages/<department>', ListStages.as_view(), name='ListStages'),
    path('OpenSemesterRegistration/', OpenSemesterRegistration.as_view(), name='OpenSemesterRegistration'),
    path('CreateStage/', CreateStage.as_view(), name='CreateStage'),
    path('SaveStage/', SaveStage.as_view(), name='SaveStage'),
    path('ListDeans/', ListDeans.as_view(), name='ListDeans'),
    path('EditStage/<pk>', EditStage.as_view(), name='EditStage'),
    path('UpdateStage/<pk>', UpdateStage.as_view(), name='UpdateStage'),
    path('DeleteStage/<pk>', DeleteStage.as_view(), name='DeleteStage'),
    path('ConfirmDeleteStage/<pk>', ConfirmDeleteStage.as_view(), name='ConfirmDeleteStage'),
    path('ListUnits/<course>', ListUnits.as_view(), name='ListUnits'),
    path('CreateUnit/', CreateUnit.as_view(), name='CreateUnit'),
    path('SaveUnit/', SaveUnit.as_view(), name='SaveUnit'),
    path('CreateDeanProfile/', CreateDeanProfile.as_view(), name='AdminCreateDeanProfile'),
    path('SaveDeanProfile/', SaveDeanProfile.as_view(), name='AdminSaveDeanProfile'),
    path('EditUnit/<pk>', EditUnit.as_view(), name='EditUnit'),
    path('UpdateUnit/<pk>', UpdateUnit.as_view(), name='UpdateUnit'),
    path('DeleteUnit/<pk>', DeleteUnit.as_view(), name='DeleteUnit'),
    path('ConfirmDeleteUnit/<pk>', ConfirmDeleteUnit.as_view(), name='ConfirmDeleteUnit'),
    path('DeleteNotice/<pk>', DeleteNotice.as_view(), name='AdminDeleteNotice'),
    path('EditNotice/<pk>', EditNotice.as_view(), name='AdminEditNotice'),
    path('UpdateNotice/<pk>', UpdateNotice.as_view(), name='AdminUpdateNotice'),
    path('ConfirmDeleteNotice/<pk>', ConfirmDeleteNotice.as_view(), name='AdminConfirmDeleteNotice'),
    path('ReadNotice/<pk>', ReadNotice.as_view(), name='AdminReadNotice'),
    path('Compose/', Compose.as_view(), name='AdminCompose'),
    path('PostNotice/', PostNotice.as_view(), name='AdminPostNotice'),
    path('SentNotices/', SentNotices.as_view(), name='AdminSentNotices'),
    path('Inbox/', Inbox.as_view(), name='AdminInbox'),
    path('SaveStatusLog/', SaveStatusLog.as_view(), name='SaveStatusLog'),
    path('UpdateUser/', UpdateUser.as_view(), name='UpdateUser'),
    path('RegisteredUnits/<pk>/<stage>', RegisteredUnits.as_view(), name='RegisteredUnits'),
    path('Deregister/<pk>', Deregister.as_view(), name='AdminDeregister'),
    path('ConfirmDeregistration/<pk>', ConfirmDeregistration.as_view(), name='ConfirmDeregistration'),
    path('StudentRegistrations/', StudentRegistrations.as_view(), name='StudentRegistrations'),
    path('YearsOfStudy/', YearsOfStudy.as_view(), name='YearsOfStudy'),
    path('ApproveResults/<student>/<year_of_study>', ApproveResults.as_view(), name='ApproveResults'),
    path('StudentResults/<pk>', StudentResults.as_view(), name='StudentResults'),
    path('GenerateProvisionalTranscripts/', GenerateProvisionalTranscripts.as_view(), name='GenerateProvisionalTranscripts'),
]
