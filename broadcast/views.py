import os
from django.shortcuts import render
from django.http import JsonResponse
from obswebsocket import obsws, requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration pulled from environment variables
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

def index(request):
    return render(request, 'broadcast/index.html')

def start_stream(request):
    if not OBS_PASSWORD:
        return JsonResponse({'status': 'error', 'message': 'OBS configuration missing'}, status=500)
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        ws.call(requests.StartStream())
        ws.disconnect()
        return JsonResponse({'status': 'success', 'message': 'Stream started'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def stop_stream(request):
    if not OBS_PASSWORD:
        return JsonResponse({'status': 'error', 'message': 'OBS configuration missing'}, status=500)
    try:
        ws = obsws(OBS_HOST, OBS_PORT, OBS_PASSWORD)
        ws.connect()
        ws.call(requests.StopStream())
        ws.disconnect()
        return JsonResponse({'status': 'success', 'message': 'Stream stopped'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)