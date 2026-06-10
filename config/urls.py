from django.urls import path
from broadcast import views

urlpatterns = [
    # Admin path removed to prevent E403 error
    path('', views.public_view, name='public'),
    path('dashboard/', views.dashboard, name='dashboard'),
]