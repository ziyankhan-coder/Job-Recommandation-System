from django.shortcuts import render, redirect
from .models import User;
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request,'account/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

from .models import UserProfile, Company
def register_view(request):
    if request.method == 'POST':
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        # skills = request.POST.get('skills')
        # education = request.POST.get('education')
        # experience = request.POST.get('experience')
        role = request.POST.get('role')
        if role == 'jobseeker':
            return redirect('register_user')
        elif role == 'recruiter':
            return redirect('register_job')
        return render(request,'account/register.html')

        # if User.objects.filter(username=username).exists():
        #     messages.error(request, 'Username already exists')
        #     return redirect('register')

        # user = User.objects.create_user(username=username, password=password)
        # profile = UserProfile(user=user, skills=skills, education=education, experience=experience,role=role)
        # profile.save()
        # user.save()

        # messages.success(request, 'Registration successful')
        # return redirect('login')
    return render(request,'account/register.html')

# Create your views here.
def register_user(request):
    if request.method == 'POST':
     username = request.POST.get('username')
     password = request.POST.get('password')
    #  email = request.POST.get('email')
    #  phone = request.POST.get('phone')
     confirm_password = request.POST.get('confirm_password')    
     skills_list = request.POST.getlist('skills')
     skills = ','.join(skills_list)  # Convert list to comma-separated string
     education = request.POST.get('education')
     experience_years = request.POST.get('experience')
     preferred_location = request.POST.get('preferred_location')
     preferred_job_type = request.POST.get('preferred_job_type')
   
     if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register_user')
     elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('register_user')
     user = User.objects.create_user(username=username, password=password, user_type="jobseeker")
     profile = UserProfile(user=user, skills=skills, education=education, experience_years=experience_years,role="jobseeker", preferred_location=preferred_location, preferred_job_type=preferred_job_type)
     profile.save()
     user.save()
     print(skills,type(skills))
     messages.success(request, 'Registration successful')
     return redirect('login')
    return render(request,'account/register_jobseeker.html')

def register_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password, user_type="recruiter")
        # email=request.POST.get('email')
        # phone=request.POST.get('phone')
        name=request.POST.get('name')
        description=request.POST.get('description')
        website=request.POST.get('website')
        industry=request.POST.get('industry')
        company_size=request.POST.get('company_size')
        location=request.POST.get('location')
        founded_year=request.POST.get('founded_year')
        company=Company(user=user,name=name,description=description,website=website,industry=industry,company_size=company_size,location=location,founded_year=founded_year,role="recruiter")
        company.save()
        user.save()
        return redirect('login')
    return render(request,'account/register_company.html')