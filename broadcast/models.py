from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # The 'storage' argument is omitted so that Django uses 
    # the 'default' backend defined in the STORAGES dictionary 
    # in settings.py (Cloudinary).
    image = models.ImageField(
        upload_to='post_images/', 
        blank=True, 
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title