from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    idRestaurant = models.AutoField(primary_key = True)
    name = models.CharField(max_length=64)
    driverNumber = models.PositiveIntegerField(default=0)
    isActive = models.BooleanField(default=True)
    expiryDate = models.DateTimeField(null=True, blank= True)
    agreeTerm = models.BooleanField(default=False)

    class Meta:
        db_table = 'Restaurant'
    
    def __str__(self):
        return "%s" % self.name
    def __unicode__(self):
        return "%s" % self.name
