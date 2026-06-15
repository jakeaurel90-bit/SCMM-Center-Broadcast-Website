from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def index(request):
    # Fetch posts, ordered by newest first
    posts = Post.objects.all().order_by('-created_at')
    
    # Updated to match your folder structure: templates/broadcast/index.html
    return render(request, 'broadcast/index.html', {'posts': posts})

def live_viewer(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Assuming viewer.html is also inside templates/broadcast/
    return render(request, 'broadcast/viewer.html', {'posts': posts})

def start_stream(request):
    return JsonResponse({'status': 'Streaming logic triggered'})

def stop_stream(request):
    return JsonResponse({'status': 'Streaming stopped'})