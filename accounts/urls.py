from django.urls import path
from django.contrib.auth import views as auth_views
# from account.views import login
from accounts import views
from restaurant import views as rest_views


urlpatterns = [
    path('', views.homePage, name='home'),
    path('login/', auth_views.LoginView.as_view( template_name='Restaurant_login.html'), name='login' ),
    path('logout/', auth_views.LogoutView.as_view( template_name='logged_out.html'), name='logout' ),
    path('signup/', views.signup, name='signup' ),
    path('profile/', views.profile, name='profile' ),
    path('profile/edit/', views.edit_profile, name='edit_profile' ),
    path('profile/edit/change-password/', 
        auth_views.PasswordChangeView.as_view
        ( 
            template_name='users/change_password.html',
            success_url = '../' 
        ),
        name='change_password'),
    path('driver/login/', views.driverLogin, name='driverLogin' ),
    path('driver/edit/', views.edit_DriverProfile, name='driverEdit' ),
    path('driver/edit/change-password/', views.PasswordChangeForDriver,name='PWChangeForDriver'), 

    path('TermAndConditionPage', views.TermAndConditionPage, name='termCondition' ),
    path('PrivacyPolicyPage', views.PrivacyPolicyPage, name='PrivacyPolicy' ),
    path('DisclaimerPage', views.DisclaimerPage, name='Disclaimer' ),

]