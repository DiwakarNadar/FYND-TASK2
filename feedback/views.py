import os, requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Submission
from .serializers import SubmissionSerializer
from django.shortcuts import render
from django.db import models as djmodels
from django.http import HttpResponse
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_MODEL = os.getenv('OPENROUTER_MODEL', 'meta-llama/llama-3.1-70b-instruct')


def debug_env(request):
    return HttpResponse("OPENROUTER_API_KEY = " + str(os.getenv("OPENROUTER_API_KEY")))

def call_openrouter(prompt):
    url = 'https://openrouter.ai/api/v1/chat/completions'
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }
    body = {
        'model': OPENROUTER_MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.0
    }
    try:
        r = requests.post(url, json=body, headers=headers, timeout=30)
        r.raise_for_status()
        data = r.json()
        return data['choices'][0]['message']['content']
    except Exception as e:
        return f'LLM Error: {e}'

@api_view(['POST'])
def submit_review(request):
    rating = request.data.get('rating')
    review = request.data.get('review')
    if rating is None or not review:
        return Response({'error': 'rating & review required'}, status=400)
    s = Submission.objects.create(user_rating=rating, user_review=review)
    # generate AI outputs
    user_prompt = f"Write a friendly 1-2 sentence reply to the customer reviewing: '{review}'. Rating: {rating}."
    summary_prompt = f"Summarize this review in one short sentence: {review}"
    action_prompt = f"Suggest 2 concise actions for the business based on this review: {review}"
    s.ai_response = call_openrouter(user_prompt)
    s.ai_summary = call_openrouter(summary_prompt)
    s.ai_actions = call_openrouter(action_prompt)
    s.save()
    return Response(SubmissionSerializer(s).data)

@api_view(['GET'])
def get_submissions(request):
    subs = Submission.objects.all().order_by('-created_at')
    return Response(SubmissionSerializer(subs, many=True).data)

def user_dashboard(request):
    ai_response = None
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        review = request.POST.get('review')
        payload = {'rating': rating, 'review': review}
        # call internal API endpoint
        from rest_framework.test import APIClient
        client = APIClient()
        resp = client.post('/api/submit/', payload, format='json')
        if resp.status_code == 200:
            data = resp.data
            ai_response = data.get('ai_response')
    return render(request, 'user_dashboard.html', {'ai_response': ai_response})

def admin_dashboard(request):
    subs = Submission.objects.all().order_by('-created_at')
    total = subs.count()
    avg = subs.aggregate(djmodels.Avg('user_rating'))['user_rating__avg'] or 0
    return render(request, 'admin_dashboard.html', {'submissions': subs, 'total': total, 'avg_rating': avg})
