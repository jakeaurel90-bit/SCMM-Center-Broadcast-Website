from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # We use a string path instead of importing the class directly.
    # This prevents the ImportError during the build process.
    image = models.ImageField(
        upload_to='post_images/', 
        storage='cloudinary_storage.storage.MediaCloudStorage', 
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title