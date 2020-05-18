from django import forms
from django.contrib.auth.models import User
from .models import Restaurant
from restaurant.models import Drivers

# from django.db import models
import re

def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)

class SignUpForm(forms.Form):
    username = forms.CharField(label='Username*', max_length=50)
    name = forms.CharField(label='Restaurant Name*', max_length=64)
    email = forms.EmailField(label='Email', required=False)
    password1 = forms.CharField(label='Password*', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

    #user clean methods to define custom validation rules
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("your username must be at least 3 characters log")
        elif len(username) > 20:
            raise forms.ValidationError("your username is too long")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError('your username already exists')
        return username
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) > 64:
            raise forms.ValidationError("Your restaurant name is too long(less than or equal to 64 characters)")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email or email_check(email):
            pass
            # filter_result = User.objects.filter(email__exact=email)
            # if len(filter_result) > 0:
            #     raise forms.ValidationError("your email already exists")
        else:
            raise forms.ValidationError("Please enter a valid email")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 3:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch Please enter again')

        return password2

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(ProfileForm, self).__init__(*args, **kwargs)                       
        # self.fields['driverCode'].widget=forms.HiddenInput()
        # self.fields['idRestaurant'].widget=forms.HiddenInput()

    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

class RestaurantForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(RestaurantForm, self).__init__(*args, **kwargs)                       

    class Meta:
        model = Restaurant
        fields = ['name']

class DriverLoginForm(forms.Form):
    driverCode = forms.CharField(label='Driver Code', max_length=12)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    # use clean methods to define custom validation rules
    def clean_driverCode(self):
        driverCode = self.cleaned_data.get('driverCode')
        filter_result = Drivers.objects.filter(driverCode__exact=driverCode)
        if not filter_result:
            raise forms.ValidationError('This Driver Code does not exist. Please ask your manager.')
        return driverCode

class DriverEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): 
        super(DriverEditForm, self).__init__(*args, **kwargs)                       

    class Meta:
        model = Drivers
        fields = ['driverName', 'phone']

