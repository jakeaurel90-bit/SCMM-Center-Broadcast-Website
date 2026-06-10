import os
from django.shortcuts import render, redirect
from django.http import JsonResponse
from obswebsocket import obsws, requests
from dotenv import load_dotenv
from .models import Post  # Ensure you have models.py set up

load_dotenv()

OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

def get_obs_connection():
    return obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD) if OBS_PASSWORD else None

# --- Viewer/Public Section ---
def public_viewer_page(request):
    """Fetches all posts to display to viewers."""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'broadcast/public.html', {'posts': posts})

# --- Dashboard Section ---
def index(request):
    """Renders the dashboard and lists existing posts."""
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'broadcast/index.html', {'posts': posts})

def add_post(request):
    """Saves a new announcement from the dashboard."""
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Post.objects.create(content=content)
    return redirect('dashboard')

# --- OBS Control Section ---
def start_stream(request):
    try:
        ws = get_obs_connection()
        ws.connect()
        ws.call(requests.StartStream())
        ws.disconnect()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def stop_stream(request):
    try:
        ws = get_obs_connection()
        ws.connect()
        ws.call(requests.StopStream())
        ws.disconnect()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)