@REM @echo off
@REM echo Starting Django Backend...
@REM start cmd /k "cd jobrecommendation && python manage.py runserver"

@REM echo Starting React Frontend...
@REM start cmd /k "cd ai-resume-analyzer-frontend && npm run dev"

@REM echo Both servers are starting!
@echo off
echo Starting Django Backend...
:: Pehle virtual environment activate hoga, fir backend directory mein jaakar server chalega
start cmd /k "call env\Scripts\activate && cd jobrecommentation && python manage.py runserver"

echo Starting React Frontend...
:: Frontend directory mein jaakar vite/react development server chalega
start cmd /k "cd ai-resume-analyzer-frontend && npm run dev"

echo Both servers are starting!