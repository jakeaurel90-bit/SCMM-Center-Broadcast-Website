from django.contrib import admin
from django.urls import path, include  # 1. Import 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Tell Django to look into broadcast/urls.py for all other paths
    path('', include('broadcast.urls')), 
]