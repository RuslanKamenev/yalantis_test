from django.db import models

# Create your models here.
class DriversModel(models.Model):
    first_name = models.CharField(max_length=64)
    second_name = models.CharField(max_length=64)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)