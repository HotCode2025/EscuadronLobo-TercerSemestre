from gestion.gestion_pedidos import (
    get_productos_por_categoria,
    crear_orden,
    get_ordenes_activas,
    get_ordenes_listas,
    get_ordenes_por_estado,
    get_items_orden,
    entregar_orden,
    mesa_tiene_orden_activa,
    cancelar_orden,
    verificar_stock,
    get_estado_mesas,
)
from menus.utils import limpiar, separador, CATEGORIAS, cambiar_contrasena_ui

ESTADOS = {
    "pendiente":  "Pendiente",
    "preparando": "En preparación",
    "listo":      "Listo para entregar",
    "entregado":  "Entregado",
}


def mostrar_items(items):
    for it in items:
        nombre = it["nombre"]
        if it["variante"]:
            nombre += f" ({it['variante']})"
        print(f"    {it['cantidad']}x  {nombre:<28} ${it['subtotal']:.2f}")


class MenuMozo:
    def __init__(self, user):
        self.user = user

    # ──────────────────────────────────────────
    def ejecutar(self):
        while True:
            limpiar()
            print("=" * 44)
            print(f"  MOZO — {self.user['nombre']}")
            print("=" * 44)
            print("  1. Tomar pedido")
            print("  2. Estado de mesas")
            print("  3. Ver órdenes activas")
            print("  4. Entregar orden lista")
            print("  5. Cancelar orden pendiente")
            print("  6. Cambiar contraseña")
            print("  0. Cerrar sesión")
            print("=" * 44)

            op = input("  Opción: ").strip()

            if op == "1":
                self.tomar_pedido()
            elif op == "2":
                self.ver_mesas()
            elif op == "3":
                self.ver_ordenes_activas()
            elif op == "4":
                self.entregar_orden()
            elif op == "5":
                self.cancelar_orden()
            elif op == "6":
                cambiar_contrasena_ui(self.user)
            elif op == "0":
                break

    # ──────────────────────────────────────────
    def tomar_pedido(self):
        limpiar()
        print("=" * 44)
        print("  NUEVO PEDIDO")
        print("=" * 44)

        mesa = self._pedir_mesa()
        if mesa is None:
            return

        carrito = []

        while True:
            limpiar()
            print("=" * 44)
            print(f"  PEDIDO — Mesa {mesa}")
            separador()
            if carrito:
                mostrar_items(carrito)
                separador()
                total = sum(i["subtotal"] for i in carrito)
                print(f"  Total: ${total:.2f}")
                separador()

            print("  Categorías:")
            for i, (_, label) in enumerate(CATEGORIAS, 1):
                print(f"    {i}. {label}")
            print("  ─")
            print("    0. Confirmar y enviar pedido")
            print("=" * 44)

            op = input("  Opción: ").strip()

            if op == "0":
                if not carrito:
                    print("\n  El pedido está vacío.")
                    input("  Presiona Enter para continuar...")
                    return
                break

            if op in ("1", "2", "3", "4"):
                cat_key, cat_label = CATEGORIAS[int(op) - 1]
                self._agregar_producto(carrito, cat_key, cat_label)

        # Confirmar
        limpiar()
        print("=" * 44)
        print(f"  CONFIRMAR PEDIDO — Mesa {mesa}")
        separador()
        mostrar_items(carrito)
        separador()
        total = sum(i["subtotal"] for i in carrito)
        print(f"  Total: ${total:.2f}")
        print("=" * 44)
        confirmar = input("  ¿Confirmar? (s/n): ").strip().lower()

        if confirmar != "s":
            print("\n  Pedido cancelado.")
            input("  Presiona Enter para continuar...")
            return

        items_db = [
            {
                "producto_id": i["producto_id"],
                "cantidad": i["cantidad"],
                "subtotal": i["subtotal"],
            }
            for i in carrito
        ]

        faltantes = verificar_stock(items_db)
        if faltantes:
            print("\n  Stock insuficiente para completar el pedido:")
            for f in faltantes:
                print(f"    {f['nombre']:<25} necesario: {f['necesario']}  disponible: {f['disponible']}")
            input("\n  Presiona Enter para volver...")
            return

        orden_id = crear_orden(mesa, items_db, mozo_id=self.user["id"])
        print(f"\n  Pedido #{orden_id} enviado a cocina.")
        input("  Presiona Enter para continuar...")

    # ──────────────────────────────────────────
    def _pedir_mesa(self):
        while True:
            mesa = input("  Mesa (1-6): ").strip()
            if mesa == "0":
                return None
            if mesa.isdigit() and 1 <= int(mesa) <= 6:
                if mesa_tiene_orden_activa(int(mesa)):
                    print(f"  La mesa {mesa} ya tiene un pedido activo.")
                    input("  Presiona Enter para continuar...")
                    return None
                return int(mesa)
            print("  Mesa inválida. Ingresá un número del 1 al 6.")

    # ──────────────────────────────────────────
    def _agregar_producto(self, carrito, categoria, label):
        while True:
            limpiar()
            productos = get_productos_por_categoria(categoria)
            print("=" * 44)
            print(f"  {label.upper()}")
            separador()
            for i, p in enumerate(productos, 1):
                nombre = p["nombre"]
                if p["variante"]:
                    nombre += f" ({p['variante']})"
                print(f"  {i:>2}. {nombre:<30} ${p['precio']:.2f}")
            separador()
            print("   0. Volver")
            print("=" * 44)

            op = input("  Opción: ").strip()
            if op == "0":
                return
            if not op.isdigit() or not (1 <= int(op) <= len(productos)):
                print("  Opción inválida.")
                input("  Presiona Enter...")
                continue

            producto = productos[int(op) - 1]

            cant = input("  Cantidad: ").strip()
            if not cant.isdigit() or int(cant) < 1:
                print("  Cantidad inválida.")
                input("  Presiona Enter...")
                continue

            cantidad = int(cant)
            subtotal = round(producto["precio"] * cantidad, 2)

            nombre_display = producto["nombre"]
            if producto["variante"]:
                nombre_display += f" ({producto['variante']})"

            # Si ya está en el carrito, sumar
            for item in carrito:
                if item["producto_id"] == producto["id"]:
                    item["cantidad"] += cantidad
                    item["subtotal"] = round(item["subtotal"] + subtotal, 2)
                    print(f"\n  Actualizado: {item['cantidad']}x {nombre_display}")
                    input("  Presiona Enter para continuar...")
                    return

            carrito.append({
                "producto_id": producto["id"],
                "nombre":      producto["nombre"],
                "variante":    producto["variante"],
                "cantidad":    cantidad,
                "subtotal":    subtotal,
            })
            print(f"\n  Agregado: {cantidad}x {nombre_display}  ${subtotal:.2f}")
            input("  Presiona Enter para continuar...")
            return

    # ──────────────────────────────────────────
    def ver_mesas(self):
        limpiar()
        mesas = get_estado_mesas()
        ESTADOS = {
            "pendiente":  "Pendiente",
            "preparando": "Preparando",
            "listo":      "Listo p/entregar",
        }
        print("=" * 44)
        print("  ESTADO DE MESAS")
        separador()
        for m in mesas:
            if m["libre"]:
                print(f"  Mesa {m['mesa']}   LIBRE")
            else:
                estado = ESTADOS.get(m["estado"], m["estado"])
                print(f"  Mesa {m['mesa']}   OCUPADA  — Orden #{m['orden_id']}  [{estado}]")
        separador()
        print("=" * 44)
        input("  Presiona Enter para volver...")

    # ──────────────────────────────────────────
    def ver_ordenes_activas(self):
        limpiar()
        ordenes = get_ordenes_activas()
        print("=" * 44)
        print("  ÓRDENES ACTIVAS")
        separador()

        if not ordenes:
            print("  No hay órdenes activas.")
        else:
            for o in ordenes:
                estado = ESTADOS.get(o["estado"], o["estado"])
                print(f"  Orden #{o['id']}  Mesa {o['mesa']}  —  {estado}")
                items = get_items_orden(o["id"])
                mostrar_items(items)
                print(f"    Total: ${o['total']:.2f}   ({o['creado_en']})")
                separador()

        print("=" * 44)
        input("  Presiona Enter para volver...")

    # ──────────────────────────────────────────
    def entregar_orden(self):
        limpiar()
        ordenes = get_ordenes_listas()
        print("=" * 44)
        print("  ÓRDENES LISTAS PARA ENTREGAR")
        separador()

        if not ordenes:
            print("  No hay órdenes listas.")
            print("=" * 44)
            input("  Presiona Enter para volver...")
            return

        for i, o in enumerate(ordenes, 1):
            print(f"  {i}. Orden #{o['id']}  Mesa {o['mesa']}  ${o['total']:.2f}")
            items = get_items_orden(o["id"])
            mostrar_items(items)
            separador()

        print("   0. Volver")
        print("=" * 44)

        op = input("  ¿Cuál entregás? (número): ").strip()
        if op == "0" or not op.isdigit() or not (1 <= int(op) <= len(ordenes)):
            return

        orden = ordenes[int(op) - 1]
        entregar_orden(orden["id"])
        print(f"\n  Orden #{orden['id']} entregada. Venta registrada.")
        input("  Presiona Enter para continuar...")

    # ──────────────────────────────────────────
    def cancelar_orden(self):
        limpiar()
        ordenes = get_ordenes_por_estado("pendiente")
        print("=" * 44)
        print("  CANCELAR ORDEN PENDIENTE")
        separador()

        if not ordenes:
            print("  No hay órdenes pendientes para cancelar.")
            print("=" * 44)
            input("  Presiona Enter para volver...")
            return

        for i, o in enumerate(ordenes, 1):
            print(f"  {i}. Orden #{o['id']}  Mesa {o['mesa']}  ${o['total']:.2f}")
            mostrar_items(get_items_orden(o["id"]))
            separador()

        print("   0. Volver")
        print("=" * 44)

        op = input("  ¿Cuál cancelás? (número): ").strip()
        if op == "0" or not op.isdigit() or not (1 <= int(op) <= len(ordenes)):
            return

        orden = ordenes[int(op) - 1]
        confirmar = input(f"  ¿Cancelar orden #{orden['id']} (mesa {orden['mesa']})? (s/n): ").strip().lower()
        if confirmar == "s":
            cancelar_orden(orden["id"])
            print(f"\n  Orden #{orden['id']} cancelada.")
        else:
            print("\n  Cancelado.")
        input("  Presiona Enter para continuar...")
