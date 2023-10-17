from django.urls import path

from Head_of_department.views import *

urlpatterns = [
    path('Dashboard', Dashboard.as_view(), name='HODDashboard'),
    path('CreateProfile', CreateProfile.as_view(), name='HODCreateProfile'),
    path('SaveProfile', SaveProfile.as_view(), name='HODSaveProfile'),
    path('UpdateProfile', UpdateProfile.as_view(), name='HODUpdateProfile'),
    path('ListUnits', ListUnits.as_view(), name='HODListUnits'),
    path('ResultsManagement/<pk>', ResultsManagement.as_view(), name='HODResultsManagement'),
    path('ApproveDisapproveResults/<pk>', ApproveDisapproveResults.as_view(), name='HODApproveDisapproveResults'),
    path('RequestLeave', RequestLeave.as_view(), name='HODRequestLeave'),
    path('Appraisal', Appraisal.as_view(), name='HODAppraisal'),
    path('Leaves', Leaves.as_view(), name='HODLeaves'),
]
