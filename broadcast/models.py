from django.db import models
from cloudinary_storage.storage import MediaCloudStorage

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # By adding 'storage=MediaCloudStorage()', we force Django 
    # to send this image directly to Cloudinary, not the local server.
    image = models.ImageField(
        upload_to='post_images/', 
        storage=MediaCloudStorage(), 
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title