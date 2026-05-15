from django.contrib import admin
from django.urls import path;
from . import views

urlpatterns = [
path('login/',views.login_view, name='login'),
path('logout/',views.logout_view, name='logout'),
path('register/',views.register_view, name='register'),
path('register_user/',views.register_user, name='register_user'),
path('register_job/',views.register_company, name='register_job'),
]