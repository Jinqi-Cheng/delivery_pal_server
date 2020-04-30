from django.urls import path
from django.contrib.auth import views as auth_views
# from account.views import login
from accounts import views

urlpatterns = [
<<<<<<< HEAD
    path('dashboard/', views.dashboard, name='dashboard'),
=======
    # path('dashboard/', views.dashboard, name='dashboard'),
>>>>>>> e953d0d065bc14cd93c3751fe910eb1842b47c26
    path('login/', auth_views.LoginView.as_view( template_name='login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view( template_name='logged_out.html'), name='logout' ),
    path('profile/', views.profile, name='profile' ),
]