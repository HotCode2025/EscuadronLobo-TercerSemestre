from database import init_db, get_connection, execute
from gestion.gestion_usuarios import hash_password


# ─────────────────────────────────────────────
#  USUARIOS
# ─────────────────────────────────────────────
USUARIOS = [
    ("Admin",            "admin",    "admin123",   "admin"),
    ("Mario Mozo",       "mozo1",    "mozo123",    "mozo"),
    ("Maria Cocinera",   "cocina1",  "cocina123",  "cocinero"),
    ("Carlos Cliente",   "cliente1", "cliente123", "cliente"),
    ("Pedro Cliente",    "cliente2", "cliente123", "cliente"),
]


# ─────────────────────────────────────────────
#  INGREDIENTES  (nombre, cantidad, minimo)
# ─────────────────────────────────────────────
INGREDIENTES = [
    # Hamburguesas
    ("Pan",              100, 20),
    ("Carne",             80, 15),
    ("Queso",             80, 15),
    ("Lechuga",           60, 10),
    ("Tomate",            60, 10),
    ("Huevo",             50, 10),
    ("Panceta",           50, 10),
    ("Salsa BBQ",        100, 20),
    ("Pollo",             60, 10),
    ("Medallon vegetal",  40, 10),
    ("Mayonesa",         150, 30),
    ("Mostaza",          150, 30),
    # Pizzas
    ("Masa pizza",        80, 15),
    ("Salsa tomate",     100, 20),
    ("Mozzarella",       100, 20),
    ("Albahaca",          50, 10),
    ("Pepperoni",         50, 10),
    ("Ajo",               80, 15),
    ("Oregano",           80, 15),
    ("Roquefort",         40, 10),
    ("Parmesano",         40, 10),
    ("Queso extra",       60, 10),
    ("Jamon",             60, 10),
    ("Anana",             40, 10),
    ("Cebolla",           60, 10),
    ("Salami",            50, 10),
    ("Verduras variadas", 60, 10),
    # Acompañamientos
    ("Papa",             150, 30),
    ("Aceite",           100, 20),
    ("Sal",              200, 30),
    ("Rebozado",          80, 15),
    ("Masa empanada",     60, 10),
    # Bebidas (stock 25, minimo 15)
    ("CocaCola_P",  25, 15),
    ("CocaCola_M",  25, 15),
    ("CocaCola_G",  25, 15),
    ("Pepsi_P",     25, 15),
    ("Pepsi_M",     25, 15),
    ("Pepsi_G",     25, 15),
    ("Fanta_P",     25, 15),
    ("Fanta_M",     25, 15),
    ("Fanta_G",     25, 15),
    ("Sprite_P",    25, 15),
    ("Sprite_M",    25, 15),
    ("Sprite_G",    25, 15),
    ("Mirinda_P",   25, 15),
    ("Mirinda_M",   25, 15),
    ("Mirinda_G",   25, 15),
]


# ─────────────────────────────────────────────
#  PRODUCTOS  (nombre, categoria, variante, precio)
#  + lista de (ingrediente, cantidad)
# ─────────────────────────────────────────────
PRODUCTOS = [
    # ── HAMBURGUESAS ──────────────────────────
    ("Simple",          "hamburguesa", None, 1725, [
        ("Pan", 1), ("Carne", 1), ("Mayonesa", 1), ("Mostaza", 1),
    ]),
    ("Cheeseburger",    "hamburguesa", None, 2070, [
        ("Pan", 1), ("Carne", 1), ("Queso", 1), ("Mayonesa", 1), ("Mostaza", 1),
    ]),
    ("Doble",           "hamburguesa", None, 3105, [
        ("Pan", 1), ("Carne", 2), ("Queso", 2), ("Mayonesa", 1), ("Mostaza", 1),
    ]),
    ("Completa",        "hamburguesa", None, 3795, [
        ("Pan", 1), ("Carne", 1), ("Queso", 1), ("Lechuga", 1),
        ("Tomate", 1), ("Huevo", 1), ("Mayonesa", 1),
    ]),
    ("Bacon",           "hamburguesa", None, 4140, [
        ("Pan", 1), ("Carne", 1), ("Queso", 1), ("Panceta", 1), ("Mayonesa", 1),
    ]),
    ("BBQ",             "hamburguesa", None, 4140, [
        ("Pan", 1), ("Carne", 1), ("Queso", 1), ("Salsa BBQ", 1),
    ]),
    ("Pollo",           "hamburguesa", None, 3450, [
        ("Pan", 1), ("Pollo", 1), ("Lechuga", 1), ("Mayonesa", 1),
    ]),
    ("Vegetariana",     "hamburguesa", None, 3450, [
        ("Pan", 1), ("Medallon vegetal", 1), ("Lechuga", 1), ("Tomate", 1),
    ]),

    # ── PIZZAS ────────────────────────────────
    ("Margarita",       "pizza", None, 4140, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1), ("Albahaca", 1),
    ]),
    ("Pepperoni",       "pizza", None, 4830, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1), ("Pepperoni", 1),
    ]),
    ("Napolitana",      "pizza", None, 4140, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1),
        ("Ajo", 1), ("Oregano", 1),
    ]),
    ("4 Quesos",        "pizza", None, 5175, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1),
        ("Roquefort", 1), ("Parmesano", 1), ("Queso extra", 1),
    ]),
    ("Hawaiana",        "pizza", None, 4830, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1),
        ("Jamon", 1), ("Anana", 1),
    ]),
    ("Fugazzeta",       "pizza", None, 4485, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1),
        ("Cebolla", 1), ("Queso extra", 1),
    ]),
    ("Calabresa",       "pizza", None, 4830, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1), ("Salami", 1),
    ]),
    ("BBQ",             "pizza", None, 5175, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1),
        ("Carne", 1), ("Salsa BBQ", 1),
    ]),
    ("Vegetariana",     "pizza", None, 4485, [
        ("Masa pizza", 1), ("Salsa tomate", 1), ("Mozzarella", 1),
        ("Verduras variadas", 1),
    ]),

    # ── ACOMPAÑAMIENTOS ───────────────────────
    ("Papas Fritas",    "acompanamiento", "Pequeño", 1380, [
        ("Papa", 1), ("Aceite", 1), ("Sal", 1),
    ]),
    ("Papas Fritas",    "acompanamiento", "Mediano",  1725, [
        ("Papa", 2), ("Aceite", 1), ("Sal", 1),
    ]),
    ("Papas Fritas",    "acompanamiento", "Grande",   2070, [
        ("Papa", 3), ("Aceite", 2), ("Sal", 1),
    ]),
    ("Aros de Cebolla", "acompanamiento", "Pequeño", 1380, [
        ("Cebolla", 1), ("Rebozado", 1), ("Aceite", 1), ("Sal", 1),
    ]),
    ("Aros de Cebolla", "acompanamiento", "Mediano",  1725, [
        ("Cebolla", 2), ("Rebozado", 1), ("Aceite", 1), ("Sal", 1),
    ]),
    ("Aros de Cebolla", "acompanamiento", "Grande",   2070, [
        ("Cebolla", 3), ("Rebozado", 2), ("Aceite", 2), ("Sal", 1),
    ]),
    ("Empanada",        "acompanamiento", "Carne",           1380, [
        ("Masa empanada", 1), ("Carne", 1), ("Cebolla", 1),
    ]),
    ("Empanada",        "acompanamiento", "Pollo",           1380, [
        ("Masa empanada", 1), ("Pollo", 1),
    ]),
    ("Empanada",        "acompanamiento", "Jamon y Queso",   1380, [
        ("Masa empanada", 1), ("Jamon", 1), ("Queso", 1),
    ]),

    # ── BEBIDAS ───────────────────────────────
    ("Coca-Cola", "bebida", "Pequeño", 1380, [("CocaCola_P", 1)]),
    ("Coca-Cola", "bebida", "Mediano",  1725, [("CocaCola_M", 1)]),
    ("Coca-Cola", "bebida", "Grande",   2070, [("CocaCola_G", 1)]),
    ("Pepsi",     "bebida", "Pequeño", 1380, [("Pepsi_P", 1)]),
    ("Pepsi",     "bebida", "Mediano",  1725, [("Pepsi_M", 1)]),
    ("Pepsi",     "bebida", "Grande",   2070, [("Pepsi_G", 1)]),
    ("Fanta",     "bebida", "Pequeño", 1380, [("Fanta_P", 1)]),
    ("Fanta",     "bebida", "Mediano",  1725, [("Fanta_M", 1)]),
    ("Fanta",     "bebida", "Grande",   2070, [("Fanta_G", 1)]),
    ("Sprite",    "bebida", "Pequeño", 1380, [("Sprite_P", 1)]),
    ("Sprite",    "bebida", "Mediano",  1725, [("Sprite_M", 1)]),
    ("Sprite",    "bebida", "Grande",   2070, [("Sprite_G", 1)]),
    ("Mirinda",   "bebida", "Pequeño", 1380, [("Mirinda_P", 1)]),
    ("Mirinda",   "bebida", "Mediano",  1725, [("Mirinda_M", 1)]),
    ("Mirinda",   "bebida", "Grande",   2070, [("Mirinda_G", 1)]),
]


# ─────────────────────────────────────────────
#  CARGA
# ─────────────────────────────────────────────
def seed():
    init_db()
    conn = get_connection()

    # Evitar duplicados
    if execute(conn, "SELECT COUNT(*) AS n FROM usuarios").fetchone()["n"] > 0:
        print("La base de datos ya tiene datos. Seed omitido.")
        conn.close()
        return

    # Usuarios
    for nombre, usuario, contrasena, rol in USUARIOS:
        execute(
            conn,
            "INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES (%s,%s,%s,%s)",
            (nombre, usuario, hash_password(contrasena), rol),
        )

    # Ingredientes
    for nombre, cantidad, minimo in INGREDIENTES:
        execute(
            conn,
            "INSERT INTO ingredientes (nombre, cantidad, minimo) VALUES (%s,%s,%s)",
            (nombre, cantidad, minimo),
        )

    # Productos + relaciones ingredientes
    for nombre, categoria, variante, precio, ingredientes in PRODUCTOS:
        cur = execute(
            conn,
            "INSERT INTO productos (nombre, categoria, variante, precio) VALUES (%s,%s,%s,%s) RETURNING id",
            (nombre, categoria, variante, precio),
        )
        producto_id = cur.fetchone()["id"]

        for ing_nombre, cantidad in ingredientes:
            ing = execute(
                conn,
                "SELECT id FROM ingredientes WHERE nombre = %s",
                (ing_nombre,),
            ).fetchone()
            if ing:
                execute(
                    conn,
                    "INSERT INTO producto_ingredientes (producto_id, ingrediente_id, cantidad) VALUES (%s,%s,%s)",
                    (producto_id, ing["id"], cantidad),
                )

    conn.commit()
    conn.close()
    print("Seed completado.")
    print(f"  {len(USUARIOS)} usuarios")
    print(f"  {len(INGREDIENTES)} ingredientes")
    print(f"  {len(PRODUCTOS)} productos")


if __name__ == "__main__":
    seed()
