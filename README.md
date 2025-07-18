## 📄 Actualización de Registros de Asociados

Este módulo permite actualizar los registros de los asociados mediante un archivo Excel suministrado por el equipo de Planeación.

### 📥 Requisitos del archivo

- **Formato**: `.xlsx` (Excel)
- **Nombre del archivo**: `rentabilidad.xlsx`
- **Nombre de la hoja**: `Rentabilidad`
- **Importante**: No modificar el **nombre de las columnas** ni su **estructura**.

El archivo debe ser proporcionado por el colaborador **Cristian Molina** del equipo de Planeación.

---

### 🚀 ¿Cómo actualizar los registros?

1. Asegúrate de que el archivo esté ubicado correctamente en el servidor.
2. Ejecuta la vista correspondiente accediendo a la siguiente URL:


> También puedes acceder mediante los nombres de vista: `"created"` o `"seedAsociados"`.

---

### ⚙️ Ejecución local

1. Inicia el servidor local:

``` python3 manage.py runserver ```

y en otra ventana putty ejecute

```curl http://127.0.0.1:8000/createAndUpdateAsociados/```

### Envio del Archivo

```scp -P 22 nombre_del_archivo usuario@IP:/home/ubicacion_final```

