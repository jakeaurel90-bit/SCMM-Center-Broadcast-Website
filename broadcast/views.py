from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from obswebsocket import obsws, requests
import os

# Your view functions must have these exact names
def public_viewer_page(request):
    return render(request, 'broadcast/public.html')

@login_required
def index(request):
    return render(request, 'broadcast/index.html')

@login_required
def start_stream(request):
    # Logic for starting stream
    return JsonResponse({'status': 'success'})

@login_required
def stop_stream(request):
    # Logic for stopping stream
    return JsonResponse({'status': 'success'})