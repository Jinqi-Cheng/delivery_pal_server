from django.urls import path
from django.contrib.auth import views as auth_views
# from account.views import login
from accounts import views
from restaurant import views as rest_views

urlpatterns = [
    # path('upload/', views.upload, name='upload'),
    # path('upload/', rest_views.upload, name='upload'),
    path('', views.homePage, name='home'),
    path('login/', auth_views.LoginView.as_view( template_name='login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view( template_name='logged_out.html'), name='logout' ),
    path('signup/', views.signup, name='signup' ),
    path('profile/', views.profile, name='profile' ),
]