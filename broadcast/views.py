from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def index(request):
    # Fetch all posts from the database, ordered by newest first
    posts = Post.objects.all().order_by('-created_at')
    # Pass the posts to the template
    return render(request, 'index.html', {'posts': posts})

def live_viewer(request):
    # Fetch posts specifically for the public viewer
    posts = Post.objects.all().order_by('-created_at')
    # Render the new viewer.html template
    return render(request, 'viewer.html', {'posts': posts})

def start_stream(request):
    # Add your actual streaming start logic here
    return JsonResponse({'status': 'success'})

def stop_stream(request):
    # Add your actual streaming stop logic here
    return JsonResponse({'status': 'success'})