from django.contrib import admin

# Register your models here.
from .models import Orders, Drivers

class OrderAdmin(admin.ModelAdmin):
    list_display = ['idOrder','ReceiverName', 'Price' ]
    fieldsets = [('Order detail' ,{ 'fields':['idRestaurant', 'Price','Meals','OrderDate','DriverId']}), ('Receiver',{'fields':['ReceiverName', 'Address', 'Phone', 'Note']})]

admin.site.register(Orders, OrderAdmin)

class DriverAdmin(admin.ModelAdmin):
    # A template for a very customized change view:
    change_form_template = 'driver/driverChangeView.html'

    list_display = ['idDriver','idRestaurant', 'driverCode','driverName', 'phone']
    readonly_fields = ('idRestaurant', 'driverCode','password',)

    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     extra_context = extra_context or {}
    #     extra_context['osm_data'] = self.get_osm_info()
    #     return super().change_view(
    #         request, object_id, form_url, extra_context=extra_context,
    #     )

admin.site.register(Drivers, DriverAdmin)