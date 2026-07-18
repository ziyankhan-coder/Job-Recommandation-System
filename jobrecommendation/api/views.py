from django.shortcuts import render
# Create your views here.
import google.generativeai as genai
from rest_framework.decorators import api_view, permission_classes # Yahan permission_classes add kiya
from rest_framework.permissions import AllowAny # Ye import karo taaki bina login ke chal sake
from rest_framework.response import Response
import PyPDF2
import json
import environ
# Views.py mein change karo:
env = environ.Env()
# .strip() lagane se extra blank spaces ya string error saaf ho jayenge
genai.configure(api_key=env('GEMINI_API_KEY').strip())

@api_view(['POST'])
@permission_classes([AllowAny]) # @login_required hata kar ye line laga do!
def analyze_resume(request):
    if 'pdf' not in request.FILES:
        return Response({"error": "No PDF provided"}, status=400)
        
    pdf_file = request.FILES['pdf']
    
    # 1. Extract text from the PDF
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        return Response({"error": f"Failed to read PDF: {str(e)}"}, status=400)
        
    # 2. Configure the Gemini Model
    model = genai.GenerativeModel('gemini-2.5-flash') 
    
    # 3. Prompt the AI to return strict JSON matching your frontend
    prompt = f"""
    Act as an expert recruiter and ATS software. Analyze this resume text. 
    Provide JSON output exactly matching this structure, with no markdown formatting. Do not include ```json tags.
    {{
      "personalDetails": {{
        "name": "Extracted Full Name",
        "email": "Extracted Email",
        "education": "Highest degree / major",
        "topSkills": ["Skill 1", "Skill 2", "Skill 3"]
      }},
      "score": 88,
      "atsScore": 92,
      "radarData": [
        {{ "subject": "Frontend", "A": 90, "fullMark": 100 }},
        {{ "subject": "Backend", "A": 40, "fullMark": 100 }},
        {{ "subject": "Design", "A": 70, "fullMark": 100 }},
        {{ "subject": "Leadership", "A": 80, "fullMark": 100 }},
        {{ "subject": "Communication", "A": 85, "fullMark": 100 }}
      ],
      "keywordsFound": ["React", "JavaScript", "Agile"],
      "keywordsMissing": ["Docker", "AWS", "Node.js"],
      "strengths": ["...", "..."],
      "weaknesses": ["..."],
      "recommendations": ["..."]
    }}
    
    Resume Text:
    {text}
    """
    
    # 4. Generate Content
    try:
        response = model.generate_content(prompt)
        response_text = response.text
        
        # Clean up in case Gemini returns markdown tags
        if response_text.startswith("```json"):
            response_text = response_text.replace("```json", "").replace("```", "").strip()
        elif response_text.startswith("```"): # Safe side ke liye agar normal markdown ho
            response_text = response_text.replace("```", "").strip()
            
        parsed_data = json.loads(response_text)
        return Response(parsed_data)
    except json.JSONDecodeError:
        return Response({"error": "Failed to parse AI response. Try again."}, status=500)
    except Exception as e:
        return Response({"error": str(e)}, status=500)