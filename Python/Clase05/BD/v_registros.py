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
            # SENTENCIA SQL SELECT CON IN
            # Permite buscar múltiples registros utilizando
            # varios id_persona al mismo tiempo.
            # --------------------------------------------------
            sentencia = 'SELECT * FROM persona WHERE id_persona IN %s'

            # Solicita al usuario los IDs a consultar
            entrada = input(
                'Digite los id_persona a buscar (separados por coma): '
            )

            # Convierte la entrada del usuario en una tupla
            # para ser utilizada en la cláusula IN
            llaves_primarias = (
                tuple(entrada.split(', ')),
            )

            # Ejecución de la consulta SQL
            cursor.execute(sentencia, llaves_primarias)

            # Recupera todos los registros encontrados
            registros = cursor.fetchall()

            # Recorre e imprime cada registro obtenido
            for registro in registros:
                print(registro)

            # cursor.fetchone() podría utilizarse si se
            # esperara obtener un único registro


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