from django.urls import path

from Finance.views import *

urlpatterns = [
    path('Dashboard/', Dashboard.as_view(), name='FinanceDashboard'),
    path('CreateProfile/', CreateProfile.as_view(), name='FinanceCreateProfile'),
    path('SaveProfile/', SaveProfile.as_view(), name='FinanceSaveProfile'),
    path('UpdateProfile/', UpdateProfile.as_view(), name='FinanceUpdateProfile'),
    path('Departments/', Departments.as_view(), name='FinanceListDepartments'),
    path('CreateFeeStructure/<department>/', CreateFeeStructure.as_view(), name='CreateFeeStructure'),
    path('SubmitFeeStructure/', SubmitFeeStructure.as_view(), name='SubmitFeeStructure'),
    path('FetchData/', FetchData.as_view(), name='FetchData'),
    path('ListFeeStructures/', ListFeeStructures.as_view(), name='ListFeeStructures'),
]
