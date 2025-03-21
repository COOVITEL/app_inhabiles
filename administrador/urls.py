from django.urls import path, include
from .views import *

urlpatterns = [
    path('administrador/', administrador, name="administrador"),
]
