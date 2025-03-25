from django.contrib import admin
from .models import *

@admin.register(Asociado)
class AsociadoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'cedula']
    field = ['nombre', 'cedula']

@admin.register(ResgistrosAsociado)
class AsociadoAdmin(admin.ModelAdmin):
    search_fields = ['asociado', 'fecha']
    field = ['asociado', 'fecha']