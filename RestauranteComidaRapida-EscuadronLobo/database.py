# ==========================================================
# Módulo de Base de Datos:
# Configura las credenciales de conexión con PostgreSQL, define funciones auxiliares
# para ejecutar consultas SQL e inicializa las tablas del sistema del restaurante.
# ==========================================================

import os
import psycopg

from psycopg.rows import dict_row

# Configuración de la conexión.
# Los parámetros se obtienen desde variables de entorno,
# utilizando valores por defecto cuando no están definidos.
DB_CONFIG = {
    "host":     os.environ.get("PGHOST",     "localhost"),
    "dbname":   os.environ.get("PGDATABASE", "restaurante_escuadronlobo"),
    "user":     os.environ.get("PGUSER",     "postgres"),
    "password": os.environ.get("PGPASSWORD", "admin"),
    "port":     int(os.environ.get("PGPORT", "5432")),
}


# ==========================================================
# Crea y devuelve una conexión activa a PostgreSQL.
# ==========================================================
def get_connection():
    """Establece y retorna una conexión activa con la base de datos PostgreSQL."""
    return psycopg.connect(**DB_CONFIG)


# ==========================================================
# Ejecuta una sentencia SQL utilizando una conexión abierta.
#
# Parámetros:
#   conn   : conexión activa a PostgreSQL.
#   sql    : consulta SQL a ejecutar.
#   params : parámetros asociados a la consulta.
#
# Retorna:
#   Cursor configurado para devolver los resultados como
#   diccionarios (nombre_columna -> valor).
# ==========================================================
def execute(conn, sql, params=()):
    """Crea un cursor que devuelve filas como diccionarios y ejecuta la consulta SQL."""
    cur = conn.cursor(row_factory=dict_row)
    cur.execute(sql, params)
    return cur


# ==========================================================
# Inicializa el esquema de la base de datos.
# Crea todas las tablas requeridas por el sistema en caso
# de que aún no existan.
# ==========================================================
def init_db():
    """Inicializa la base de datos creando las tablas del sistema si no existen."""
    # Establece la conexión y crea el cursor de trabajo.
    conn = get_connection()
    cur = conn.cursor()

    # Definición de las sentencias SQL necesarias para crear
    # la estructura de la base de datos.
    statements = [

        # Almacena la información de los usuarios y sus roles.
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id          SERIAL PRIMARY KEY,
            nombre      TEXT NOT NULL,
            usuario     TEXT UNIQUE NOT NULL,
            contrasena  TEXT NOT NULL,
            rol         TEXT NOT NULL CHECK(
                rol IN ('admin', 'mozo', 'cocinero', 'cliente')
            )
        )
        """,

        # Gestiona el inventario de ingredientes disponibles.
        """
        CREATE TABLE IF NOT EXISTS ingredientes (
            id       SERIAL PRIMARY KEY,
            nombre   TEXT UNIQUE NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            minimo   INTEGER NOT NULL DEFAULT 0
        )
        """,

        # Contiene el catálogo de productos ofrecidos.
        """
        CREATE TABLE IF NOT EXISTS productos (
            id         SERIAL PRIMARY KEY,
            nombre     TEXT NOT NULL,
            categoria  TEXT NOT NULL CHECK(
                categoria IN (
                    'hamburguesa',
                    'pizza',
                    'acompanamiento',
                    'bebida'
                )
            ),
            variante   TEXT,
            precio     NUMERIC(10,2) NOT NULL,
            disponible BOOLEAN NOT NULL DEFAULT TRUE
        )
        """,

        # Relaciona cada producto con los ingredientes que lo componen.
        """
        CREATE TABLE IF NOT EXISTS producto_ingredientes (
            producto_id    INTEGER NOT NULL,
            ingrediente_id INTEGER NOT NULL,
            cantidad       INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (producto_id, ingrediente_id),
            FOREIGN KEY (producto_id)
                REFERENCES productos(id),
            FOREIGN KEY (ingrediente_id)
                REFERENCES ingredientes(id)
        )
        """,

        # Registra las órdenes realizadas en el restaurante.
        """
        CREATE TABLE IF NOT EXISTS ordenes (
            id         SERIAL PRIMARY KEY,
            cliente_id INTEGER,
            mozo_id    INTEGER,
            mesa       INTEGER NOT NULL,
            estado     TEXT NOT NULL DEFAULT 'pendiente'
                         CHECK(
                            estado IN (
                                'pendiente',
                                'preparando',
                                'listo',
                                'entregado'
                            )
                         ),
            total      NUMERIC(10,2) NOT NULL DEFAULT 0,
            creado_en  TIMESTAMP NOT NULL DEFAULT NOW(),
            FOREIGN KEY (cliente_id)
                REFERENCES usuarios(id),
            FOREIGN KEY (mozo_id)
                REFERENCES usuarios(id)
        )
        """,

        # Almacena el detalle de productos asociados a cada orden.
        """
        CREATE TABLE IF NOT EXISTS orden_items (
            id          SERIAL PRIMARY KEY,
            orden_id    INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad    INTEGER NOT NULL DEFAULT 1,
            subtotal    NUMERIC(10,2) NOT NULL,
            FOREIGN KEY (orden_id)
                REFERENCES ordenes(id),
            FOREIGN KEY (producto_id)
                REFERENCES productos(id)
        )
        """,

        # Registra el historial de ventas del sistema.
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id       SERIAL PRIMARY KEY,
            orden_id INTEGER NOT NULL,
            total    NUMERIC(10,2) NOT NULL,
            fecha    TIMESTAMP NOT NULL DEFAULT NOW(),
            FOREIGN KEY (orden_id)
                REFERENCES ordenes(id)
        )
        """,
    ]

    # Ejecuta cada sentencia SQL definida anteriormente.
    for stmt in statements:
        cur.execute(stmt)

    # Confirma los cambios realizados y libera los recursos utilizados.
    conn.commit()
    conn.close()