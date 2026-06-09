"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include  # 1. Added 'include' here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('broadcast.urls')),  # 2. Added this line to link your app
]