from django.shortcuts import render , get_object_or_404 , redirect;
from django.http import HttpResponse
from account.models import Company , User , UserProfile
from .models import Job , JobApplication
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import random
from django.contrib.auth import get_user_model
from django.http import JsonResponse
@login_required
def add_job(request):
    if(request.method == 'POST'):
        # Logic to handle job addition
        user=Company.objects.get(user=request.user)
        
        title=request.POST.get('title')
        description=request.POST.get('description')
        location=request.POST.get('location')
        salary=request.POST.get('salary')
        skills_list = request.POST.getlist('skills')
        required_skills = ','.join(skills_list)
        job_type=request.POST.get('job_type')
        
        

        Job.objects.create(company=user, title=title, description=description, location=location, salary=salary,required_skills=required_skills, job_type=job_type)
        return render(request, 'home.html')
    return render(request, 'job/add_job.html')

def job_list(request):
    jobs = Job.objects.all()
    q = request.GET.get('q')
    location = request.GET.get('location')
    min_salary = request.GET.get('min_salary')
    

    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) 
        )

    if location:
        jobs = jobs.filter(location__icontains=location)

    if min_salary:
        jobs = jobs.filter(salary__gte=min_salary)
    


    return render(request, 'job/job_list.html', {'jobs': jobs})

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    apply_status= JobApplication.objects.filter(job=job, apllicant_name=request.user).exists()
    if(apply_status==False):
        JobApplication.objects.create(job=job, apllicant_name=request.user)
        messages.success(request, 'You have successfully applied for the job.')
        return redirect('job_list') 
    else:
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_list')

#for autocomplete search
def search_skills(request):
    query = request.GET.get("q", "").lower()

    profiles = UserProfile.objects.filter(
        skills__icontains=query
    ).values_list("skills", flat=True)

    skill_set = set()

    for skills in profiles:
        for skill in skills.split(","):
            skill = skill.strip()
            if query in skill.lower():
                skill_set.add(skill)

    return JsonResponse(list(skill_set)[:10], safe=False)

def job_analysis(request, job_id):

    job = get_object_or_404(Job, id=job_id)
    applications = JobApplication.objects.filter(job=job)
    total_applications = applications.count()   
    shortlisted_count = applications.filter(status='shortlisted').count()
    rejected_count = applications.filter(status='rejected').count()
    Company = job.company
    title = job.title
    description = job.description
    location = job.location
    salary = job.salary
    posted_at = job.created_at
    job_skills= set(job.required_skills.split(','))
    #default value
    user_skills = set()
    matched_skills = set()
    match_percentage = 0
    if request.user.user_type=="jobseeker":
        user = get_object_or_404(UserProfile, user=request.user.id)
        # Convert both to sets
        user_skills = set(user.skills.split(','))
        # Find matches
        matched_skills = user_skills.intersection(job_skills)
        # Calculate percentage
        if len(job_skills) > 0:
            match_percentage = round((len(matched_skills) / len(job_skills)) * 100, 2)
        else:
            match_percentage = 0


    analysis_data = {
        'job': job,
        'total_applications': total_applications,
        'shortlisted_count': shortlisted_count,
        'rejected_count': rejected_count,
        'company': Company,
        'title': title,
        'description': description,
        'location': location,
        'salary': salary,
        'posted_at': posted_at,
        'required_skills':job_skills,
        'user_skills':user_skills,

        "match_percentage": match_percentage,
        "matched_count": len(matched_skills),
        "total_required": len(job_skills),
        "matched_skills": matched_skills,
        "missing_skills": job_skills - matched_skills,
    }
    
    
    return render(request, 'job/job_analysis.html', analysis_data)

