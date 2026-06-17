from django.shortcuts import render
from django.http import JsonResponse
from .models import Post

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'broadcast/index.html', {'posts': posts})

def live_viewer(request):
    # Fetching all posts
    posts = Post.objects.all().order_by('-created_at')
    
    # DEBUG: This will print to your terminal window. 
    # Check your VS Code terminal when you refresh the page.
    for post in posts:
        if post.image:
            print(f"DEBUG: Post '{post.title}' - Image Name: {post.image.name} - Full Path: {post.image.path}")
        else:
            print(f"DEBUG: Post '{post.title}' has NO image attached.")
        
    return render(request, 'broadcast/viewer.html', {'posts': posts})

def start_stream(request):
    return JsonResponse({'status': 'Streaming logic triggered'})

def stop_stream(request):
    return JsonResponse({'status': 'Streaming stopped'})