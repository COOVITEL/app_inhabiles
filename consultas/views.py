from django.shortcuts import render, redirect, HttpResponse
from .models import Asociado, ResgistrosAsociado
from django.contrib import messages
from django.utils.timezone import localtime
from .utils import setValue
from django.core.cache import cache
from django.db import transaction
import pandas as pd

def index(request):
    
    if request.method == 'POST':
        form = request.POST.get("form_id")
        
        if form == "form-consulta":
            cedula = request.POST.get("cedula", "").strip()
            request.session.update({
                'cedula': cedula
            })
            
            asociado = Asociado.objects.filter(cedula=cedula).first()
            if not asociado:
                messages.error(request, "No se encontró ningún asociado con ese número de identificación.")
            else:
                request.session.update({
                    'name': asociado.nombre,
                })
                preaprobado = {
                    'prestamo': int(asociado.preaprobado) > 0,
                    'monto': setValue(asociado.preaprobado),
                    'cuota': setValue(asociado.cuota),
                    'plazo': asociado.plazo
                }
                return render(request, 'index.html', {
                    'asociado': asociado,
                    'prestamo': preaprobado
                })
            
        elif form == "form_entrega":
            try:
                with transaction.atomic():
                    ResgistrosAsociado.objects.create(
                        asociado=request.session.get('name'),
                        asesor=request.session.get('name'),
                        observacion=request.session.get('name'),
                    )
                messages.success(request, "Se ha registrado con éxito la entrega.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al registrar la entrega: {str(e)}")
            
    return render(request, 'index.html')

def close(request):
    return redirect ('index')

def seedUserus(request):
     df = pd.read_excel('base.xlsx', sheet_name='Base Plataforma 15012024', skiprows=1)
     asociados = df.values.tolist()
     for asociado in asociados:
         exist = Asociados.objects.filter(documento=asociado[0]).exists()
         if not exist:
             aso = Asociados(
                 documento=asociado[0],
                 nombre=asociado[1],
                 tipo=asociado[2],
                 obsequio=asociado[4],
                 state=asociado[5],
                 causa=asociado[6],
                 preaprobado=asociado[7],
                 cuota=asociado[8],
                 plazo=asociado[9]
                 )
             aso.save()
     return HttpResponse("Se crearon de forma correcta")