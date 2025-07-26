"""Medical_Recommendation_System_django_ml URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from medicalapp.views import *

from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('predict/', predict_medicine, name='predict_medicine'),
    path('admin_login/', admin_login, name='admin_login'),
    path('user_login/', user_login, name='user_login'),
    path('user_register/', user_register, name='user_register'),
    path('logout_admin/', logout_admin, name='logout_admin'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('password-change/', password_change, name='password_change'),
    path('reg-user/', reg_user, name='reg_user'),
    path('send-feed/', feed, name='feed'),
    path('feed-view/', feed_view, name='feed_view'),
    path('delete_feed/<int:pid>', delete_feed, name='delete_feed'),
    path('delete_reg/<int:pid>', delete_reg, name='delete_reg'),
    path('profile/', profile, name='profile'),
    path('predict_history/', predict_history, name='predict_history'),
    path('detail_predict/<int:pid>', detail_predict, name='detail_predict'),
    path('user_predict_view/<int:pid>', user_predict_view, name='user_predict_view'),
    path('delete_pridict/<int:pid>', delete_pridict, name='delete_pridict'),
    path('user_delete_pridict/<int:pid>', user_delete_pridict, name='user_delete_pridict'),
    path('delete_pridict_ma/<int:pid>', delete_pridict_ma, name='delete_pridict_ma'),
    path('pre_history/', pre_history, name='pre_history'),
    path('add_doctor/', add_doctor, name='add_doctor'),
    path('manage_doctor/', manage_doctor, name='manage_doctor'),
    path('edit_doctor/<int:pid>', edit_doctor, name='edit_doctor'),
    path('delete_doctor/<int:pid>', delete_doctor, name='delete_doctor'),
    path('doctor_detail/<int:pid>', doctor_detail, name='doctor_detail'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
