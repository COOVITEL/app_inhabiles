from django.urls import path
from .views import index, close, seedAsociados
from . import views

urlpatterns = [
    path('', index, name='index'),
    path('close/', close, name="close"),
    path('createAndUpdateAsociados/', seedAsociados, name="created"),
    path('proxy/asesores/', views.proxy_asesores, name='proxy_asesores'),
]
