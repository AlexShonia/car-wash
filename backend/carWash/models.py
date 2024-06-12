from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    type = models.CharField(max_length=200)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField("appointment date")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
