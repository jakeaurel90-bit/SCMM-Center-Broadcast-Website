from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'posts': posts})

def live_viewer(request):
    # Fetch posts to show in the sidebar of the live page
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'viewer.html', {'posts': posts})

def start_stream(request):
    return JsonResponse({'status': 'Streaming logic triggered'})

def stop_stream(request):
    return JsonResponse({'status': 'Streaming stopped'})