from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Comment

def live_viewer(request):
    latest_post = Post.objects.order_by('-created_at').first()
    
    # 1. Handle Comment Submission (Triggered by the FORM)
    if request.method == 'POST' and latest_post:
        name = request.POST.get('name')
        body = request.POST.get('body')
        if name and body:
            Comment.objects.create(post=latest_post, name=name, body=body)
        # Returns ONLY the comment list fragment
        return render(request, 'broadcast/partials/comment_list.html', {'post': latest_post})

    # 2. Handle HTMX Polling (Triggered by the ANNOUNCEMENT div)
    # This specifically checks for the header we added to viewer.html
    if request.headers.get('X-HTMX-Polling') == 'true':
        return render(request, 'broadcast/partials/post_update.html', {'post': latest_post})

    # 3. Standard Load (Returns full page - no header present)
    return render(request, 'broadcast/viewer.html', {'post': latest_post})