from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Create your views here.

from .models import Restaurant

def index(request):
    return render(request, 'index.html')

@login_required
def dashboard(request):
    return redirect('restautant/dashboard.html')

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