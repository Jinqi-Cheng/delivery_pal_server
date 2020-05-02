from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .loginForm import LoginForm

# Create your views here.

from .models import Restaurant

@login_required
def dashboard(request):
    return redirect('restaurant/dashboard.html')
    # return render(request, 'restautant/dashboard.html',{'section': 'dashboard'})
    # return render(request, 'dashboard.html',{'section': 'dashboard'})

@login_required
def profile(request):
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('/admin/')
        else:
            restaurant = Restaurant.objects.get(user_id = user.id)
            return render(request, 'profile.html', {'restaurant': restaurant})
    else:
        return redirect('/accounts/login/',{'message':'Wrong password Please Try agagin'})