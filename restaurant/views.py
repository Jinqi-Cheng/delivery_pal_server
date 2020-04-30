from django.shortcuts import render
# from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

from accounts.models import Restaurant, Orders, Drivers

@login_required
def dashboard(request):
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    # driver = Drivers.objects.create(idRestaurant=None, idDriver=10)
    # orders = Orders.objects.create(idOrder=1, idRestaurant=restaurant,Price=34.5, ReceiverName='Hsuan', Meals=None, OrderDate=None, DriverId=driver, Address='6783')

    # driver = Drivers.objects.get(idDriver=10)
    # orders = Orders.objects.create(idOrder=2, idRestaurant=restaurant,Price=50.25, ReceiverName='Hsuan', Meals=None, OrderDate=None, DriverId=driver, Address='6625')

    driver = Drivers.objects.get(idDriver=10)
    orders = Orders.objects.filter(DriverId=driver)
    
    print(orders)


    return render(request, 'dashboard.html',{'restaurant': restaurant, 'orders':orders})
