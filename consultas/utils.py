def prioridadProductos(num1, num2, num3):
    count = sum(1 for num in [num1, num2, num3] if num > 0)
    if count == 3:
        return "Alta"
    elif count == 2:
        return "Media"
    else:
        return "Baja"

def prioridadCdat(value):
    if value >= 100000 and value < 1000000:
        return "Baja"
    if value >= 1000000 and value < 10000000:
        return "Media"
    if value >= 10000000:
        return "Alta"
    else:
        return ""

def prioridadCartera(value):
    if value >= 100000 and value < 1000000:
        return "Baja"
    if value >= 1000000 and value < 10000000:
        return "Media"
    if value >= 10000000:
        return "Alta"
    else:
        return "No cuenta con cartera"

def prioridadCarteraExiste(value):
    if value > 0:
        return "Alta"
    return "Baja"

def findRentabilidad(value):
    if value >= 0 and value < 0.05:
        return "Baja"
    if value >= 0.05 and value < 0.1:
        return "Media"
    if value >= 0.1:
        return "Alta"
    else:
        return ""

def estadoCartera(calificacion):
    if calificacion == "A":
        return "Cartera Normal"
    elif calificacion == "-":
        return "No cuenta con Cartera"
    return "Cartera Vencida"

def estadoAportes(dias):
    if dias <= 30:
        return "Aportes al día"
    return f"Gestionar normalización de aportes: dias vencidos {dias}"

def porcentajeRen(num):
    mul = num * 100
    print(f"Porcentaje de rentabilidad: {mul}")
    return round(mul, 2)
