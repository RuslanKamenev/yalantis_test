from django.db import models


# Create your models here.
class Driver(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vehicle(models.Model):
    make = models.CharField(max_length=4)
    model = models.CharField(max_length=64)
    plate_number = models.CharField(max_length=8)

    driver = models.ForeignKey(Driver, null=True, on_delete=models.SET_NULL)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

