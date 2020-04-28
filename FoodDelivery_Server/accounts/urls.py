from django.urls import path
from django.contrib.auth import views as auth_views
# from account.views import login
from accounts import views

urlpatterns = [
    # path('^$', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view( template_name='login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view( template_name='logged_out.html'), name='logout' ),
    path('profile/', views.profile, name='profile' ),
    # path('login/', login, name='login' ),
]