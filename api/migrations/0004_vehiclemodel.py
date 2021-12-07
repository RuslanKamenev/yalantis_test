# Generated by Django 3.2.9 on 2021-12-07 23:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_delete_vehiclemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=4)),
                ('model', models.CharField(max_length=64)),
                ('plate_number', models.CharField(max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('driver_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.drivermodel')),
            ],
        ),
    ]
