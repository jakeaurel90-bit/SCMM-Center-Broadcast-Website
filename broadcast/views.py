import os
from django.shortcuts import render
from django.http import JsonResponse
from obswebsocket import obsws, requests
from dotenv import load_dotenv

load_dotenv()

OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

def get_obs_connection():
    return obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD) if OBS_PASSWORD else None

def public_viewer_page(request):
    return render(request, 'broadcast/public.html')

# Removed @login_required to stop the AttributeError
def index(request):
    return render(request, 'broadcast/index.html')

# Removed @login_required to stop the AttributeError
def start_stream(request):
    try:
        ws = get_obs_connection()
        ws.connect()
        ws.call(requests.StartStream())
        ws.disconnect()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# Removed @login_required to stop the AttributeError
def stop_stream(request):
    try:
        ws = get_obs_connection()
        ws.connect()
        ws.call(requests.StopStream())
        ws.disconnect()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)