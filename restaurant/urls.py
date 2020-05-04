from django.urls import path
from django.contrib.auth import views as auth_views

from restaurant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order_for_kitchen/', views.order_for_kitchen, name='order_for_kitchen'),
    path(r'get_order_sequence/',views.get_order_sequence),
    path('driverManager/', views.driverManager, name='driverManager'),
    path('driverManager/<int:id>/delete/', views.driverDelete, name='drivers-delete'),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('printable_routes',views.printable_routes,name='printable_routes')
]