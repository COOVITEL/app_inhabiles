from django.db import models
from django.utils import timezone

class Asociado(models.Model):
    cedula = models.CharField(max_length=200)
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    nomina = models.CharField(max_length=200)
    tipoAsociado = models.CharField(max_length=200)
    fechaultimaAfiliacion = models.CharField(max_length=200)
    antiguedad = models.CharField(max_length=200)
    telefono = models.CharField(max_length=200)
    movil = models.CharField(max_length=200)
    cartera = models.CharField(max_length=200)
    aportes = models.CharField(max_length=200)
    numeroAhorro = models.CharField(max_length=200)
    cantidadAhorro = models.CharField(max_length=200)
    numeroCooviaho = models.CharField(max_length=200)
    cantidadCooviaho = models.CharField(max_length=200)
    numeroCdat = models.CharField(max_length=200)
    cantidadCdat = models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.nombre} - {self.cedula}"


class ResgistrosAsociado(models.Model): 
    asociado = models.ForeignKey(Asociado, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    asesor = models.CharField(max_length=200)
    observacion = models.TextField()
    
    def __str__(self):
        return f"{self.asociado}, asesor {self.asesor}"

