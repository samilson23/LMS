"""
URL configuration for Core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.staticfiles.views import serve
from django.urls import path, include
from django.views.decorators.cache import cache_control, never_cache
from ckeditor_uploader import views as ckeditor_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('User.urls')),
    path('Admin/', include('Admin.urls')),
    path('Dean/', include('Dean.urls')),
    path('HOD/', include('Head_of_department.urls')),
    path('Faculty/', include('Faculty.urls')),
    path('Lecturer/', include('Lecturer.urls')),
    path('Finance/', include('Finance.urls')),
    path('Student/', include('Student.urls')),
    path('Pespal/', include('django_pesapal.urls'), name='pesapal'),
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, view=cache_control(no_cache=True, must_revalidate=True)(serve))
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, view=cache_control(no_cache=True, must_revalidate=True)(serve))
