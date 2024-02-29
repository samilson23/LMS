from django.urls import path

from User.views import *

urlpatterns = [
    path('', MyLoginView.as_view(), name='login'),
    path('Register/', Register.as_view(), name='Register'),
    path('CreateUser/', CreateUser.as_view(), name='SignUp'),
    path('UpdateUser/', UpdateUser.as_view(), name='UpdateUser'),
    path('logout/', SignOut.as_view(), name='logout'),
    path('password-change/',
         PasswordsChangeView.as_view(), name="password-change"),
]
