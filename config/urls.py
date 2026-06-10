from django.urls import path
from broadcast import views

urlpatterns = [
    path('', views.public_viewer_page, name='public'),
    path('dashboard/', views.index, name='dashboard'),
    path('start-stream/', views.start_stream, name='start_stream'),
    path('stop-stream/', views.stop_stream, name='stop_stream'),
]