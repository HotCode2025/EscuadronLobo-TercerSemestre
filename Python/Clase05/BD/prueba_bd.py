# ==========================================================
# IMPORTACIÓN DE LIBRERÍAS
# ==========================================================

# Biblioteca que permite la conexión y manipulación de bases
# de datos PostgreSQL desde Python.
import psycopg2


# ==========================================================
# CONFIGURACIÓN DE LA CONEXIÓN
# ==========================================================

# Establece una conexión con la base de datos PostgreSQL.
conexion = psycopg2.connect(
    user='postgres',          # Usuario de PostgreSQL
    password='admin',         # Contraseña del usuario
    host='127.0.0.1',         # Dirección del servidor
    port='5432',              # Puerto por defecto de PostgreSQL
    database='test_bd',       # Base de datos a utilizar
    client_encoding='utf-8'   # Codificación de caracteres
)


# ==========================================================
# CONSULTA DE REGISTROS
# ==========================================================

try:

    # Administra automáticamente la transacción.
    # Si ocurre un error, realiza rollback.
    # Si todo sale correctamente, realiza commit.
    with conexion:

        # Creación del cursor para ejecutar consultas SQL.
        with conexion.cursor() as cursor:

            # --------------------------------------------------
            # CONSULTA PARAMETRIZADA
            # Busca una persona según su identificador.
            # --------------------------------------------------
            sentencia = '''
                SELECT *
                FROM persona
                WHERE id_persona = %s
            '''

            # Solicita al usuario el ID de la persona a consultar.
            id_persona = input(
                'Digite un número para el id_persona: '
            )

            # Ejecuta la consulta enviando el parámetro
            # mediante una tupla.
            cursor.execute(sentencia, (id_persona,))

            # Recupera un único registro de la consulta.
            registros = cursor.fetchone()

            # Muestra el resultado obtenido.
            print(registros)


# ==========================================================
# MANEJO DE EXCEPCIONES
# ==========================================================

except Exception as e:
    print(f'Ocurrió un error: {e}')


# ==========================================================
# LIBERACIÓN DE RECURSOS
# ==========================================================

finally:

    # Cierra la conexión con la base de datos.
    conexion.close()
