# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

# Permite conectarse y trabajar con bases de datos PostgreSQL
import psycopg2


# ==========================================================
# CONFIGURACIÓN DE LA CONEXIÓN A LA BASE DE DATOS
# ==========================================================

# Se establece la conexión con el servidor PostgreSQL
conexion = psycopg2.connect(
    user='postgres',          # Usuario de la base de datos
    password='admin',         # Contraseña del usuario
    host='127.0.0.1',         # Dirección IP del servidor
    port='5432',              # Puerto de PostgreSQL
    database='test_bd',       # Nombre de la base de datos
    client_encoding='utf8'    # Codificación de caracteres
)

# print(conexion)  # Utilizado para verificar que la conexión fue exitosa


# ==========================================================
# BLOQUE PRINCIPAL DE EJECUCIÓN
# ==========================================================

try:

    # El contexto "with conexion" administra automáticamente
    # la transacción (commit o rollback según corresponda)
    with conexion:

        # Creación del cursor para ejecutar instrucciones SQL
        with conexion.cursor() as cursor:

            # --------------------------------------------------
            # SENTENCIA SQL DELETE
            # Elimina un registro de la tabla persona según
            # el id_persona indicado por el usuario.
            # --------------------------------------------------
            sentencia = 'DELETE FROM persona WHERE id_persona=%s'

            # Solicita el ID del registro a eliminar
            entrada = input(
                'Digite el número de registro que desee eliminar: '
            )

            # Valor que será enviado como parámetro a la consulta
            valores = (entrada)

            # Ejecución de la sentencia SQL
            cursor.execute(sentencia, valores)

            # Obtiene la cantidad de registros eliminados
            registros_eliminados = cursor.rowcount

            # Muestra el resultado de la operación
            print(
                f'Los registros eliminados son: '
                f'{registros_eliminados}'
            )


# ==========================================================
# MANEJO DE EXCEPCIONES
# ==========================================================

except Exception as e:
    print(f'Ocurrió un error: {e}')


# ==========================================================
# CIERRE DE RECURSOS
# ==========================================================

finally:

    # Cierra la conexión con la base de datos
    conexion.close()