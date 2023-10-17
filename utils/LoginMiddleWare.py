from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user
        if user.is_authenticated:
            if user.usertype == "ADMIN":
                if modulename == "Admin.Views" or modulename == "User.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("AdminDashboard"))
            elif user.usertype == "DEAN":
                if modulename == "Dean.Views":
                    pass
                elif modulename == "Dean.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("DeanDashBoard"))
            elif user.usertype == "HOD":
                if modulename == "Head_of_department.Views":
                    pass
                elif modulename == "Head_of_department.Views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("HODDashboard"))
            elif user.usertype == "LECTURER":
                if modulename == "Lecturer.Views":
                    pass
                elif modulename == "Lecturer.Views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("LECDashboard"))
            elif user.usertype == "STUDENT":
                if modulename == "Student.Views":
                    pass
                elif modulename == "Student.Views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("STDDashboard"))
            else:
                return HttpResponseRedirect(reverse("login"))

        else:
            if request.path == reverse("logout"):
                pass
            else:
                return HttpResponseRedirect(reverse("logout"))
