from django.urls import path
from . import views

urlpatterns = [
    # The home/dashboard page
    path('', views.index, name='index'),
    
    # The new public viewer page
    path('live/', views.live_viewer, name='live_viewer'),
    
    # Your streaming control paths
    path('start-stream/', views.start_stream, name='start_stream'),
    path('stop-stream/', views.stop_stream, name='stop_stream'),
]