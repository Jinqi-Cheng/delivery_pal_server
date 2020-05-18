from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib import messages


# Create your views here.

from .models import Restaurant
from .forms import SignUpForm, ProfileForm, RestaurantForm, DriverLoginForm, DriverEditForm
from restaurant.models import Drivers
from restaurant.forms import DriverPWChangeForm


def homePage(request):
    return render(request, 'homePage.html')

@login_required
def profile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('/admin/')
        else:
            restaurant = Restaurant.objects.get(user_id = user.id)
            return render(request, 'users/profile.html', {'user': user, 'restaurant': restaurant})
    else:
        return redirect('/accounts/login/',{'message':'Wrong password Please Try agagin'})

@login_required
def edit_profile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('/admin/')
    else:
        return redirect('/accounts/login/')

    if request.method == 'POST':
        user_form = ProfileForm(request.POST)
        restaurant_form = RestaurantForm(request.POST)
        if user_form.is_valid() and restaurant_form.is_valid():
            email = user_form.cleaned_data['email']
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            name = restaurant_form.cleaned_data['name']
            restaurant = Restaurant.objects.get(user_id = request.user.id)

            User.objects.filter(id = request.user.id).update(email=email, last_name=last_name, first_name=first_name)
            Restaurant.objects.filter(user_id = request.user.id).update(name=name)
            return redirect("../")
    else:
        instance = get_object_or_404(User, id=user.id)
        restaurant = Restaurant.objects.get(user_id = user.id)
        rest_instance = get_object_or_404(Restaurant, idRestaurant=restaurant.idRestaurant)
        user_form = ProfileForm(request.POST or None, instance=instance)
        restaurant_form = RestaurantForm(request.POST or None, instance=rest_instance)
    return render(request, 'users/edit_profile.html', {'user': user, 'restaurant_form': restaurant_form, 'user_form': user_form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']
            name = form.cleaned_data['name']
            user = User.objects.create_user(username=username, password=password, email=email)
            restaurant = Restaurant(user=user, name = name)
            restaurant.save()

            form = SignUpForm()
            return render(request, 'users/signup_page.html', {'form': form, 'successful_submit':True})
    else:
        form = SignUpForm()
    return render(request, 'users/signup_page.html', {'form': form})

def driverLogin(request):
    request.session['idDriver'] = None
    if request.method == 'POST':
        form = DriverLoginForm(request.POST)
        if form.is_valid():
            driverCode = form.cleaned_data['driverCode']
            password = form.cleaned_data['password']
            driver = get_object_or_404(Drivers, driverCode=driverCode)
            if driver.check_password(password) is True:
                request.session['idDriver'] = driver.idDriver
                return redirect(reverse('driverEdit'))
            else:
                request.session['idDriver'] = None
                return render(request, 'driver_login.html', {'form': form, 'message':'Wrong password Please Try agagin'})
    else:
        form = DriverLoginForm()
    return render(request, 'driver/driver_login.html', {'form': form})

def edit_DriverProfile(request):
    try:
        id = request.session.get('idDriver')
        if not id:
            return redirect(reverse('driverLogin'))
    except KeyError:
        return redirect(reverse('driverLogin'))

    if request.method == 'POST':
        driver_form = DriverEditForm(request.POST)
        driver = get_object_or_404(Drivers, idDriver=id)
        if driver_form.is_valid():
            driverName = driver_form.cleaned_data['driverName']
            phone = driver_form.cleaned_data['phone']
            Drivers.objects.filter(idDriver = id).update(driverName=driverName, phone=phone)
            return render(request, 'driver/driverEditForm.html', {'driver_form': driver_form, 'driver': driver, 'message':'True'})
        else:
            print('Fail')
    else:
        driver = get_object_or_404(Drivers, idDriver=id)
        driver_form = DriverEditForm(instance=driver)
    return render(request, 'driver/driverEditForm.html', {'driver_form': driver_form, 'driver': driver})

def PasswordChangeForDriver(request): 
    try:
        id = request.session.get('idDriver')
        if not id:
            return redirect(reverse('driverLogin'))
    except KeyError:
        return redirect(reverse('driverLogin'))

    driver = Drivers.objects.get(idDriver=id)
    if request.method == "POST":
        form = DriverPWChangeForm(driver, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your password was successfully updated!')
            return redirect('../')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = DriverPWChangeForm(driver)
    return render(request, 'driver/ChangePassowrdForDriver.html', {'form': form})


