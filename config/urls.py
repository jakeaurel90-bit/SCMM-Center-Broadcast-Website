from django.urls import path
from broadcast import views

urlpatterns = [
    # Public viewer page
    path('', views.public_viewer_page, name='public'),
    
    # Dashboard and control
    path('dashboard/', views.index, name='dashboard'),
    
    # Post functionality
    path('add-post/', views.add_post, name='add_post'),
    
    # OBS Stream controls
    path('start-stream/', views.start_stream, name='start_stream'),
    path('stop-stream/', views.stop_stream, name='stop_stream'),
]