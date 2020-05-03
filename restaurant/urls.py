from django.urls import path
from django.contrib.auth import views as auth_views

from restaurant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('driverManager/', views.driverManager, name='driverManager'),
    path('driverManager/<int:id>/delete/', views.driverDelete, name='drivers-delete'),
]