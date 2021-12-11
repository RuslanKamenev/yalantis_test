from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import *
from api.serializers import *
import re
import datetime


# Работа со всеми водителями, добавление водителя.
class DriversView(APIView):
    http_method_names = ['get', 'post']
    DATE_VALIDATION_REGEX = '^(3[01]|[12][0-9]|0?[1-9])-(1[0-2]|0?[1-9])-([0-9]{4})$'

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
                return Response({'error': 'Дата поиска введена неправильно, требуемый формат даты d-m-Y'}, status=status.HTTP_400_BAD_REQUEST)

        if 'created_at__lte' in request.query_params:
            if re.search(self.DATE_VALIDATION_REGEX, request.query_params['created_at__lte']):
                search_date = request.query_params['created_at__lte']
                search_date = datetime.datetime.strptime(search_date, '%d-%m-%Y').strftime('%Y-%m-%d')
                queryset = Driver.objects.filter(created_at__lte=search_date)
                serializer = DriverNameSerializer(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Дата поиска введена неправильно, требуемый формат даты d-m-Y'}, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({'success': 'Водитель успешно добавлен'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Водитель с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Неправильно введены поля'}, status=status.HTTP_400_BAD_REQUEST)

# Работа с конкретным водителем: получение/удаление/обновление данных
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
                        return Response({'success': 'Водитель успешно изменен'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Водитель с таким именем и фамилией уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f"Водитель с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)

# Удаление водителя из БД по id
    def delete(self, request, pk):
        queryset = Driver.objects.filter(id=pk)
        if queryset:
            if Driver.objects.filter(id=pk).delete():
                return Response({'success': f"Водитель с id={pk} успешно удален"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ошибка удаления'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f"Водитель с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)


class VehiclesView(APIView):
    http_method_names = ['get', 'post']
    VEHICLE_VALIDATION_REGEX = '^([A-Z]{2} [0-9]{4} [A-Z]{2})$'

# Возвращает весь список автомобилей
# Если в качестве URL параметра указан with_drivers=yes, автомобилей с водителями
# Если в качестве URL параметра указан with_drivers=yes, автомобилей без водителя
    def get(self, request):
        queryset = False
        if 'with_drivers' in request.query_params:
            search_parameter = request.query_params['with_drivers'].strip()
            if search_parameter == 'yes':
                queryset = Vehicle.objects.filter(driver_id__isnull=False)
            elif search_parameter == 'no':
                queryset = Vehicle.objects.filter(driver_id__isnull=True)
            sanitizer = VehicleFullInfoSerializer(queryset, many=True)
            if queryset:
                return Response(sanitizer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': f'Параметр with_drivers введен неправильно, доступимые значения yes/no, получено: {search_parameter} или нет водителей с авто'},
                    status=status.HTTP_400_BAD_REQUEST)

        else:
            queryset = Vehicle.objects.all()
            serializer = VehicleShortInfoSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

# Добавление нового автомобиля
    def post(self, request):
        serializer = VehicleShortInfoSerializer(data=request.data, many=True)
        if serializer.is_valid() and re.search(self.VEHICLE_VALIDATION_REGEX, request.data[0]['plate_number']):
            if Vehicle.objects.filter(plate_number=request.data[0]['plate_number']):
                return Response({'error': 'Автомобиль с указаным номером уже есть в БД'}, status=status.HTTP_400_BAD_REQUEST)
            obj, created = Vehicle.objects.get_or_create(
                make=request.data[0]['make'],
                model=request.data[0]['model'],
                plate_number=request.data[0]['plate_number'])
            if created:
                return Response({'success': 'Автомобиль успешно добавлен'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ошибка'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Неправильно введены поля или данные в полях'}, status=status.HTTP_400_BAD_REQUEST)


class VehicleView(APIView):
    http_method_names = ['get', 'update', 'delete']

# Получение данных о автомобиле по id
    def get(self, request, pk):
        if Vehicle.objects.filter(id=pk):
            queryset = Vehicle.objects.filter(id=pk)
            serializer = VehicleFullInfoSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': f"Автомобиль с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)

# Обновление данных о автомобиле по id
    def update(self, request, pk):
        if Vehicle.objects.filter(id=pk):
            serializer = VehicleShortInfoSerializer(data=request.data, many=True)
            if serializer.is_valid():
                if Vehicle.objects.filter(plate_number=request.data[0]['plate_number']):
                    return Response({'error': 'Автомобиль с указаными номерами уже существует'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    update = Vehicle.objects.filter(id=pk).update(
                        make=request.data[0]['make'],
                        model=request.data[0]['model'],
                        plate_number=request.data[0]['plate_number'])
                    if update:
                        return Response({'success': 'Пользователь успешно изменен'}, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Пользователь с таким именем уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f"Водитель с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)

# Удаление автомобиля из БД по id
    def delete(self, request, pk):
        queryset = Vehicle.objects.filter(id=pk)
        if queryset:
            if Vehicle.objects.filter(id=pk).delete():
                return Response({'success': f"Автомобиль с id={pk} успешно удален"}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Ошибка удаления'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': f"Автомобиль с id={pk} не найден"}, status=status.HTTP_400_BAD_REQUEST)


class SetDriver(APIView):
    http_method_names = ['post']

# Добавление или удаление driver_id к автомобилю
    def post(self, request, pk):
        if 'id' in request.data[0] and Driver.objects.filter(id=request.data[0]['id']):
            vehicle_data = Vehicle.objects.filter(id=pk)
            driver_id = request.data[0]['id']
            if vehicle_data:
                serializer = VehicleFullInfoSerializer(vehicle_data, many=True)
                if driver_id == serializer.data[0]['driver_id']:
                    update = Vehicle.objects.filter(id=pk).update(driver_id=None)
                    return Response({'success': 'Водитель высажен из автомобиля'}, status=status.HTTP_200_OK)
                else:
                    update = Vehicle.objects.filter(id=pk).update(driver_id=driver_id)
                    return Response({'success': 'Водитель добавлен в автомобиль'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': f'Автомобиль с id={pk} не найдено'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': f'В запросе не указано id водителя или водителя с таким id в БД не найдено'},
                status=status.HTTP_400_BAD_REQUEST)
