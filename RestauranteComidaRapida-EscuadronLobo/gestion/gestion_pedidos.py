#Módulo de Gestión de Pedidos: Administra todo el ciclo de vida de los pedidos (creación, cambio de estado,
#entrega y cancelación) y realiza la verificación y descuento del stock de ingredientes.

from database import get_connection, execute

def get_productos_por_categoria(categoria): 
    # Trae los productos disponibles de una categoría, ya ordenados (ORDER BY nombre, variante) y filtrados por disponible = TRUE directo en la consulta
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM productos WHERE categoria = %s AND disponible = TRUE ORDER BY nombre, variante",
        (categoria,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def crear_orden(mesa, items, mozo_id=None, cliente_id=None):   
    # Calcula el total sumando los subtotales
    total = sum(i["subtotal"] for i in items) 
    conn = get_connection()

    # Inserta la orden con INSERT ... RETURNING id para recuperar el ID recién creado,
    cur = execute(
        conn,
        "INSERT INTO ordenes (cliente_id, mozo_id, mesa, total) VALUES (%s,%s,%s,%s) RETURNING id", 
        (cliente_id, mozo_id, mesa, total),
    )
    orden_id = cur.fetchone()["id"]
    
    # y con ese ID, inserta cada ítem en orden_items dentro de la misma conexión, cerrando todo con un solo commit() — es decir, la orden y sus ítems se guardan como una unidad.
    for item in items:
        execute(
            conn,
            "INSERT INTO orden_items (orden_id, producto_id, cantidad, subtotal) VALUES (%s,%s,%s,%s)",
            (orden_id, item["producto_id"], item["cantidad"], item["subtotal"]),
        )

    conn.commit()
    conn.close()
    return orden_id

def verifica_stock(items): 
    # Se crea un diccionario 'necesario' para llevar la cuenta de cuánto stock se necesita en total
    conn = get_connection()
    necesario = {}
    
    # Por cada producto del carrito, busca su receta con un JOIN entre producto_ingredientes e ingredientes
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
            # Va acumulando en el diccionario 'necesario' cuánto se necesita de cada ingrediente, multiplicando la cantidad de la receta por la cantidad pedida
            necesario[ing_id]["total"] += ing["por_unidad"] * item["cantidad"]

    faltantes = [] # lista para guardar los ingredientes faltantes
    # Luego compara ese total contra el stock real de cada ingrediente
    for ing_id, data in necesario.items():
        # Busca el stock real del ingrediente
        stock = execute(
            conn, "SELECT cantidad FROM ingredientes WHERE id = %s", (ing_id,)
        ).fetchone()["cantidad"]
        
        # Si el stock es menor al necesario, se agrega a la lista de faltantes
        if stock < data["total"]:
            faltantes.append({
                "nombre":     data["nombre"],
                "necesario":  data["total"],
                "disponible": stock,
            })    
    # Esto es lo que evita que se cree un pedido imposible de preparar — se valida antes de tocar la tabla 'ordenes'
    conn.close()
    return faltantes

def cambiar_estado(orden_id, nuevo_estado):
    # Actualiza el estado de preparación o entrega de una orden.
    conn = get_connection()
    # un simple UPDATE ordenes SET estado = %s — lo usa el cocinero para pasar de "pendiente" a "preparando".
    execute(conn, "UPDATE ordenes SET estado = %s WHERE id = %s", (nuevo_estado, orden_id)) 
    conn.commit()
    conn.close()

def marcar_listo(orden_id):
    # Marca una orden como lista, descuenta los ingredientes del stock y comprueba si algún ingrediente quedó bajo el mínimo.
    conn = get_connection()
    # busca los ítems de la orden y, para cada uno, su receta
    items = execute(
        conn,
        "SELECT producto_id, cantidad FROM orden_items WHERE orden_id = %s",
        (orden_id,),
    ).fetchall()
    # Itera sobre cada producto de la orden para ajustar el stock
    for item in items:
        ingredientes = execute(
            conn,
            "SELECT ingrediente_id, cantidad FROM producto_ingredientes WHERE producto_id = %s",
            (item["producto_id"],),
        ).fetchall()
        # descuenta el stock de cada ingrediente
        for ing in ingredientes:
            execute(
                conn,
                "UPDATE ingredientes SET cantidad = GREATEST(0, cantidad - %s) WHERE id = %s", 
                (ing["cantidad"] * item["cantidad"], ing["ingrediente_id"]),
            )
    # Cambia el estado de la orden a 'listo'
    execute(conn, "UPDATE ordenes SET estado = 'listo' WHERE id = %s", (orden_id,)) 
    conn.commit()
    # Consulta qué ingredientes quedaron en alerta (WHERE cantidad <= minimo) para devolver esa lista — 
    # así el cocinero se entera al instante si algo se está por terminar.
    alertas = execute(
        conn,
        "SELECT nombre, cantidad, minimo FROM ingredientes WHERE cantidad <= minimo", 
    ).fetchall()
    conn.close()

    return [dict(a) for a in alertas]

def entregar_orden(orden_id):
    # Marca la orden como 'entregada' y registra su total en la tabla de ventas
    conn = get_connection()
    execute(conn, "UPDATE ordenes SET estado = 'entregado' WHERE id = %s", (orden_id,))
    total = execute(
        conn, "SELECT total FROM ordenes WHERE id = %s", (orden_id,)
    ).fetchone()["total"]
    # inserta el registro en ventas con el total de la orden — 
    # este es el puente exacto con la parte de Juan: acá nace cada venta que después él va a reportar
    execute(conn, "INSERT INTO ventas (orden_id, total) VALUES (%s,%s)", (orden_id, total))
    conn.commit()
    conn.close()    

def mesa_tiene_orden_activa(mesa):
    # Verifica si una mesa en particular tiene algún pedido en proceso o no entregado
    conn = get_connection()
    row = execute(
        conn,
        "SELECT id FROM ordenes WHERE mesa = %s AND estado != 'entregado'",
        (mesa,),
    ).fetchone()
    conn.close()
    return row is not None

def get_estado_mesas(total_mesas=6):
    # Consulta y retorna el estado de ocupación y preparación de cada una de las mesas
    # recorre las 6 mesas y, para cada una, consulta si tiene una orden activa — 
    # la función que arma la pantalla de "estado de mesas" que va a mostrar Valentín
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
    # Elimina físicamente la orden y todos sus ítems asociados de la base de datos
    # borra primero orden_items y después ordenes — 
    conn = get_connection()
    execute(conn, "DELETE FROM orden_items WHERE orden_id = %s", (orden_id,))
    execute(conn, "DELETE FROM ordenes WHERE id = %s", (orden_id,))
    conn.commit()
    conn.close()

def get_ordenes_activas():
    # Devuelve una lista con todas las ordenes donde estado NO sea 'entregado'
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE estado != 'entregado' ORDER BY creado_en",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_ordenes_listas():
    # Devuelve una lista con todas las ordenes donde estado sea 'listo'
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE estado = 'listo' ORDER BY creado_en",
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_items_orden(orden_id):
    # Devuelve el detalle de productos, cantidades y subtotales asociados a una orden
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

# get_ordenes_por_estado, get_ordenes_cliente, get_orden_por_id se reutilizan en varios módulos (cliente, cocinero y mozo).
def get_orden_por_id(orden_id):
    # Obtiene una orden de la base de datos filtrada por su identificador único (ID)
    conn = get_connection()
    row = execute(conn, "SELECT * FROM ordenes WHERE id = %s", (orden_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

def get_ordenes_por_estado(estado):
    # Obtiene todas las órdenes registradas filtradas por un estado específico.
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE estado = %s ORDER BY creado_en",
        (estado,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_ordenes_cliente(cliente_id):
    # Obtiene el historial completo de órdenes de un cliente ordenadas por fecha descendente.
    conn = get_connection()
    rows = execute(
        conn,
        "SELECT * FROM ordenes WHERE cliente_id = %s ORDER BY creado_en DESC",
        (cliente_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]



