from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('live/', views.live_viewer, name='live_viewer'),
    path('start-stream/', views.start_stream, name='start_stream'),
    path('stop-stream/', views.stop_stream, name='stop_stream'),
]

# This allows Django to serve media files (images) during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)