from urllib import request

from django.shortcuts import render
from account.models import Company, UserProfile
from job.models import Job, JobApplication
# from .utils import predict_job, calculate_match
import joblib
from scipy.sparse import hstack
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

def home(request):

    if request.user.is_authenticated:
        if request.user.user_type=='recruiter':
            return render(request, 'home.html', {'jobs': []})
        else:
            recommended = recommended_jobs(request)
            return render(request, 'home.html', {'jobs': recommended,'match_percent': 50})
    else:
        return render(request, 'home.html', {'jobs': []})

model = joblib.load("model/job_model.pkl")
vectorizer = joblib.load("model/vectorizer.pkl")
def predict_job(user_skills, job_req, match_score):
    text = user_skills + " " + job_req
    text_vector = vectorizer.transform([text])
    X = hstack((text_vector, [[match_score]]))
    prediction = model.predict(X)
    return prediction[0]


def calculate_match(user_skills, job_req):
    if not user_skills or not job_req:
        return 0
    user = set([s.strip() for s in user_skills.lower().split(",")])
    job = set([s.strip() for s in job_req.lower().split(",")])
    match = user & job
    return len(match) / len(job) if len(job) >       0 else 0

def recommended_jobs(request):
    profile= get_object_or_404(UserProfile, user=request.user)
    user_skills = profile.skills
    jobs = Job.objects.all()
    recommended = []
    for job in jobs:
        match_score = calculate_match(user_skills, job.required_skills)
        pred = predict_job(user_skills, job.required_skills, match_score)
        final_score = (match_score * 0.6) +(pred * 0.4)
        user_set = set([s.strip() for s in user_skills.lower().split(",")])
        job_set = set([s.strip() for s in job.required_skills.lower().split(",")])
        matched_skills = list(user_set & job_set)
        recommended.append({
            "job": job,
            "score": final_score,
            "match_score": match_score,
            "match_percentage": round(match_score * 100, 2),
            "matched_skills": matched_skills
        })
        recommended = sorted(recommended, key=lambda x: x['score'], reverse=True)
    
    return recommended[:3]
from django.shortcuts import render

def custom_404(request, exception):
    return render(request, '404.html', status=404)
