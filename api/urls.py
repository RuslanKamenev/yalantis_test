from django.urls import path
from api.views import *

urlpatterns = [
    path('drivers/driver/', DriversView.as_view()),
]
