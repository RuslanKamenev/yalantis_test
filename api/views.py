from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from api.serializers import *
import re
import datetime


# Create your views here.
class DriversView(APIView):
    http_method_names = ['get', 'post']
    DATE_VALIDATION_REGEX = '(3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([0-9]{4})$'

    def get(self, request):
        if 'created_at__gte' in request.query_params:
            if re.search(self.DATE_VALIDATION_REGEX, request.query_params['created_at__gte']):
                search_date = request.query_params['created_at__gte']
                search_date = datetime.datetime.strptime(search_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = Driver.objects.filter(created_at__gte=search_date)
                serializer = DriverNameSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'Дата поиска введена неправильно'})

        if 'created_at__lte' in request.query_params:
            if re.search(self.DATE_VALIDATION_REGEX, request.query_params['created_at__lte']):
                search_date = request.query_params['created_at__lte']
                search_date = datetime.datetime.strptime(search_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = Driver.objects.filter(created_at__lte=search_date)
                serializer = DriverNameSerializer(queryset, many=True)
                return Response(serializer.data)
            else:
                return Response({'error': 'Дата поиска введена неправильно'})

        else:
            queryset = Driver.objects.all()
            serializer = DriverNameSerializer(queryset, many=True)
            return Response(serializer.data)
