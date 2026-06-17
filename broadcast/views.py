from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment

def index(request):
    posts = Post.objects.all()
    return render(request, 'broadcast/index.html', {'posts': posts})

def live_viewer(request):
    # Fetch only the single most recent post
    latest_post = Post.objects.order_by('-created_at').first()
    
    # Handle Comment Submission
    if request.method == 'POST' and latest_post:
        name = request.POST.get('name')
        body = request.POST.get('body')
        if name and body:
            Comment.objects.create(post=latest_post, name=name, body=body)
            # Redirect to avoid form resubmission on refresh
            return redirect('live_viewer')

    return render(request, 'broadcast/viewer.html', {'post': latest_post})

def start_stream(request):
    return JsonResponse({'status': 'Streaming logic triggered'})

def stop_stream(request):
    return JsonResponse({'status': 'Streaming stopped'})