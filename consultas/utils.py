def prioridadProductos(num1, num2, num3):
    count = sum(1 for num in [num1, num2, num3] if num > 0)
    if count == 3:
        return "Alta"
    elif count == 2:
        return "Media"
    elif count == 1:
        return "Baja"
    else:
        return ""

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
        return ""