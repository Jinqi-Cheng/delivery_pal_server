from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    idRestaurant = models.AutoField(primary_key = True)
    name = models.CharField(max_length=64)
    driverNumber = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=128, null=True, blank=True,default="")
    class Meta:
        db_table = 'Restaurant'
