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
            return redirect('live_viewer')

    return render(request, 'broadcast/viewer.html', {'post': latest_post})

def edit_comment(request, comment_id):
    # Get the specific comment or return 404
    comment = get_object_or_404(Comment, id=comment_id)
    
    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.save()
        return redirect('live_viewer')
        
    return render(request, 'broadcast/edit_comment.html', {'comment': comment})

def delete_comment(request, comment_id):
    # Find the comment and remove it
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('live_viewer')

def start_stream(request):
    return JsonResponse({'status': 'Streaming logic triggered'})

def stop_stream(request):
    return JsonResponse({'status': 'Streaming stopped'})