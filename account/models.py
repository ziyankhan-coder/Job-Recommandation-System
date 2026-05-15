from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
Role_choice = (('jobseeker','Jobseeker'),('recruiter','Recruiter'))
class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=Role_choice)

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # email = models.EmailField()   # 🔥 important
    # phone = models.CharField(max_length=15, blank=True)
    resume = models.FileField(upload_to="resumes/", null=True, blank=True)
    skills = models.TextField(max_length=100
    )
    experience_years = models.FloatField(default=0)
    preferred_location = models.CharField(max_length=255, blank=True)
    preferred_job_type = models.CharField(
        max_length=50,
        choices=[
            ('full_time', 'Full Time'),
            ('part_time', 'Part Time'),
            ('remote', 'Remote'),
        ],
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    education = models.CharField(max_length=200)
    
    role=models.CharField(max_length=20, choices=Role_choice)
    def __str__(self):
         return self.user.username
    
class Company(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # email = models.EmailField()   # 🔥 important
    # phone = models.CharField(max_length=15, blank=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100)
    company_size = models.CharField(
        max_length=50,
        choices=[
            ('startup', 'Startup'),
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large'),
        ]
    )
    location = models.CharField(max_length=255)
    founded_year = models.PositiveIntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    role=models.CharField(max_length=20, choices=Role_choice)

    def __str__(self):
        return self.name
# Create your models here.
