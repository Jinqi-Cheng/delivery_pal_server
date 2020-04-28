from django.db import models
from django_mysql.models import JSONField
# from django_mysql.models import JSONField, Model

# Create your models here.

from django.contrib.auth.models import User

class Resaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    idRestaurant = models.AutoField(primary_key = True)
    name = models.CharField(max_length=64)

    class Meta:
        db_table = 'Restaurant'

class Drivers(models.Model):

    idDriver = models.AutoField(primary_key=True)
    idRestaurant = models.OneToOneField(Resaurant, on_delete=models.SET_NULL,null=True)

    # idRestaurant = models.IntegerField()
    class Meta:
        db_table = "Drivers"

class Orders(models.Model):

    idOrder = models.AutoField(primary_key=True)
    idRestaurant = models.ForeignKey(Resaurant, on_delete=models.SET_NULL, null=True)
    # idRestaurant = models.IntegerField()
    Price = models.DecimalField(max_digits=9,decimal_places=4)
    ReceiverName = models.CharField(max_length=64)
    Meals = JSONField()
    OrderDate = models.DateTimeField()
    DriverId = models.OneToOneField(Drivers, on_delete=models.SET_NULL, null=True, to_field='idDriver')
    # DriverId = models.IntegerField()
    Address = models.CharField(max_length=1024)

    class Meta:
        db_table = "Orders"