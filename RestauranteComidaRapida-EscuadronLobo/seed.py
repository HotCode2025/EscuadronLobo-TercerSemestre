# Importa funciones para inicializar la base de datos,
# obtener conexiones y ejecutar consultas SQL.
from database import init_db, get_connection, execute

# Importa la función encargada de cifrar las contraseñas
# antes de almacenarlas en la base de datos.
from gestion.gestion_usuarios import hash_password


# ==========================================================
# DATOS INICIALES - USUARIOS
# ==========================================================
# Lista de usuarios que serán cargados automáticamente
# al ejecutar el proceso de inicialización (seed).

USUARIOS = [
    ("Admin",            "admin",    "admin123",   "admin"),
    ("Mario Mozo",       "mozo1",    "mozo123",    "mozo"),
    ("Maria Cocinera",   "cocina1",  "cocina123",  "cocinero"),
    ("Carlos Cliente",   "cliente1", "cliente123", "cliente"),
    ("Pedro Cliente",    "cliente2", "cliente123", "cliente"),
]


# ==========================================================
# DATOS INICIALES - INGREDIENTES
# ==========================================================
# Cada ingrediente contiene:
# (nombre, cantidad_stock, stock_minimo)

INGREDIENTES = [
    ...
]


# ==========================================================
# DATOS INICIALES - PRODUCTOS
# ==========================================================
# Estructura:
#
# (
#   nombre,
#   categoria,
#   variante,
#   precio,
#   [
#       (ingrediente, cantidad),
#       ...
#   ]
# )
#
# Cada producto tiene asociada una lista de ingredientes
# necesarios para su elaboración.

PRODUCTOS = [
    ...
]


# ==========================================================
# FUNCIÓN: seed
# ==========================================================
# Objetivo:
# Cargar información inicial en la base de datos.
#
# Esta función crea:
# - Usuarios
# - Ingredientes
# - Productos
# - Relaciones producto-ingrediente
#
# Solo se ejecutará si la base de datos se encuentra vacía.
# ==========================================================

def seed():

    # Garantiza que todas las tablas existan
    init_db()

    # Obtiene una conexión a PostgreSQL
    conn = get_connection()

    # ------------------------------------------------------
    # Verificación de datos existentes
    # ------------------------------------------------------
    # Evita insertar registros duplicados si la base
    # ya contiene información.
    # ------------------------------------------------------
    if execute(
        conn,
        "SELECT COUNT(*) AS n FROM usuarios"
    ).fetchone()["n"] > 0:

        print("La base de datos ya tiene datos. Seed omitido.")
        conn.close()
        return

    # ------------------------------------------------------
    # CARGA DE USUARIOS
    # ------------------------------------------------------
    # Inserta todos los usuarios predefinidos.
    # Las contraseñas se almacenan cifradas.
    # ------------------------------------------------------
    for nombre, usuario, contrasena, rol in USUARIOS:

        execute(
            conn,
            """
            INSERT INTO usuarios
            (nombre, usuario, contrasena, rol)
            VALUES (%s,%s,%s,%s)
            """,
            (
                nombre,
                usuario,
                hash_password(contrasena),
                rol
            ),
        )

    # ------------------------------------------------------
    # CARGA DE INGREDIENTES
    # ------------------------------------------------------
    # Inserta todos los ingredientes con su stock inicial
    # y su stock mínimo permitido.
    # ------------------------------------------------------
    for nombre, cantidad, minimo in INGREDIENTES:

        execute(
            conn,
            """
            INSERT INTO ingredientes
            (nombre, cantidad, minimo)
            VALUES (%s,%s,%s)
            """,
            (
                nombre,
                cantidad,
                minimo
            ),
        )

    # ------------------------------------------------------
    # CARGA DE PRODUCTOS
    # ------------------------------------------------------
    # Inserta cada producto y luego registra
    # los ingredientes asociados.
    # ------------------------------------------------------
    for nombre, categoria, variante, precio, ingredientes in PRODUCTOS:

        # Inserta el producto y obtiene el ID generado.
        cur = execute(
            conn,
            """
            INSERT INTO productos
            (nombre, categoria, variante, precio)
            VALUES (%s,%s,%s,%s)
            RETURNING id
            """,
            (
                nombre,
                categoria,
                variante,
                precio
            ),
        )

        # Recupera el ID recién generado.
        producto_id = cur.fetchone()["id"]

        # --------------------------------------------------
        # Asociación producto-ingrediente
        # --------------------------------------------------
        for ing_nombre, cantidad in ingredientes:

            # Busca el ID del ingrediente
            ing = execute(
                conn,
                """
                SELECT id
                FROM ingredientes
                WHERE nombre = %s
                """,
                (ing_nombre,),
            ).fetchone()

            # Si el ingrediente existe,
            # crea la relación correspondiente.
            if ing:

                execute(
                    conn,
                    """
                    INSERT INTO producto_ingredientes
                    (producto_id, ingrediente_id, cantidad)
                    VALUES (%s,%s,%s)
                    """,
                    (
                        producto_id,
                        ing["id"],
                        cantidad
                    ),
                )

    # ------------------------------------------------------
    # Confirmación de cambios
    # ------------------------------------------------------
    conn.commit()

    # Cierre de conexión
    conn.close()

    # ------------------------------------------------------
    # Resumen de carga realizada
    # ------------------------------------------------------
    print("Seed completado.")
    print(f"  {len(USUARIOS)} usuarios")
    print(f"  {len(INGREDIENTES)} ingredientes")
    print(f"  {len(PRODUCTOS)} productos")


# ==========================================================
# PUNTO DE ENTRADA DEL PROGRAMA
# ==========================================================
# Permite ejecutar este archivo directamente.
# ==========================================================

if __name__ == "__main__":
    seed()
