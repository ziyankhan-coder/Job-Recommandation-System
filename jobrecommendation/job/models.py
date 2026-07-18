from django.db import models
from account.models import Company
from django.conf import settings
class Job(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE , related_name='jobs')
    title=models.CharField(max_length=100)
    description=models.TextField()
    location=models.CharField(max_length=255)
    salary=models.DecimalField(max_digits=10, decimal_places=2)
    required_skills=models.TextField()
    job_type=models.CharField(max_length=50,choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('internship', 'Internship'),
    ])
    created_at=models.DateTimeField(auto_now_add=True)
        
    def __str__(self):
        return self.company.name + " - " + self.title

# Create your models here.
class JobApplication(models.Model):
    job=models.ForeignKey(Job, on_delete=models.CASCADE , related_name='applications')
    apllicant_name=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='applications')
    appliad_at=models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('applied', 'Applied'),
            ('shortlisted', 'Shortlisted'),
            ('rejected', 'Rejected'),
        ],
        default='applied'
    )

    def __str__(self):
        return f"{self.apllicant_name} → {self.job.title}"
    