from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import Orders, Drivers
from accounts.models import Restaurant
from .forms import DriverForm

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
    return render(request, 'dashboard.html',{'restaurant': restaurant, 'orders':orders})

@login_required
def driverManager(request):
    if request.method == 'POST':
        driver_form = DriverForm(request.POST)
        if driver_form.is_valid():
            #Create a new driver
            new_driver = driver_form.save(commit=False)
            driver_form.save()
            restaurant = Restaurant.objects.get(user_id = request.user.id)
            restaurant.driverNumber = F('driverNumber') + 1
            restaurant.save()
            # print('New Name:', new_driver.driverName)
            # print('New Code:', new_driver.driverCode)
            # print('New ID:', new_driver.idDriver)
            redirect('restaurant/driverManager')
        else:
            print('Fail')
    else:
        driver_form = DriverForm()
    restaurant = Restaurant.objects.get(user_id = request.user.id)
    drivers = Drivers.objects.filter(idRestaurant=restaurant)
    
    driver_form = DriverForm(initial={'idRestaurant': restaurant,'driverCode':genDriverCode(restaurant)})
    # driver_form = DriverForm(initial={'idRestaurant': restaurant,'driverCode':genDriverCode(request.user.id, drivers)})
    return render(request, 'driverManager.html',{'restaurant': restaurant, 'drivers':drivers, 'driver_form':driver_form})

def genDriverCode(restaurant):
    code = str(restaurant.idRestaurant).zfill(6)
    next_id = restaurant.driverNumber+1 
    code += str(next_id).zfill(6)
    return code

@login_required
def driverDelete(request, id):
    driver = Drivers.objects.get(idDriver=id)
    if request.method == "POST":
        if driver:
            driver.delete()
        return redirect('../../')
    return render(request, "driverDelete.html", {"driver": driver})