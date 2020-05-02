from django.db import models
from django_mysql.models import JSONField
# from django_mysql.models import JSONField, Model

# Create your models here.

from django.contrib.auth.models import User

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    idRestaurant = models.AutoField(primary_key = True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'Restaurant'

class Drivers(models.Model):

    idDriver = models.AutoField(primary_key=True)
    idRestaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL,null=True, to_field='idRestaurant')
    driverCode = models.CharField(max_length=12, unique=True, null=True)
    
    class Meta:
        db_table = "Drivers"
        verbose_name = 'Driver'

class Orders(models.Model):

    idOrder = models.AutoField(primary_key=True)
    idDisp = models.IntegerField(default=0)
    idRestaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, to_field='idRestaurant')
    Price = models.DecimalField(max_digits=9,decimal_places=4)
    ReceiverName = models.CharField(max_length=64)
    Meals = JSONField()
    OrderDate = models.DateTimeField()
    DriverId = models.ForeignKey(Drivers, on_delete=models.SET_NULL, null=True, to_field='idDriver')
    Address = models.CharField(max_length=1024)
    Rank = models.IntegerField(null=True)
    class Meta:
        db_table = "Orders"
        verbose_name = 'Order'