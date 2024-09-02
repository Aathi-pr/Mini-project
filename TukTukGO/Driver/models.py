from django.db import models

# Create your models here.


class tuktukResponse(models.Model):
    requestID = models.CharField(max_length=50)
    responseTime = models.TimeField()
    responseDate = models.DateField()
    response = models.CharField(max_length=50)


class endOfRide(models.Model):
    requestID = models.CharField(max_length=50)
    totalRideRate = models.IntegerField()
    waitingCharges = models.IntegerField()
    endOfRideDate = models.DateField()
    endOfRideTime = models.TimeField()
    emotionFeedback = models.CharField(max_length=100)
    totalDistance = models.CharField(max_length=50)


class onGoingRide(models.Model):
    requestID = models.CharField(max_length=50)
    minimumFare = models.IntegerField()
    waitingFare = models.IntegerField()
    onGoingRideDate = models.DateField()
    onGoingRideTime = models.TimeField()
    comment = models.CharField(max_length=100)
