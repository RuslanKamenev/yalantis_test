# Generated by Django 3.2.9 on 2021-12-08 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_driver_id_vehiclemodel_driver'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DriverModel',
            new_name='Driver',
        ),
        migrations.RenameModel(
            old_name='VehicleModel',
            new_name='Vehicle',
        ),
    ]
