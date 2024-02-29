import logging

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user
from User.models import UserActivity


class UserActivityMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if get_user(request).is_anonymous:
            pass
        else:
            path = request.path
            method = request.method
            user = request.user

            UserActivity.objects.create(user=user, action=f"{method} - {path}")

    def process_exception(self, request, exception):
        if get_user(request).is_anonymous:
            pass
        else:
            path = request.path
            method = request.method
            user = request.user
            error = str(exception)

            UserActivity.objects.create(user=user, action=f"{method} - {path}", error=error)

