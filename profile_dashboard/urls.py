from django.contrib import admin
from django.urls import path , include
from profile_dashboard import views;
urlpatterns = [
    path('profile', views.profile, name='profile'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('status_analysis/<int:job_id>/', views.status_analysis, name='status_analysis'),
    path('applicant_detail/<int:applicant_id>/', views.applicant_detail, name='applicant_detail'),
    
]