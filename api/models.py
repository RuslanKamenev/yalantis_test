from django.db import models


# Create your models here.
class DriverModel(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VehicleModel(models.Model):
    driver = models.ForeignKey(DriverModel, null=True, on_delete=models.SET_NULL)

    make = models.CharField(max_length=4)
    model = models.CharField(max_length=64)
    plate_number = models.CharField(max_length=8)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

