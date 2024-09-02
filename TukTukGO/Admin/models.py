from django.db import models


# Create your models here.
class tuktukData(models.Model):
    VehicleRegNo = models.CharField(max_length=15, primary_key=True)
    vehicleType = models.CharField(max_length=10)
    vehicleFuelType = models.CharField(max_length=10)
    manufacturedCompany = models.CharField(max_length=20)
    Vcc = models.IntegerField()
    manufactureYear = models.CharField(max_length=4)
    RC = models.CharField(max_length=100)
    vPhoto = models.CharField(max_length=100)
    regDate = models.DateField()


class tuktukDriverData(models.Model):
    driverID = models.CharField(max_length=15, primary_key=True)
    driverName = models.CharField(max_length=20)
    houseName = models.CharField(max_length=50)
    placeName = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    phoneNumber = models.CharField(max_length=12)
    gender = models.CharField(max_length=10)
    dateOfBirth = models.DateField()
    aadhar = models.CharField(max_length=12)
    license = models.CharField(max_length=25)
    driverPhoto = models.CharField(max_length=100)
    dateOfRegistration = models.DateField()


class tuktukDriverAllot(models.Model):
    allotID = models.CharField(max_length=8, primary_key=True)
    VehicleRegNo = models.CharField(max_length=12)
    driverID = models.CharField(max_length=15)
    allotDate = models.DateField()
    status = models.CharField(max_length=3)


class feedback(models.Model):
    feedbackID = models.IntegerField(primary_key=True)
    feedback = models.CharField(max_length=100)
    feedbackDate = models.DateField()
    userID = models.CharField(max_length=50)
    driverID = models.CharField(max_length=50)
    reply = models.CharField(max_length=100)
    replyDate = models.DateField()
    EMail = models.CharField(max_length=50)
    name = models.CharField(max_length=50)


class fareEstimation(models.Model):
    fareNO = models.IntegerField(primary_key=True)
    minimumFare = models.IntegerField()
    farePerKm = models.IntegerField()
    waitingFare = models.IntegerField()
    currentDateOfChange = models.DateField()
    minimumKM = models.IntegerField()
