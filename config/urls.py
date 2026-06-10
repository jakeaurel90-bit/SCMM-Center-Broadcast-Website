"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path
from broadcast import views  # Import your views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Public-facing viewer page
    path('', views.public_viewer_page, name='public'),
    
    # Protected dashboard for controls
    path('dashboard/', views.index, name='index'),
    
    # Paths for your API controls (Start/Stop)
    path('start-stream/', views.start_stream, name='start_stream'),
    path('stop-stream/', views.stop_stream, name='stop_stream'),
]