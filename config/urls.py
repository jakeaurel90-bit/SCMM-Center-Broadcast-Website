from django.contrib import admin
from django.urls import path, include 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Path for your app
    path('', include('broadcast.urls')), 
]

# This block is the "gatekeeper" for media files.
# If DEBUG is False (Production), Django will NOT serve media files.
# If DEBUG is True (Development), this ensures your images render.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)