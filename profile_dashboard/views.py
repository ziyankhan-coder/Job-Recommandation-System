from django.shortcuts import render
from account.models import UserProfile, Company;
from job.models import Job, JobApplication
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
def profile(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'jobseeker':
            profile = get_object_or_404(UserProfile, user=request.user)
            profile_info = {
                'skills': profile.skills.split(','),
                'experience_years': profile.experience_years,
                'preferred_location': profile.preferred_location,
                'preferred_job_type': profile.preferred_job_type,
                'education': profile.education,
                'role': profile.role
            }
            return render(request, 'profile_dashboard/profile.html', profile_info)
        elif request.user.user_type == 'recruiter':
            company = get_object_or_404(Company, user=request.user)
            jobs_posted = Job.objects.filter(company=company)
            profile_info = {
                'company_name': company.name,
                'company_description': company.description,
                'company_website': company.website,
                'industry': company.industry,
                'company_size': company.company_size,
                'location': company.location,
                'founded_year': company.founded_year,
                'role': company.role,
                'jobs_posted': jobs_posted
            }
            return render(request, 'profile_dashboard/profile.html', profile_info)
def status_analysis(request, job_id):
    if request.GET.get('status')!= None:
        application_id = request.GET.get('applicant_id')
        new_status = request.GET.get('status')
        application = get_object_or_404(JobApplication, job=job_id, apllicant_name=application_id)
        application.status = new_status
        application.save()

    job = Job.objects.get(id=job_id)
    applications = JobApplication.objects.filter(job=job)
    total_applications = applications.count()
    shortlisted_count = applications.filter(status='shortlisted').count()
    rejected_count = applications.filter(status='rejected').count()
    appllicant_name=[ app.apllicant_name for app in applications]
    


    analysis_data = {
        'job': job,
        'total_applications': total_applications,
        'shortlisted_count': shortlisted_count,
        'rejected_count': rejected_count,
        'appllicant_name': appllicant_name, 
    }

    return render(request, 'profile_dashboard/status_analysis.html', analysis_data)
# Create your views here.
def applicant_detail(request, applicant_id):
    application = get_object_or_404(UserProfile, user=applicant_id)
    applicant = application.user
    applicant_skills = application.skills

    applicant_data = {
        'applicant': applicant,
        'applicant_skills': applicant_skills
    }

    return render(request, 'profile_dashboard/applicant_detail.html', applicant_data)
def update_profile(request):
    if request.user.user_type == 'jobseeker':
        profile = get_object_or_404(UserProfile, user=request.user)
    elif request.user.user_type == 'recruiter':
        company = get_object_or_404(Company, user=request.user)

    if request.method == 'POST':
        if request.user.user_type == 'jobseeker':
            profile.skills = request.POST.get('skills')
            profile.experience_years = request.POST.get('experience_years')
            profile.preferred_location = request.POST.get('preferred_location')
            profile.preferred_job_type = request.POST.get('preferred_job_type')
            profile.education = request.POST.get('education')
            profile.role = request.POST.get('role')
            profile.save()

        elif request.user.user_type == 'recruiter':
            company.name = request.POST.get('company_name')
            company.description = request.POST.get('company_description')
            company.website = request.POST.get('company_website')
            company.industry = request.POST.get('industry')
            company.company_size = request.POST.get('company_size')
            company.location = request.POST.get('location')
            company.founded_year = request.POST.get('founded_year')
            company.role = request.POST.get('role')
            company.save()

    context = {
        'profile': profile if request.user.user_type == 'jobseeker' else None,
        'company': company if request.user.user_type == 'recruiter' else None
    }

    return render(request, 'profile_dashboard/update_profile.html', context)