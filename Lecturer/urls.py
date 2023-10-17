from django.urls import path, include

from Lecturer.views import *

urlpatterns = [
    path('Dashboard', Dashboard.as_view(), name='LECDashboard'),
    path('CreateProfile', CreateProfile.as_view(), name='LECCreateProfile'),
    path('SaveProfile', SaveProfile.as_view(), name='LECSaveProfile'),
    path('UpdateProfile', UpdateProfile.as_view(), name='LECUpdateProfile'),
    path('Units', Units.as_view(), name='LECUnits'),
    path('Appraisal', Appraisal.as_view(), name='LECAppraisal'),
    path('Leaves', Leaves.as_view(), name='LECLeaves'),
    path('UnitApplication', UnitApplication.as_view(), name='LECUnitApplication'),
    path('RequestLeave', RequestLeave.as_view(), name='LECRequestLeave'),
    path('SubmitApplication', SubmitApplication.as_view(), name='LECSubmitApplication'),
    path('UploadResults/<pk>/', UploadResults.as_view(), name='LECUploadResults'),
]
