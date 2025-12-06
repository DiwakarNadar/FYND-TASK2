# Task2 Django Project (Feedback System)
This project contains a Django app `feedback` that implements:
- API endpoints for submitting reviews and listing submissions
- Simple user and admin dashboards as Django templates
- OpenRouter LLM integration for generating responses, summaries, and suggested actions

## Quickstart (local)
1. Create a virtualenv and install requirements: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill your OPENROUTER_API_KEY
3. Run migrations: `python manage.py migrate`
4. Run server: `python manage.py runserver`
5. Visit: http://localhost:8000/user/ and http://localhost:8000/admin_dashboard/

## Deploy
- Add environment variables in your host (OPENROUTER_API_KEY)
- Use gunicorn with Procfile for hosting providers like Render.
