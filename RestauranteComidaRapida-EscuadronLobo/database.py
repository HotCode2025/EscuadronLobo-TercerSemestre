import psycopg
from psycopg.rows import dict_row

import os

DB_CONFIG = {
    "host":     os.environ.get("PGHOST",     "localhost"),
    "dbname":   os.environ.get("PGDATABASE", "restaurante_escuadronlobo"),
    "user":     os.environ.get("PGUSER",     "postgres"),
    "password": os.environ.get("PGPASSWORD", "1234"),
    "port":     int(os.environ.get("PGPORT", "5432")),
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


def execute(conn, sql, params=()):
    cur = conn.cursor(row_factory=dict_row)
    cur.execute(sql, params)
    return cur


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    statements = [
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id          SERIAL PRIMARY KEY,
            nombre      TEXT   NOT NULL,
            usuario     TEXT   UNIQUE NOT NULL,
            contrasena  TEXT   NOT NULL,
            rol         TEXT   NOT NULL CHECK(rol IN ('admin', 'mozo', 'cocinero', 'cliente'))
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ingredientes (
            id       SERIAL PRIMARY KEY,
            nombre   TEXT    UNIQUE NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 0,
            minimo   INTEGER NOT NULL DEFAULT 0
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS productos (
            id         SERIAL PRIMARY KEY,
            nombre     TEXT          NOT NULL,
            categoria  TEXT          NOT NULL CHECK(categoria IN ('hamburguesa', 'pizza', 'acompanamiento', 'bebida')),
            variante   TEXT,
            precio     NUMERIC(10,2) NOT NULL,
            disponible BOOLEAN       NOT NULL DEFAULT TRUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS producto_ingredientes (
            producto_id    INTEGER NOT NULL,
            ingrediente_id INTEGER NOT NULL,
            cantidad       INTEGER NOT NULL DEFAULT 1,
            PRIMARY KEY (producto_id, ingrediente_id),
            FOREIGN KEY (producto_id)    REFERENCES productos(id),
            FOREIGN KEY (ingrediente_id) REFERENCES ingredientes(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ordenes (
            id         SERIAL        PRIMARY KEY,
            cliente_id INTEGER,
            mozo_id    INTEGER,
            mesa       INTEGER       NOT NULL,
            estado     TEXT          NOT NULL DEFAULT 'pendiente'
                                     CHECK(estado IN ('pendiente', 'preparando', 'listo', 'entregado')),
            total      NUMERIC(10,2) NOT NULL DEFAULT 0,
            creado_en  TIMESTAMP     NOT NULL DEFAULT NOW(),
            FOREIGN KEY (cliente_id) REFERENCES usuarios(id),
            FOREIGN KEY (mozo_id)    REFERENCES usuarios(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orden_items (
            id          SERIAL        PRIMARY KEY,
            orden_id    INTEGER       NOT NULL,
            producto_id INTEGER       NOT NULL,
            cantidad    INTEGER       NOT NULL DEFAULT 1,
            subtotal    NUMERIC(10,2) NOT NULL,
            FOREIGN KEY (orden_id)    REFERENCES ordenes(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ventas (
            id       SERIAL        PRIMARY KEY,
            orden_id INTEGER       NOT NULL,
            total    NUMERIC(10,2) NOT NULL,
            fecha    TIMESTAMP     NOT NULL DEFAULT NOW(),
            FOREIGN KEY (orden_id) REFERENCES ordenes(id)
        )
        """,
    ]

    for stmt in statements:
        cur.execute(stmt)

    conn.commit()
    conn.close()
