
from django.urls import path , include
from job import views;
urlpatterns = [
    path('add/', views.add_job, name='add_job'),
    path('jobs',views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path("search/", views.search_skills, name="search_skills"), 
    path('job_analysis/<int:job_id>/', views.job_analysis, name='job_analysis'),

]