from django.contrib import admin

# Register your models here.
from .models import Orders, Drivers

class OrderAdmin(admin.ModelAdmin):
    list_display = ['idOrder','ReceiverName', 'Price' ]
    # prepopulated_fields = {'ReceiverName': ('Address',)}
    fieldsets = [('Order detail' ,{ 'fields':['idRestaurant', 'Price','Meals','OrderDate','DriverId']}), ('Receiver',{'fields':['ReceiverName', 'Address']})]

admin.site.register(Orders, OrderAdmin)

class DriverAdmin(admin.ModelAdmin):
    list_display = ['idDriver','idRestaurant', 'driverCode','driverName']

admin.site.register(Drivers, DriverAdmin)