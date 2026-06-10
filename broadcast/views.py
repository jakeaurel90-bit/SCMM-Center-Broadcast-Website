import os
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from obswebsocket import obsws, requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration pulled from environment variables
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

# Helper function to handle OBS connection
def get_obs_connection():
    if not OBS_PASSWORD:
        return None
    return obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)

# Public page for all viewers
def public_viewer_page(request):
    """
    Renders the public page where viewers watch the stream.
    """
    return render(request, 'broadcast/public.html')

# Protected dashboard for the broadcaster
@login_required
def index(request):
    """
    Renders the dashboard; accessible only by logged-in admins.
    """
    return render(request, 'broadcast/index.html')

# Protected stream control functions
@login_required
def start_stream(request):
    ws = get_obs_connection()
    if not ws:
        return JsonResponse({'status': 'error', 'message': 'OBS configuration missing'}, status=500)
    try:
        ws.connect()
        ws.call(requests.StartStream())
        ws.disconnect()
        return JsonResponse({'status': 'success', 'message': 'Stream started'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def stop_stream(request):
    ws = get_obs_connection()
    if not ws:
        return JsonResponse({'status': 'error', 'message': 'OBS configuration missing'}, status=500)
    try:
        ws.connect()
        ws.call(requests.StopStream())
        ws.disconnect()
        return JsonResponse({'status': 'success', 'message': 'Stream stopped'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)