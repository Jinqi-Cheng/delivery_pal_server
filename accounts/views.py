from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .forms import SignUpForm

# Create your views here.

from .models import Restaurant

def homePage(request):
    return render(request, 'homepage.html')

@login_required
def profile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('/admin/')
        else:
            restaurant = Restaurant.objects.get(user_id = user.id)
            return render(request, 'users/profile.html', {'restaurant': restaurant})
    else:
        return redirect('/accounts/login/',{'message':'Wrong password Please Try agagin'})

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
