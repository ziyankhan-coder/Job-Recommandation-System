import os
import json
import google.generativeai as genai
import PyPDF2
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# API Key setup
api_key = os.environ.get('GEMINI_API_KEY', '').strip()
if api_key:
    genai.configure(api_key=api_key)

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_resume(request):
    if 'pdf' not in request.FILES:
        return Response({"error": "No PDF provided"}, status=400)

    pdf_file = request.FILES['pdf']

    # 1. PDF Text Extraction
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t
    except Exception as e:
        return Response({"error": f"PDF parse error: {str(e)}"}, status=400)

    if not text.strip():
        return Response({"error": "Could not extract text from PDF"}, status=400)

    # 2. Gemini Analysis
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Act as an expert recruiter and ATS software. Analyze this resume text:
        {text[:4000]}

        Return ONLY a raw JSON object (no markdown formatting, no ```json tags) with these exact keys:
        {{
            "score": 85,
            "atsScore": 80,
            "personalDetails": {{
                "name": "Candidate Name",
                "education": "Degree Details",
                "topSkills": ["Skill 1", "Skill 2", "Skill 3"]
            }},
            "radarData": [
                {{"subject": "Technical", "A": 85}},
                {{"subject": "Communication", "A": 75}},
                {{"subject": "Problem Solving", "A": 90}},
                {{"subject": "Experience", "A": 70}},
                {{"subject": "Leadership", "A": 65}}
            ],
            "keywordsFound": ["Python", "Django"],
            "keywordsMissing": ["Docker", "AWS"],
            "strengths": ["Clear layout", "Strong technical background"],
            "weaknesses": ["Needs more project metrics"],
            "recommendations": ["Add quantifiable impact in bullets"]
        }}
        """
        response = model.generate_content(prompt)
        cleaned_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(cleaned_text)
        return Response(data)
    except Exception as e:
        return Response({"error": f"AI Generation error: {str(e)}"}, status=500)