from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Resaurant

admin.site.unregister(User)

class RestaurantProfileInline(admin.StackedInline):
    model = Resaurant

class RestaurantProfile(UserAdmin):
    inlines = [RestaurantProfileInline, ]

admin.site.register(User, RestaurantProfile)
