from django.db import models


class tuktukUserData(models.Model):
    userID = models.CharField(max_length=50, primary_key=True)
    userName = models.CharField(max_length=50)
    dateOfRegistration = models.DateField()
