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
            request.session.update({'cedula': cedula})

            asociado = Asociado.objects.filter(cedula=cedula).first()
            if not asociado:
                messages.error(request, "No se encontró ningún asociado con ese número de identificación.")
            else:
                registros = ResgistrosAsociado.objects.filter(asociado=asociado).order_by('-fecha')
                request.session.update({'name': asociado.nombre})

                return render(request, 'index.html', {
                    'asociado': asociado,
                    'registros': registros,  # Agregar registros al contexto
                })

        elif form == "form_entrega":
            try:
                with transaction.atomic():
                    ResgistrosAsociado.objects.create(
                        asociado=Asociado.objects.get(cedula=request.session.get('cedula')),
                        asesor=request.session.get('name'),
                        observacion=request.POST.get('razon'),
                    )
                messages.success(request, "Se ha registrado con éxito la entrega.")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al registrar la entrega: {str(e)}")

    return render(request, 'index.html')


def close(request):
    return redirect ('index')

def seedAsociados(request):
    df = pd.read_excel('BASE_INACTIVIDAD_90_120.xlsx', sheet_name='INACTIVIDAD_91_120', skiprows=1)
    asociados = df.values.tolist()
    for asociado in asociados:
        exist = Asociado.objects.filter(cedula=asociado[0]).first()
        if not exist:
            aso = Asociado(
                cedula=asociado[0],
                nombre=asociado[3],
                ubicacion=asociado[4],
                nomina=asociado[8],
                tipoAsociado=asociado[10],
                fechaultimaAfiliacion=asociado[11],
                antiguedad=asociado[13],
                telefono=asociado[33],
                movil=asociado[34],
                cartera=asociado[63],
                aportes=asociado[28],
                numeroAhorro=asociado[57],
                cantidadAhorro=asociado[58],
                numeroCooviaho=asociado[59],
                cantidadCooviaho=asociado[60],
                numeroCdat=asociado[61],
                cantidadCdat=asociado[62]
            )
            aso.save()
        else:
            updated = False
            if exist.nombre != asociado[3]:
                exist.nombre = asociado[3]
                updated = True
            if exist.ubicacion != asociado[4]:
                exist.ubicacion = asociado[4]
                updated = True
            if exist.nomina != asociado[8]:
                exist.nomina = asociado[8]
                updated = True
            if exist.tipoAsociado != asociado[10]:
                exist.tipoAsociado = asociado[10]
                updated = True
            if exist.fechaultimaAfiliacion != asociado[11]:
                exist.fechaultimaAfiliacion = asociado[11]
                updated = True
            if exist.antiguedad != asociado[13]:
                exist.antiguedad = asociado[13]
                updated = True
            if exist.telefono != asociado[33]:
                exist.telefono = asociado[33]
                updated = True
            if exist.movil != asociado[34]:
                exist.movil = asociado[34]
                updated = True
            if exist.cartera != asociado[63]:
                exist.cartera = asociado[63]
                updated = True
            if exist.aportes != asociado[28]:
                exist.aportes = asociado[28]
                updated = True
            if exist.numeroAhorro != asociado[57]:
                exist.numeroAhorro = asociado[57]
                updated = True
            if exist.cantidadAhorro != asociado[58]:
                exist.cantidadAhorro = asociado[58]
                updated = True
            if exist.numeroCooviaho != asociado[59]:
                exist.numeroCooviaho = asociado[59]
                updated = True
            if exist.cantidadCooviaho != asociado[60]:
                exist.cantidadCooviaho = asociado[60]
                updated = True
            if exist.numeroCdat != asociado[61]:
                exist.numeroCdat = asociado[61]
                updated = True
            if exist.cantidadCdat != asociado[62]:
                exist.cantidadCdat = asociado[62]
                updated = True
            if updated:
                exist.save()
    return HttpResponse("Se crearon y actualizaron los registros de forma correcta")