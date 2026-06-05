from gestion.gestion_pedidos import (
    get_productos_por_categoria,
    crear_orden,
    get_items_orden,
    mesa_tiene_orden_activa,
    verificar_stock,
    get_ordenes_cliente,
)
from menus.utils import limpiar, separador, CATEGORIAS, cambiar_contrasena_ui

ESTADOS = {
    "pendiente":  "Pendiente  (esperando cocina)",
    "preparando": "En preparación",
    "listo":      "Listo para retirar",
    "entregado":  "Entregado",
}


def mostrar_items(items):
    for it in items:
        nombre = it["nombre"]
        if it["variante"]:
            nombre += f" ({it['variante']})"
        print(f"    {it['cantidad']}x  {nombre:<28} ${it['subtotal']:.2f}")


class MenuCliente:
    def __init__(self, user):
        self.user = user

    # ──────────────────────────────────────────
    def ejecutar(self):
        while True:
            limpiar()
            print("=" * 44)
            print(f"  Bienvenido, {self.user['nombre']}")
            print("=" * 44)
            print("  1. Ver menú")
            print("  2. Hacer pedido")
            print("  3. Ver estado de mis pedidos")
            print("  4. Cambiar contraseña")
            print("  0. Cerrar sesión")
            print("=" * 44)

            op = input("  Opción: ").strip()

            if op == "1":
                self.ver_menu()
            elif op == "2":
                self.hacer_pedido()
            elif op == "3":
                self.ver_mis_pedidos()
            elif op == "4":
                self._cambiar_contrasena()
            elif op == "0":
                break

    # ──────────────────────────────────────────
    def ver_menu(self):
        while True:
            limpiar()
            print("=" * 44)
            print("  MENÚ")
            print("=" * 44)
            for i, (_, label) in enumerate(CATEGORIAS, 1):
                print(f"  {i}. {label}")
            print("  0. Volver")
            print("=" * 44)

            op = input("  Categoría: ").strip()
            if op == "0":
                return
            if not op.isdigit() or not (1 <= int(op) <= len(CATEGORIAS)):
                continue

            cat_key, cat_label = CATEGORIAS[int(op) - 1]
            self._mostrar_categoria(cat_key, cat_label)

    def _mostrar_categoria(self, categoria, label):
        limpiar()
        productos = get_productos_por_categoria(categoria)
        print("=" * 44)
        print(f"  {label.upper()}")
        separador()
        print(f"  {'Nombre':<32} {'Precio':>7}")
        separador()
        for p in productos:
            nombre = p["nombre"]
            if p["variante"]:
                nombre += f" ({p['variante']})"
            print(f"  {nombre:<32} ${p['precio']:.2f}")
        separador()
        print("=" * 44)
        input("  Presiona Enter para volver...")

    # ──────────────────────────────────────────
    def hacer_pedido(self):
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
            print(f"  MI PEDIDO — Mesa {mesa}")
            separador()
            if carrito:
                mostrar_items(carrito)
                separador()
                total = sum(i["subtotal"] for i in carrito)
                print(f"  Total: ${total:.2f}")
                separador()

            for i, (_, label) in enumerate(CATEGORIAS, 1):
                print(f"  {i}. {label}")
            print("  ─")
            print("  0. Confirmar pedido")
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
                "cantidad":    i["cantidad"],
                "subtotal":    i["subtotal"],
            }
            for i in carrito
        ]

        faltantes = verificar_stock(items_db)
        if faltantes:
            print("\n  Algunos productos no tienen stock suficiente:")
            for f in faltantes:
                print(f"    {f['nombre']:<25} disponible: {f['disponible']}")
            input("\n  Presiona Enter para volver...")
            return

        orden_id = crear_orden(mesa, items_db, cliente_id=self.user["id"])
        print(f"\n  Pedido #{orden_id} realizado. ¡Ya lo estamos preparando!")
        input("  Presiona Enter para continuar...")

    # ──────────────────────────────────────────
    def _pedir_mesa(self):
        while True:
            mesa = input("  Mesa (1-6, o 0 para cancelar): ").strip()
            if mesa == "0":
                return None
            if mesa.isdigit() and 1 <= int(mesa) <= 6:
                if mesa_tiene_orden_activa(int(mesa)):
                    print(f"  La mesa {mesa} ya tiene un pedido activo.")
                    input("  Presiona Enter para continuar...")
                    return None
                return int(mesa)
            print("  Número de mesa inválido.")

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

    def _cambiar_contrasena(self):
        cambiar_contrasena_ui(self.user)

    # ──────────────────────────────────────────
    def ver_mis_pedidos(self):
        limpiar()
        ordenes = get_ordenes_cliente(self.user["id"])

        print("=" * 44)
        print("  MIS PEDIDOS")
        separador()

        if not ordenes:
            print("  No tenés pedidos registrados.")
        else:
            for o in ordenes:
                estado = ESTADOS.get(o["estado"], o["estado"])
                print(f"  Orden #{o['id']}  Mesa {o['mesa']}  ${o['total']:.2f}")
                print(f"  Estado: {estado}")
                mostrar_items(get_items_orden(o["id"]))
                print(f"  ({o['creado_en']})")
                separador()

        print("=" * 44)
        input("  Presiona Enter para volver...")
