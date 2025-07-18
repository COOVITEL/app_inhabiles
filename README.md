## Actualizacion de registros

Para actualizar los registros de los asociados, se debe cargar el archivo excel o xlsx.
Este archivo es suministrado por el colaborador Cristian Molina del equipo de Planeacion.
El archivo debe tener el nombre "rentabilidad.xlsx" con el nombre de hoja Rentabilidad

Recuerde que este no debe cambiar su formato o nombre de las columnas.

Para actualizarlos ejecute o abra la vista con el nombre "created" o "seedAsociados" en la url: createAndUpdateAsociados/

Para validar su ejecucion puede hacerlo de forma local en su servidor, corriendo la aplicacion con el comando
""" python3 manage.py runserver """
Y en otra ventana putty correr el comando
""" curl http://127.0.0.1:8000/createAndUpdateAsociados/ """

Esto correra y actualizara el listado


### Envio archivo desde otro servidor

Para enviar el archvio puede hacerlo mediante el comando
""" scp -P 22 nombre_del_archivo usuario_servidor_final@IP:/home/ubicacion_final """
luego se pedira la password del usuario final o del servidor final