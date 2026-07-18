import os
import joblib
import numpy as np
from pathlib import Path
from scipy.sparse import hstack

from django.shortcuts import render, get_object_or_404
from account.models import Company, UserProfile
from job.models import Job, JobApplication

# Dynamic Directory Setup
VIEWS_DIR = Path(__file__).resolve().parent
BASE_DIR = VIEWS_DIR.parent

model_path = os.path.join(BASE_DIR, 'model', 'job_model.pkl')
vectorizer_path = os.path.join(BASE_DIR, 'model', 'vectorizer.pkl')

# Safe Globals Global Context
model = None
vectorizer = None

try:
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    print("[SUCCESS] Upgraded Random Forest & TF-IDF Model loaded into Django!")
except Exception as e:
    print(f"🚨 [CRITICAL ERROR] Upgraded model files missing or corrupted: {e}")

# ========================================================
# REFACTORED INFERENCE ENGINE
# ========================================================

def predict_job(user_skills, job_req, match_score):
    if model is None or vectorizer is None:
        return 0
    try:
        text = str(user_skills) + " " + str(job_req)
        # Transform using the upgraded TF-IDF instance
        text_vector = vectorizer.transform([text])
        X = hstack((text_vector, [[match_score]]))
        
        # Random Forest classification call
        prediction = model.predict(X)
        return int(prediction[0])
    except Exception as e:
        print(f"Inference Error: {e}")
        return 0

def calculate_match(user_skills, job_req):
    if not user_skills or not job_req:
        return 0
    user = set([s.strip().lower() for s in str(user_skills).split(",") if s.strip()])
    job = set([s.strip().lower() for s in str(job_req).split(",") if s.strip()])
    if not job:
        return 0
    match = user & job
    return len(match) / len(job)

def recommended_jobs(request):
    try:
        profile = get_object_or_404(UserProfile, user=request.user)
    except Exception:
        print("UserProfile reference not found.")
        return []

    user_skills = profile.skills if profile.skills else ""
    jobs = Job.objects.all()
    recommended_list = []
    
    user_set = set([s.strip().lower() for s in str(user_skills).split(",") if s.strip()])

    for job in jobs:
        job_skills = job.required_skills if job.required_skills else ""
        
        match_score = calculate_match(user_skills, job_skills)
        pred = predict_job(user_skills, job_skills, match_score)
        
        # Final blended logic score weightage mapping
        final_score = (match_score * 0.6) + (pred * 0.4)
        
        job_set = set([s.strip().lower() for s in str(job_skills).split(",") if s.strip()])
        matched_skills = list(user_set & job_set)
        
        recommended_list.append({
            "job": job,
            "score": final_score,
            "match_score": match_score,
            "match_percentage": round(match_score * 100, 2),
            "matched_skills": matched_skills
        })
    
    # Sort from highest matrix output rating context to lowest
    recommended_list = sorted(recommended_list, key=lambda x: x['score'], reverse=True)
    return recommended_list[:3]


def home(request):
    try:
        if request.user.is_authenticated:
            user_type = getattr(request.user, 'user_type', None)
            if user_type == 'recruiter':
                return render(request, 'home.html', {'jobs': []})
            else:
                jobs = recommended_jobs(request)
                return render(request, 'home.html', {'jobs': jobs})
        else:
            return render(request, 'home.html', {'jobs': []})
    except Exception as e:
        print(f"🚨 View Execution Failure: {e}")
        return render(request, 'home.html', {'jobs': [], 'error': 'Takneeki kharabi.'})

def custom_404(request, exception):
    return render(request, '404.html', status=404)