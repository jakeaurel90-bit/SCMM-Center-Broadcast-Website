from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # We keep it simple. When you are ready to switch back to Cloudinary,
    # you do not need to change this line; the 'default' storage backend 
    # in settings.py handles the magic.
    image = models.ImageField(
        upload_to='post_images/', 
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # This ensures the newest posts appear at the top
        ordering = ['-created_at']

    def __str__(self):
        return self.title