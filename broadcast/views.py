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
        
        # If the request is from HTMX, re-render the partial so it updates 
        # instantly without a full page refresh/redirect
        if request.headers.get('HX-Request'):
            return render(request, 'broadcast/partials/post_update.html', {'post': latest_post})
            
        return redirect('live_viewer')

    # Standard HTMX update
    if request.headers.get('HX-Request'):
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