from django.urls import path
from api.views import *

urlpatterns = [
    path('drivers/driver/', DriversView.as_view()),
    path('vehicles/vehicle/', VehiclesView.as_view()),
    path('drivers/driver/<int:pk>/', DriverView.as_view()),
    path('vehicles/vehicle/<int:pk>/', VehicleView.as_view())
]
