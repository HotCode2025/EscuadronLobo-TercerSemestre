from database import get_connection, execute


def get_productos_por_categoria(categoria):
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM productos WHERE categoria = %s AND disponible = TRUE ORDER BY nombre, variante",
        (categoria,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def crear_orden(mesa, items, mozo_id=None, cliente_id=None):
    """
    items: lista de {"producto_id": int, "cantidad": int, "subtotal": float}
    Retorna el id de la orden creada.
    """
    total = sum(i["subtotal"] for i in items)
    conn = get_connection()

    cur = execute(
        conn,
        "INSERT INTO ordenes (cliente_id, mozo_id, mesa, total) VALUES (%s,%s,%s,%s) RETURNING id",
        (cliente_id, mozo_id, mesa, total),
    )
    orden_id = cur.fetchone()["id"]

    for item in items:
        execute(
            conn,
            "INSERT INTO orden_items (orden_id, producto_id, cantidad, subtotal) VALUES (%s,%s,%s,%s)",
            (orden_id, item["producto_id"], item["cantidad"], item["subtotal"]),
        )

    conn.commit()
    conn.close()
    return orden_id


def get_ordenes_activas():
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE estado != 'entregado' ORDER BY creado_en",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ordenes_listas():
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE estado = 'listo' ORDER BY creado_en",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_items_orden(orden_id):
    conn = get_connection()
    rows = execute(
        conn,
        """
        SELECT oi.cantidad, oi.subtotal, p.nombre, p.variante
        FROM orden_items oi
        JOIN productos p ON p.id = oi.producto_id
        WHERE oi.orden_id = %s
        """,
        (orden_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def entregar_orden(orden_id):
    conn = get_connection()
    execute(conn, "UPDATE ordenes SET estado = 'entregado' WHERE id = %s", (orden_id,))
    total = execute(
        conn, "SELECT total FROM ordenes WHERE id = %s", (orden_id,)
    ).fetchone()["total"]
    execute(conn, "INSERT INTO ventas (orden_id, total) VALUES (%s,%s)", (orden_id, total))
    conn.commit()
    conn.close()


def mesa_tiene_orden_activa(mesa):
    conn = get_connection()
    row = execute(
        conn,
        "SELECT id FROM ordenes WHERE mesa = %s AND estado != 'entregado'",
        (mesa,),
    ).fetchone()
    conn.close()
    return row is not None


def verificar_stock(items):
    """
    items: lista de {"producto_id": int, "cantidad": int}
    Retorna lista de {"nombre": str, "necesario": int, "disponible": int}
    para ingredientes con stock insuficiente. Lista vacía = todo OK.
    """
    conn = get_connection()
    necesario = {}

    for item in items:
        ingredientes = execute(
            conn,
            """
            SELECT i.id, i.nombre, pi.cantidad AS por_unidad
            FROM producto_ingredientes pi
            JOIN ingredientes i ON i.id = pi.ingrediente_id
            WHERE pi.producto_id = %s
            """,
            (item["producto_id"],),
        ).fetchall()
        for ing in ingredientes:
            ing_id = ing["id"]
            if ing_id not in necesario:
                necesario[ing_id] = {"nombre": ing["nombre"], "total": 0}
            necesario[ing_id]["total"] += ing["por_unidad"] * item["cantidad"]

    faltantes = []
    for ing_id, data in necesario.items():
        stock = execute(
            conn, "SELECT cantidad FROM ingredientes WHERE id = %s", (ing_id,)
        ).fetchone()["cantidad"]
        if stock < data["total"]:
            faltantes.append({
                "nombre":     data["nombre"],
                "necesario":  data["total"],
                "disponible": stock,
            })

    conn.close()
    return faltantes


def get_estado_mesas(total_mesas=6):
    conn = get_connection()
    mesas = []
    for num in range(1, total_mesas + 1):
        orden = execute(
            conn,
            "SELECT id, estado FROM ordenes WHERE mesa = %s AND estado != 'entregado'",
            (num,),
        ).fetchone()
        if orden:
            mesas.append({"mesa": num, "libre": False, "orden_id": orden["id"], "estado": orden["estado"]})
        else:
            mesas.append({"mesa": num, "libre": True, "orden_id": None, "estado": None})
    conn.close()
    return mesas


def cancelar_orden(orden_id):
    conn = get_connection()
    execute(conn, "DELETE FROM orden_items WHERE orden_id = %s", (orden_id,))
    execute(conn, "DELETE FROM ordenes WHERE id = %s", (orden_id,))
    conn.commit()
    conn.close()


def get_orden_por_id(orden_id):
    conn = get_connection()
    row = execute(conn, "SELECT * FROM ordenes WHERE id = %s", (orden_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_ordenes_por_estado(estado):
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE estado = %s ORDER BY creado_en",
        (estado,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ordenes_cliente(cliente_id):
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE cliente_id = %s ORDER BY creado_en DESC",
        (cliente_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def cambiar_estado(orden_id, nuevo_estado):
    conn = get_connection()
    execute(conn, "UPDATE ordenes SET estado = %s WHERE id = %s", (nuevo_estado, orden_id))
    conn.commit()
    conn.close()


def marcar_listo(orden_id):
    conn = get_connection()

    items = execute(
        conn,
        "SELECT producto_id, cantidad FROM orden_items WHERE orden_id = %s",
        (orden_id,),
    ).fetchall()

    for item in items:
        ingredientes = execute(
            conn,
            "SELECT ingrediente_id, cantidad FROM producto_ingredientes WHERE producto_id = %s",
            (item["producto_id"],),
        ).fetchall()
        for ing in ingredientes:
            execute(
                conn,
                "UPDATE ingredientes SET cantidad = GREATEST(0, cantidad - %s) WHERE id = %s",
                (ing["cantidad"] * item["cantidad"], ing["ingrediente_id"]),
            )

    execute(conn, "UPDATE ordenes SET estado = 'listo' WHERE id = %s", (orden_id,))
    conn.commit()

    alertas = execute(
        conn,
        "SELECT nombre, cantidad, minimo FROM ingredientes WHERE cantidad <= minimo",
    ).fetchall()
    conn.close()

    return [dict(a) for a in alertas]
