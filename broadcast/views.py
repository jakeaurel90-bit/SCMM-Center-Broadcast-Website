from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment

def index(request):
    posts = Post.objects.all()
    return render(request, 'broadcast/index.html', {'posts': posts})

def live_viewer(request):
    latest_post = Post.objects.order_by('-created_at').first()
    
    # Handle Comment Submission
    if request.method == 'POST' and latest_post:
        name = request.POST.get('name')
        body = request.POST.get('body')
        if name and body:
            Comment.objects.create(post=latest_post, name=name, body=body)
        
        # After posting, return only the COMMENT LIST partial
        # so the form stays visible and the page doesn't jump
        return render(request, 'broadcast/partials/comment_list.html', {'post': latest_post})

    # Standard HTMX update for the Announcement Polling
    # Triggered by the 5s interval on #announcement-content
    if request.headers.get('HX-Trigger') == 'announcement-poll':
        return render(request, 'broadcast/partials/post_update.html', {'post': latest_post})

    # Standard Load: Return the full page
    return render(request, 'broadcast/viewer.html', {'post': latest_post})

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.body = request.POST.get('body')
        comment.save()
        return redirect('live_viewer')
    return render(request, 'broadcast/edit_comment.html', {'comment': comment})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('live_viewer')

def start_stream(request):
    return JsonResponse({'status': 'Streaming logic triggered'})

def stop_stream(request):
    return JsonResponse({'status': 'Streaming stopped'})