from django.contrib import admin
from .models import Asociado

@admin.register(Asociado)
class AsociadoAdmin(admin.ModelAdmin):
    search_fields = ['nombre', 'cedula']
    field = ['nombre', 'cedula']