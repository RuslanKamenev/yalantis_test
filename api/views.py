from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.
class DriversView(APIView):
    http_method_names = ['get', 'post']
