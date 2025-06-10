from django.shortcuts import render, redirect, HttpResponse
from .models import Asociado, ResgistrosAsociado
from django.contrib import messages
from django.utils.timezone import localtime
from .utils import *
from django.core.cache import cache
from django.db import transaction
import pandas as pd
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
                request.session.update({'asociado_nombre': asociado.nombre})  # Changed session key to 'asociado_nombre'
                numCoovi = asociado.numeroCooviaho
                numCdat = asociado.numeroCdat
                numVista = asociado.numeroAhorro
                valorCdat = asociado.cantidadCdat
                valorCartera = asociado.cartera
                return render(request, 'index.html', {
                    'asociado': asociado,
                    'registros': registros,
                    'prioridad1': prioridadProductos(int(numCoovi), int(numCdat), int(numVista)),
                    'prioridad2': prioridadCdat(int(valorCdat)),
                    'prioridad3': prioridadCartera(int(valorCartera)),
                    'prioridad4': prioridadCarteraExiste(int(valorCartera)),
                    'estadoCartera': estadoCartera(asociado.calificacion),
                    'dias': estadoAportes(int(asociado.diasVencidos)),
                    'porcentajeRen': porcentajeRen(float(asociado.rentabilidadPor)) if asociado.rentabilidadPor else "No disponible",
                })

        elif form == "form_entrega":
            try:
                with transaction.atomic():
                    asesor_name = request.POST.get('asesor_nombre')  # Get the asesor name from the form
                    ResgistrosAsociado.objects.create(
                        asociado=Asociado.objects.get(cedula=request.session.get('cedula')),
                        asesor=asesor_name,  # Use the asesor name from the form
                        observacion=request.POST.get('razon'),
                    )
                messages.success(request, "Se ha registrado la observación")
            except Exception as e:
                messages.error(request, f"Ocurrió un error al registrar el seguimiento: {str(e)}")

    return render(request, 'index.html')


def close(request):
    return redirect ('index')

def seedAsociados(request):
    # 1. Cargar el Excel
    try:
        df = pd.read_excel('baseMayoUp.xlsx', sheet_name='MAYO')
        asociados_data = df.to_dict(orient='records')

        # 2. Cargar todos los asociados existentes a memoria (usando cedula como clave)
        existentes = {
            str(aso.cedula).strip().replace(".0", ""): aso
            for aso in Asociado.objects.all()
        }

        nuevos = []
        actualizados = []
        campos_actualizables = [
            'nombre', 'ubicacion', 'nomina', 'tipoAsociado', 'fechaultimaAfiliacion',
            'antiguedad', 'acumAportes', 'aportes', 'telefono', 'movil', 'correo',
            'numeroAhorro', 'cantidadAhorro', 'numeroCooviaho', 'cantidadCooviaho',
            'numeroCdat', 'cantidadCdat', 'cartera', 'rentabilidad', 'rentabilidadPor',
            'salario', 'calificacion', 'diasVencidos'
        ]

        for data in asociados_data:
            cedula_raw = data.get('NRO_CEDULA')
            if pd.isna(cedula_raw):
                continue

            cedula = str(int(cedula_raw))  # Eliminar .0 si está presente

            if not cedula:
                continue

            campos = {
                'nombre': data.get('NOMBRES'),
                'ubicacion': data.get('N_UBICA1'),
                'nomina': data.get('NOMINA'),
                'tipoAsociado': data.get('K_TIPASO'),
                'fechaultimaAfiliacion': data.get('F_ULTAFI'),
                'antiguedad': data.get('F_ANTIGU'),
                'acumAportes': int(data.get('ACUM_APO')) if not pd.isna(data.get('ACUM_APO')) else 0,
                'aportes': int(data.get('ACUM_APO')) if not pd.isna(data.get('ACUM_APO')) else 0,
                'telefono': data.get('FIJO'),
                'movil': data.get('MOVIL'),
                'correo': data.get('D_EMAIL'),
                'numeroAhorro': int(data.get('N_AHORROVISTA')) if not pd.isna(data.get('N_AHORROVISTA')) else 0,
                'cantidadAhorro': int(data.get('Ah. Vista')) if not pd.isna(data.get('Ah. Vista')) else 0,
                'numeroCooviaho': int(data.get('N_COVIAHORRO')) if not pd.isna(data.get('N_COVIAHORRO')) else 0,
                'cantidadCooviaho': int(data.get('Cooviahorro')) if not pd.isna(data.get('Cooviahorro')) else 0,
                'numeroCdat': int(data.get('N_CDAT')) if not pd.isna(data.get('N_CDAT')) else 0,
                'cantidadCdat': int(data.get('CDAT')) if not pd.isna(data.get('CDAT')) else 0,
                'cartera': int(data.get('Cartera')) if not pd.isna(data.get('Cartera')) else 0,
                'rentabilidad': data.get('tipólogiaTipologia'),
                'rentabilidadPor': data.get('Rent. EA'),
                'salario': data.get('SALARIO'),
                'calificacion': data.get('Calif'),
                'diasVencidos': int(data.get('DIAS_VENCIDOS')) if not pd.isna(data.get('DIAS_VENCIDOS')) else 0,
            }

            existente = existentes.get(cedula)

            if not existente:
                nuevos.append(Asociado(cedula=cedula, **campos))
            else:
                actualizado = False
                for campo, valor in campos.items():
                    if getattr(existente, campo) != valor:
                        setattr(existente, campo, valor)
                        actualizado = True
                if actualizado:
                    actualizados.append(existente)

        # 3. Guardar en lote
        if nuevos:
            Asociado.objects.bulk_create(nuevos, batch_size=1000)

        if actualizados:
            Asociado.objects.bulk_update(actualizados, campos_actualizables, batch_size=1000)

        return HttpResponse(f"Se crearon {len(nuevos)} y se actualizaron {len(actualizados)} registros correctamente.")
    except Exception as e:
        # Loguear el error en consola o archivo
        print(f"Error procesando asociados: {e}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def proxy_asesores(request):
    url = "https://adminsimuladores.coovitel.coop/api/asesores/"
    headers = {
        "Authorization": "Token c75ac915b957a299350028888cf832efa86e5b1c"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Si no es 2xx, lanza error
        return JsonResponse(response.json(), safe=False)

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"No se pudo obtener la lista de asesores: {str(e)}"}, status=500)
