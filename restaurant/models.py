from django.db import models

from accounts.models import Restaurant
from django_mysql.models import JSONField
from .driverModel import AbstractBaseDriver, DriverManager

# Create your models here.
class Drivers(AbstractBaseDriver):

    idDriver = models.AutoField(primary_key=True, verbose_name='ID')
    idRestaurant = models.ForeignKey(Restaurant, verbose_name='Restaurant', on_delete=models.SET_NULL,null=True, to_field='idRestaurant')
    driverCode = models.CharField(max_length=12, verbose_name='Driver Code', unique=True, null=True)
    driverName = models.CharField(max_length=64, verbose_name='Name', null=True)
    phone = models.CharField(max_length=32, null=True)

    USERNAME_FIELD = 'driverCode'
    REQUIRED_FIELDS = ['driverCode']

    objects = DriverManager()

    class Meta:
        db_table = "Drivers"
        verbose_name = 'Driver'

    # function
    def get_idDriver(self):
        return self.idDriver

    def get_driverName(self):
        return self.driverName

    def get_idRestaurant(self):
        return self.idRestaurant
    
    def get_phone(self):
        return self.phone

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

class Coordinate(models.Model):

    idCoordinate = models.AutoField(primary_key=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    
    class Meta:
        db_table = "Coordinate"
        # verbose_name = 'Coor'

class Address(models.Model):

    idAddr = models.AutoField(primary_key=True)
    address = models.CharField(max_length=1024)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    # idCoordinate = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, null=True, to_field='idCoordinate')
    idCoordinate = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, default=None, null=True, to_field='idCoordinate')
    
    class Meta:
        db_table = "Address"

class Distance(models.Model):

    idDistance = models.AutoField(primary_key=True)
    point_A = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, null=True
        , to_field='idCoordinate', related_name="pointA_2_coor")

    point_B = models.ForeignKey(Coordinate, on_delete=models.SET_NULL, null=True
        , to_field='idCoordinate', related_name="pointB_2_coor")
    distance = models.DecimalField(max_digits=8,decimal_places=3)
    class Meta:
        db_table = "Distance"

