from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.

from .models import Restaurant
from .forms import SignUpForm, ProfileForm, RestaurantForm

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
            return render(request, 'signup/signup_page.html', {'form': form, 'successful_submit':True})
    else:
        form = SignUpForm()
    return render(request, 'users/signup_page.html', {'form': form})
