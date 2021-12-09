from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from api.models import *


class DriverNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name']


class DriverFullInfoSerializer(serializers.ModelSerializer):
    class Meta:
        validator = [
            UniqueTogetherValidator(
                queryset=Driver.objects.all(),
                fields=['first_name', 'last_name']
            )]
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'created_at', 'updated_at']
