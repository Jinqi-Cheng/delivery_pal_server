from django.urls import path
from django.contrib.auth import views as auth_views

from restaurant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order_for_kitchen/', views.order_for_kitchen, name='order_for_kitchen'),
]