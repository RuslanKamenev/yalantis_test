from django.shortcuts import render
from rest_framework import status
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

# Возвращает весь список водителей
# Если в качестве URL параметра указан created_at__gte=dd-mm-YYYY, водителей созданных после указанной даты
# Если в качестве URL параметра указан created_at__lte=dd-mm-YYYY, водителей созданных до указанной даты
    def get(self, request):
        if 'created_at__gte' in request.query_params:
            if re.search(self.DATE_VALIDATION_REGEX, request.query_params['created_at__gte']):
                search_date = request.query_params['created_at__gte']
                search_date = datetime.datetime.strptime(search_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = Driver.objects.filter(created_at__gte=search_date)
                serializer = DriverNameSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Дата поиска введена неправильно'}, status=status.HTTP_400_BAD_REQUEST)

        if 'created_at__lte' in request.query_params:
            if re.search(self.DATE_VALIDATION_REGEX, request.query_params['created_at__lte']):
                search_date = request.query_params['created_at__lte']
                search_date = datetime.datetime.strptime(search_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = Driver.objects.filter(created_at__lte=search_date)
                serializer = DriverNameSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Дата поиска введена неправильно'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            queryset = Driver.objects.all()
            serializer = DriverNameSerializer(queryset, many=True)
            return Response(serializer.data)

# Добавление нового водителя
    def post(self, request):
        serializer = DriverNameSerializer(data=request.data, many=True)
        if serializer.is_valid():
            obj, created = Driver.objects.get_or_create(
                first_name=request.data[0]['first_name'],
                last_name=request.data[0]['last_name'])
            if created:
                return Response({'success': 'Пользователь успешно добавлен'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Неправильно введены поля'}, status=status.HTTP_400_BAD_REQUEST)


class DriverView(APIView):
    http_method_names = ['get', 'update', 'delete']

# Получение водителя по id
    def get(self, request, pk):
        if Driver.objects.filter(id=pk):
            queryset = Driver.objects.filter(id=pk)
            serializer = DriverFullInfoSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': f"Водитель с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)

# Обновление имени и фамилии водителя, если водителя с таким именем нет в БД
    def update(self, request, pk):
        if Driver.objects.filter(id=pk):
            serializer = DriverNameSerializer(data=request.data, many=True)
            if serializer.is_valid():
                if Driver.objects.filter(
                        first_name=request.data[0]['first_name'],
                        last_name=request.data[0]['last_name']):
                    return Response({'error': 'Водитель с указаным именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    update = Driver.objects.filter(id=pk).update(
                        first_name=request.data[0]['first_name'],
                        last_name=request.data[0]['last_name'])
                    if update:
                        return Response({'success': 'Пользователь успешно изменен'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f"Водитель с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)

# Удаление водителя из БД
    def delete(self, request, pk):
        if Driver.objects.filter(id=pk).delete():
            return Response({'success': f"Водитель с id={pk} успешно удален"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': f"Водитель с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)
