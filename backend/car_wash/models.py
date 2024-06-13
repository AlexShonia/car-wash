from django.db import models
from django.contrib.auth.models import User


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    brand = models.CharField(max_length=200, blank=False)
    model = models.CharField(max_length=200, blank=False)
    type = models.CharField(max_length=200, blank=False)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    date = models.DateTimeField("appointment date", blank=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, blank=False)
