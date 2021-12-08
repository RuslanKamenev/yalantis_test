from rest_framework import serializers
from api.models import *


class DriverNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name']
