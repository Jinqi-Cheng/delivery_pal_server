from django.db import models

from accounts.models import Restaurant
from django_mysql.models import JSONField

# Create your models here.
class Drivers(models.Model):

    idDriver = models.AutoField(primary_key=True)
    idRestaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL,null=True, to_field='idRestaurant')
    driverCode = models.CharField(max_length=12, unique=True, null=True)
    driverName = models.CharField(max_length=64, null=True)
    
    class Meta:
        db_table = "Drivers"
        verbose_name = 'Driver'

class Orders(models.Model):

    idOrder = models.AutoField(primary_key=True)
    idDisplay = models.PositiveSmallIntegerField(default=0)
    idRestaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, to_field='idRestaurant')
    Price = models.DecimalField(max_digits=9,decimal_places=4)
    ReceiverName = models.CharField(max_length=64)
    Meals = JSONField()
    OrderDate = models.DateTimeField()
    DriverId = models.ForeignKey(Drivers, on_delete=models.SET_NULL, null=True, to_field='idDriver')
    Address = models.CharField(max_length=1024)
    isPickup = models.BooleanField(default=False)
    Sequence = models.PositiveIntegerField(default=0)
    Phone = models.CharField(max_length=20,blank=True)
    Note = models.CharField(max_length=1024,blank=True)

    class Meta:
        db_table = "Orders"
        verbose_name = 'Order'

class Address(models.Model):

    idAddr = models.AutoField(primary_key=True)
    address = models.CharField(max_length=1024)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    idCoordinate = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, null=True, to_field='idCoordinate')
    
    class Meta:
        db_table = "Address"

class Coordinate(models.Model):

    idCoordinate = models.AutoField(primary_key=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    
    class Meta:
        db_table = "Coordinate"
        # verbose_name = 'Coor'

class Distance(models.Model):

    idDistance = models.AutoField(primary_key=True)
    point_A = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, null=True, to_field='idCoordinate')
    point_B = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, null=True, to_field='idCoordinate')
    distance = models.DecimalField(max_digits=8,decimal_places=3)
    class Meta:
        db_table = "Distance"

