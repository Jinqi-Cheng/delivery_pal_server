from django.urls import path
from django.contrib.auth import views as auth_views
# from account.views import login
from accounts import views
from accounts.loginForm import RestaurantLoginForm
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view( template_name='page-login.html', authentication_form=RestaurantLoginForm), name='login' ),
    path('logout/', auth_views.LogoutView.as_view( template_name='logged_out.html'), name='logout' ),
    # path('profile/', views.profile, name='profile' ),
    path('index/',views.index)
]