import logging

from django.apps import apps
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, TemplateView

from User.forms.CreateUserAccount import CreateUserAccount
from User.forms.LoginForm import UserLoginForm
from User.forms.PasswordChangeForm import PasswordChange


db_logger = logging.getLogger('db')
User = get_user_model()


class MyLoginView(LoginView):
    template_name = 'account/login.html'
    authentication_form = UserLoginForm

    def form_valid(self, form):
        super().form_valid(form)
        if self.request.user.is_authenticated:
            db_logger.info(f'{self.request.user.username} signed in successfully')
            if self.request.user.usertype == 'ADMIN':
                if self.request.user.has_profile:
                    messages.success(self.request, f"Welcome back {self.request.user.first_name}  {self.request.user.last_name}")
                    return redirect('AdminDashboard')
                else:
                    messages.info(self.request, "Please Create your profile first")
                    return redirect('AdminCreateProfile')
            elif self.request.user.usertype == 'DEAN':
                if not self.request.user.has_perm('User.login'):
                    messages.info(self.request, f'Login for {self.request.user.usertype}S has been disabled for now')
                    return redirect('logout')
                else:
                    if self.request.user.has_profile:
                        messages.success(self.request, f"Welcome back {self.request.user.first_name}  {self.request.user.last_name}")
                        return redirect('DeanDashBoard')
                    else:
                        messages.info(self.request, "Please Create your profile first")
                        return redirect('DeanCreateProfile')
            elif self.request.user.usertype == 'HOD':
                if not self.request.user.has_perm('User.login'):
                    messages.info(self.request, f'Login for {self.request.user.usertype}S has been disabled for now')
                    return redirect('logout')
                else:
                    if self.request.user.has_profile:
                        messages.success(self.request, f"Welcome back {self.request.user.first_name}  {self.request.user.last_name}")
                        return redirect('HODDashboard')
                    else:
                        messages.info(self.request, "Please Create your profile first")
                        return redirect('HODCreateProfile')
            elif self.request.user.usertype == 'LECTURER':
                if not self.request.user.has_perm('User.login'):
                    messages.info(self.request, f'Login for {self.request.user.usertype}S has been disabled for now')
                    return redirect('logout')
                else:
                    if self.request.user.has_profile:
                        messages.success(self.request, f"Welcome back {self.request.user.first_name}  {self.request.user.last_name}")
                        return redirect('LECDashboard')
                    else:
                        messages.info(self.request, "Please Create your profile first")
                        return redirect('LECCreateProfile')
            elif self.request.user.usertype == 'STUDENT':
                if not self.request.user.has_perm('User.login'):
                    messages.info(self.request, f'Login for {self.request.user.usertype}S has been disabled for now')
                    return redirect('logout')
                else:
                    if self.request.user.has_profile:
                        messages.success(self.request, f"Welcome back {self.request.user.first_name}  {self.request.user.last_name}")
                        return redirect('STDDashboard')
                    else:
                        messages.info(self.request, "Please Create your profile first")
                        return redirect('STDCreateProfile')
            else:
                db_logger.warning(f'{self.request.user.username} does not have a role user assigned')
                messages.add_message(self.request, messages.ERROR, 'Role not assigned')
                return redirect('logout')

    def form_invalid(self, form):
        response = super().form_invalid(form)
        db_logger.error('Failed login attempt')
        messages.add_message(self.request, messages.ERROR, 'Invalid login credentials')
        return response


class Register(TemplateView):
    def get(self, request, *args, **kwargs):
        form = CreateUserAccount
        return render(self.request, 'account/register.html', {'form': form})


class CreateUser(CreateView):
    form_class = CreateUserAccount
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Registration successful')
        messages.add_message(self.request, messages.INFO, 'Contact system admin to have your account activated')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Registration unsuccessful')
        return super().form_invalid(form)


class PasswordsChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChange
    success_url = reverse_lazy('login')
    success_message = 'Password change successful'
    template_name = 'account/password-change.html'


class UpdateUser(LoginRequiredMixin, View):
    @staticmethod
    def post(request):
        try:
            _model = apps.get_model('User', request.POST['model'])
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
