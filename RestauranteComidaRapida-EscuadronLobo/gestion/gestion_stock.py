from database import get_connection, execute


def get_todos():
    conn = get_connection()
    rows = execute(conn, "SELECT * FROM ingredientes ORDER BY nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_alertas():
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ingredientes WHERE cantidad <= minimo ORDER BY nombre",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def ajustar_stock(ingrediente_id, cantidad):
    """cantidad puede ser positiva (agregar) o negativa (quitar). Nunca baja de 0."""
    conn = get_connection()
    execute(
        conn,
        "UPDATE ingredientes SET cantidad = GREATEST(0, cantidad + %s) WHERE id = %s",
        (cantidad, ingrediente_id),
    )
    conn.commit()
    conn.close()


def get_todos_productos():
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM productos ORDER BY categoria, nombre, variante",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def toggle_disponible(producto_id):
    conn = get_connection()
    execute(
        conn,
        "UPDATE productos SET disponible = NOT disponible WHERE id = %s",
        (producto_id,),
    )
    conn.commit()
    conn.close()
