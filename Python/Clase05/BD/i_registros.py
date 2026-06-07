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
            # SENTENCIA SQL INSERT
            # Inserta un nuevo registro en la tabla persona
            # --------------------------------------------------
            sentencia = '''
                INSERT INTO persona (nombre, apellido, email)
                VALUES (%s, %s, %s)
            '''

            # Valores que serán insertados en la tabla
            valores = (
                'Axel',
                'Constantino',
                'axelconst@gmail.com'
            )

            # Ejecución de la sentencia SQL
            cursor.execute(sentencia, valores)

            # El bloque with realiza automáticamente el COMMIT
            # por lo que no es necesario ejecutar:
            # conexion.commit()

            # Obtiene la cantidad de registros afectados
            registros_insertados = cursor.rowcount

            # Muestra el resultado de la operación
            print(f'Los registros insertados son: {registros_insertados}')


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
