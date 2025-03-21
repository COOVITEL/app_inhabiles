from django.urls import path
from .views import index, close, seedAsociados

urlpatterns = [
    path('', index, name='index'),
    path('close/', close, name="close"),
    path('createAndUpdateAsociados/', seedAsociados, name="created")
]
