from django.urls import path
from django.contrib.auth import views as auth_views

from restaurant import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order_for_kitchen/', views.order_for_kitchen, name='order_for_kitchen'),
    path(r'get_order_sequence/',views.get_order_sequence),
    path(r'get_order_sequence2/',views.get_order_sequence2),
    path('driverManager/', views.driverManager, name='driverManager'),
    path('driverManager/<int:id>/delete/', views.driverDelete, name='drivers-delete'),
    path('dashboard/upload_done/', views.uploadDone, name='uploadDone'),
    path("order_history/", views.orderHistory, name="order_history"),
    path('contact_us/',views.contact_us,name='contact_us'),
    path('printable_routes',views.printable_routes,name='printable_routes'),
    path('driver_item_list/',views.driver_item_list,name='driver_item_list'),
    path('printable_driver_sequence/',views.printable_driver_sequence,name='printable_driver_sequence')
]