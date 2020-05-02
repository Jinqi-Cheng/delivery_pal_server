from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Orders, Drivers
from accounts.models import Restaurant

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
