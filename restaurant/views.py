from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Orders, Drivers
from accounts.models import Restaurant
from .Order import Order

import datetime

# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    drivers = Drivers.objects.filter(idRestaurant=restaurant)
    orders = []
    for driver in drivers:
        orders += Orders.objects.filter(DriverId=driver)

    today = datetime.date.today()
    tmr =today+ datetime.timedelta(days=1)
    return render(request, 'dashboard.html',{'restaurant': restaurant, 'orders':orders,'today':today,'Tmr':tmr})

@login_required
def order_for_kitchen(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    restaurant = Restaurant.objects.get(user_id=request.user.id)
    print(restaurant)
    dic = Order.parser_meals(restaurant.idRestaurant,"2020-05-01",True)
    return render(request,'order_for_kitchen.html',{'orders':dic.items()})

def get_order_sequence(request):
    driver_id = request.GET.get('driver_id')
    date = request.GET.get('date')
    lst = Order.generate_deliver_list(driver_id,date)
    return JsonResponse(lst,safe=False)