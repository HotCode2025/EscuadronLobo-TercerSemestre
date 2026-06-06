import re
from gestion.gestion_usuarios import get_todos, crear_usuario, eliminar_usuario, ROLES
from gestion.gestion_stock import (
    get_todos as get_ingredientes,
    get_alertas,
    ajustar_stock,
    get_todos_productos,
    toggle_disponible,
)
from gestion.gestion_ventas import get_ventas_hoy, get_ventas_por_fecha, get_resumen_ventas, get_items_venta
from menus.utils import limpiar, separador, icono_stock, cambiar_contrasena_ui

CATEGORIAS_LABEL = {
    "hamburguesa":    "Hamburguesa",
    "pizza":          "Pizza",
    "acompanamiento": "Acompañamiento",
    "bebida":         "Bebida",
}


class MenuAdmin:
    def __init__(self, user):
        self.user = user

    # ──────────────────────────────────────────
    def ejecutar(self):
        while True:
            limpiar()
            print("=" * 48)
            print(f"  ADMIN — {self.user['nombre']}")
            print("=" * 48)
            print("  1. Gestión de usuarios")
            print("  2. Gestión del menú")
            print("  3. Inventario / Stock")
            print("  4. Reportes de ventas")
            print("  5. Cambiar contraseña")
            print("  0. Cerrar sesión")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self.gestion_usuarios()
            elif op == "2":
                self.gestion_menu()
            elif op == "3":
                self.gestion_stock()
            elif op == "4":
                self.reportes_ventas()
            elif op == "5":
                self._cambiar_contrasena()
            elif op == "0":
                break

    # ══════════════════════════════════════════
    #  USUARIOS
    # ══════════════════════════════════════════
    def gestion_usuarios(self):
        while True:
            limpiar()
            print("=" * 48)
            print("  GESTIÓN DE USUARIOS")
            print("=" * 48)
            print("  1. Ver todos los usuarios")
            print("  2. Crear usuario")
            print("  3. Eliminar usuario")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ver_usuarios()
            elif op == "2":
                self._crear_usuario()
            elif op == "3":
                self._eliminar_usuario()
            elif op == "0":
                break

    def _ver_usuarios(self):
        limpiar()
        usuarios = get_todos()
        print("=" * 48)
        print("  USUARIOS")
        separador(48)
        print(f"  {'ID':<4} {'Nombre':<20} {'Usuario':<14} {'Rol'}")
        separador(48)
        for u in usuarios:
            print(f"  {u['id']:<4} {u['nombre']:<20} {u['usuario']:<14} {u['rol']}")
        separador(48)
        print(f"  Total: {len(usuarios)} usuarios")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _crear_usuario(self):
        limpiar()
        print("=" * 48)
        print("  CREAR USUARIO")
        print("=" * 48)

        nombre = input("  Nombre completo : ").strip()
        usuario = input("  Usuario         : ").strip()
        contrasena = input("  Contraseña      : ").strip()

        print(f"  Roles disponibles: {', '.join(ROLES)}")
        rol = input("  Rol             : ").strip().lower()

        if not nombre or not usuario or not contrasena:
            print("\n  Todos los campos son obligatorios.")
            input("  Presiona Enter para volver...")
            return

        if rol not in ROLES:
            print(f"\n  Rol inválido. Debe ser uno de: {', '.join(ROLES)}")
            input("  Presiona Enter para volver...")
            return

        ok, msg = crear_usuario(nombre, usuario, contrasena, rol)
        print(f"\n  {msg}")
        input("  Presiona Enter para continuar...")

    def _eliminar_usuario(self):
        limpiar()
        usuarios = get_todos()
        print("=" * 48)
        print("  ELIMINAR USUARIO")
        separador(48)
        for i, u in enumerate(usuarios, 1):
            print(f"  {i:>2}. [{u['rol']:<8}] {u['nombre']}  (@{u['usuario']})")
        separador(48)
        print("   0. Volver")
        print("=" * 48)

        op = input("  ¿Cuál eliminás? (número): ").strip()
        if op == "0" or not op.isdigit() or not (1 <= int(op) <= len(usuarios)):
            return

        target = usuarios[int(op) - 1]

        if target["id"] == self.user["id"]:
            print("\n  No podés eliminarte a vos mismo.")
            input("  Presiona Enter para volver...")
            return

        confirmar = input(f"  ¿Eliminar a {target['nombre']}? (s/n): ").strip().lower()
        if confirmar == "s":
            eliminar_usuario(target["id"])
            print(f"\n  Usuario '{target['nombre']}' eliminado.")
        else:
            print("\n  Cancelado.")
        input("  Presiona Enter para continuar...")

    # ══════════════════════════════════════════
    #  MENÚ
    # ══════════════════════════════════════════
    def gestion_menu(self):
        while True:
            limpiar()
            print("=" * 48)
            print("  GESTIÓN DEL MENÚ")
            print("=" * 48)
            print("  1. Ver todos los productos")
            print("  2. Habilitar / deshabilitar producto")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ver_productos()
            elif op == "2":
                self._toggle_producto()
            elif op == "0":
                break

    def _ver_productos(self):
        limpiar()
        productos = get_todos_productos()
        print("=" * 48)
        print("  PRODUCTOS")
        separador(48)
        cat_actual = None
        for p in productos:
            cat = CATEGORIAS_LABEL.get(p["categoria"], p["categoria"])
            if cat != cat_actual:
                if cat_actual:
                    separador(48)
                print(f"  {cat.upper()}")
                cat_actual = cat
            nombre = p["nombre"]
            if p["variante"]:
                nombre += f" ({p['variante']})"
            estado = "OK" if p["disponible"] else "OFF"
            print(f"  {p['id']:>3}. {nombre:<32} ${p['precio']:.2f}  [{estado}]")
        separador(48)
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _toggle_producto(self):
        limpiar()
        productos = get_todos_productos()
        print("=" * 48)
        print("  HABILITAR / DESHABILITAR PRODUCTO")
        separador(48)
        for p in productos:
            nombre = p["nombre"]
            if p["variante"]:
                nombre += f" ({p['variante']})"
            estado = "ON" if p["disponible"] else "OFF"
            print(f"  {p['id']:>3}. [{estado}] {nombre}")
        separador(48)
        print("   0. Volver")
        print("=" * 48)

        op = input("  ID del producto: ").strip()
        if op == "0":
            return

        ids = [p["id"] for p in productos]
        if not op.isdigit() or int(op) not in ids:
            print("  ID inválido.")
            input("  Presiona Enter para volver...")
            return

        toggle_disponible(int(op))
        print(f"\n  Producto actualizado.")
        input("  Presiona Enter para continuar...")

    # ══════════════════════════════════════════
    #  STOCK
    # ══════════════════════════════════════════
    def gestion_stock(self):
        while True:
            limpiar()
            print("=" * 48)
            print("  INVENTARIO / STOCK")
            print("=" * 48)
            print("  1. Ver stock completo")
            print("  2. Ver alertas de stock bajo")
            print("  3. Reponer ingrediente")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ver_stock_completo()
            elif op == "2":
                self._ver_alertas()
            elif op == "3":
                self._reponer()
            elif op == "0":
                break

    def _ver_stock_completo(self):
        limpiar()
        ingredientes = get_ingredientes()
        print("=" * 48)
        print("  STOCK COMPLETO")
        separador(48)
        print(f"  {'ID':<4} {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
        separador(48)
        for ing in ingredientes:
            icono = icono_stock(ing["cantidad"], ing["minimo"])
            print(f"  {ing['id']:<4} {ing['nombre']:<25} {ing['cantidad']:>6}  {ing['minimo']:>5}  {icono}")
        separador(48)
        alertas = [i for i in ingredientes if i["cantidad"] <= i["minimo"]]
        if alertas:
            print(f"  {len(alertas)} ingrediente(s) con stock bajo.")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _ver_alertas(self):
        limpiar()
        alertas = get_alertas()
        print("=" * 48)
        print("  ALERTAS DE STOCK BAJO")
        separador(48)
        if not alertas:
            print("  Sin alertas. Todo el stock está OK.")
        else:
            print(f"  {'ID':<4} {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
            separador(48)
            for a in alertas:
                print(f"  {a['id']:<4} {a['nombre']:<25} {a['cantidad']:>6}  {a['minimo']:>5}  ⚠")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _reponer(self):
        limpiar()
        ingredientes = get_ingredientes()
        print("=" * 48)
        print("  AJUSTAR STOCK")
        separador(48)
        print(f"  {'ID':<4} {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
        separador(48)
        for ing in ingredientes:
            icono = icono_stock(ing["cantidad"], ing["minimo"])
            print(f"  {ing['id']:<4} {ing['nombre']:<25} {ing['cantidad']:>6}  {ing['minimo']:>5}  {icono}")
        separador(48)
        print("   0. Volver")
        print("=" * 48)

        op = input("  ID del ingrediente: ").strip()
        if op == "0":
            return

        ids = [i["id"] for i in ingredientes]
        if not op.isdigit() or int(op) not in ids:
            print("  ID inválido.")
            input("  Presiona Enter para volver...")
            return

        ing = next(i for i in ingredientes if i["id"] == int(op))
        print(f"\n  {ing['nombre']} — Stock actual: {ing['cantidad']}")
        print("  1. Agregar")
        print("  2. Quitar")
        accion = input("  Opción: ").strip()

        if accion not in ("1", "2"):
            return

        cant = input("  Cantidad: ").strip()
        if not cant.isdigit() or int(cant) < 1:
            print("  Cantidad inválida.")
            input("  Presiona Enter para volver...")
            return

        cantidad = int(cant) if accion == "1" else -int(cant)
        ajustar_stock(ing["id"], cantidad)
        signo = "+" if cantidad > 0 else ""
        print(f"\n  {ing['nombre']}: {signo}{cantidad} unidades.")
        input("  Presiona Enter para continuar...")

    # ══════════════════════════════════════════
    #  VENTAS
    # ══════════════════════════════════════════
    def reportes_ventas(self):
        while True:
            limpiar()
            resumen = get_resumen_ventas()
            print("=" * 48)
            print("  REPORTES DE VENTAS")
            separador(48)
            print(f"  Total de ventas:     {resumen['total_ventas']}")
            print(f"  Recaudado total:     ${resumen['total_recaudado']:.2f}")
            print(f"  Recaudado hoy:       ${resumen['hoy']:.2f}")
            separador(48)
            print("  1. Ver ventas de hoy")
            print("  2. Ver ventas por fecha")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ventas_hoy()
            elif op == "2":
                self._ventas_por_fecha()
            elif op == "0":
                break

    def _mostrar_ventas(self, ventas, titulo):
        limpiar()
        print("=" * 48)
        print(f"  {titulo}")
        separador(48)
        if not ventas:
            print("  Sin ventas registradas.")
        else:
            for v in ventas:
                hora = v["fecha"].strftime("%H:%M")
                print(f"  Venta #{v['id']}  Orden #{v['orden_id']}  Mesa {v['mesa']}  ${v['total']:.2f}  {hora}")
                items = get_items_venta(v["orden_id"])
                for it in items:
                    nombre = it["nombre"]
                    if it["variante"]:
                        nombre += f" ({it['variante']})"
                    print(f"      {it['cantidad']}x  {nombre}")
                separador(48)
            total = sum(v["total"] for v in ventas)
            print(f"  TOTAL: ${total:.2f}  ({len(ventas)} ventas)")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _ventas_hoy(self):
        self._mostrar_ventas(get_ventas_hoy(), "VENTAS DE HOY")

    def _ventas_por_fecha(self):
        limpiar()
        fecha = input("  Fecha (AAAA-MM-DD): ").strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("\n  Formato inválido. Usá AAAA-MM-DD (ej: 2026-04-02).")
            input("  Presiona Enter para volver...")
            return
        ventas = get_ventas_por_fecha(fecha)
        self._mostrar_ventas(ventas, f"VENTAS DEL {fecha}")

    def _cambiar_contrasena(self):
        cambiar_contrasena_ui(self.user, ancho=48)
