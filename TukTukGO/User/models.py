from django.db import models


# Create your models here.
class loginCredentials(models.Model):
    userID = models.CharField(max_length=20, primary_key=True)
    EMail = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=10)


class loginSession(models.Model):
    userID = models.CharField(max_length=20, primary_key=True)
    userType = models.CharField(max_length=10)


class tuktukRequest(models.Model):
    requestID = models.CharField(max_length=50, primary_key=True)
    userID = models.CharField(max_length=50)
    destination = models.CharField(max_length=60)
    requestDate = models.DateField()
    requestTime = models.TimeField()
    VehicleRegNo = models.CharField(max_length=50)
    userLat = models.FloatField()
    userLon = models.FloatField()
    driverID = models.CharField(max_length=50)
    distance = models.DecimalField(max_digits=5, decimal_places=2)
