from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Headline")
    content = models.TextField(verbose_name="Announcement Content")
    image = models.ImageField(
        upload_to='post_images/', 
        blank=True, 
        null=True,
        help_text="Upload an image to display with the announcement."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Published Date")
    updated_at = models.DateTimeField(auto_now=True) # Tracks changes

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __str__(self):
        return self.title

class Comment(models.Model):
    # 'related_name' allows you to access comments from a post via post.comments.all()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80, verbose_name="Your Name")
    body = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'