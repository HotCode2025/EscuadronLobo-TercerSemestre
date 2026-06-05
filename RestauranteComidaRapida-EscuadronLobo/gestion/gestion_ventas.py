from database import get_connection, execute


def get_ventas_hoy():
    conn = get_connection()
    rows = execute(
        conn,
        """
        SELECT v.id, v.total, v.fecha, v.orden_id, o.mesa
        FROM ventas v
        JOIN ordenes o ON o.id = v.orden_id
        WHERE DATE(v.fecha) = CURRENT_DATE
        ORDER BY v.fecha
        """,
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ventas_por_fecha(fecha):
    """fecha: string 'YYYY-MM-DD'"""
    conn = get_connection()
    rows = execute(
        conn,
        """
        SELECT v.id, v.total, v.fecha, v.orden_id, o.mesa
        FROM ventas v
        JOIN ordenes o ON o.id = v.orden_id
        WHERE DATE(v.fecha) = %s
        ORDER BY v.fecha
        """,
        (fecha,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_items_venta(orden_id):
    conn = get_connection()
    rows = execute(
        conn,
        """
        SELECT oi.cantidad, p.nombre, p.variante
        FROM orden_items oi
        JOIN productos p ON p.id = oi.producto_id
        WHERE oi.orden_id = %s
        """,
        (orden_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_resumen_ventas():
    conn = get_connection()
    row = execute(
        conn,
        """
        SELECT
            COUNT(*)                                                             AS total_ventas,
            COALESCE(SUM(total), 0)                                              AS total_recaudado,
            COALESCE(SUM(CASE WHEN DATE(fecha) = CURRENT_DATE THEN total END), 0) AS hoy
        FROM ventas
        """,
    ).fetchone()
    conn.close()
    return dict(row)
