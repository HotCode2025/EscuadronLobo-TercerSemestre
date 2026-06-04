from gestion.gestion_pedidos import (
    get_ordenes_por_estado,
    get_items_orden,
    cambiar_estado,
    marcar_listo,
)
from gestion.gestion_stock import get_todos as get_ingredientes
from menus.utils import limpiar, separador, icono_stock, cambiar_contrasena_ui

ESTADOS = {
    "pendiente":  "Pendiente",
    "preparando": "En preparación",
    "listo":      "Listo",
}


def mostrar_items(items):
    for it in items:
        nombre = it["nombre"]
        if it["variante"]:
            nombre += f" ({it['variante']})"
        print(f"    {it['cantidad']}x  {nombre}")


def mostrar_ordenes(ordenes, titulo):
    limpiar()
    print("=" * 44)
    print(f"  {titulo}")
    separador()
    if not ordenes:
        print("  No hay órdenes.")
        print("=" * 44)
        input("  Presiona Enter para volver...")
        return False

    for i, o in enumerate(ordenes, 1):
        estado = ESTADOS.get(o["estado"], o["estado"])
        print(f"  {i}. Orden #{o['id']}  Mesa {o['mesa']}  [{estado}]")
        mostrar_items(get_items_orden(o["id"]))
        print(f"     {o['creado_en']}")
        separador()

    print("   0. Volver")
    print("=" * 44)
    return True


class MenuCocinero:
    def __init__(self, user):
        self.user = user

    # ──────────────────────────────────────────
    def ejecutar(self):
        while True:
            limpiar()
            print("=" * 44)
            print(f"  COCINERO — {self.user['nombre']}")
            print("=" * 44)
            print("  1. Ver pedidos pendientes")
            print("  2. Iniciar preparación")
            print("  3. Marcar pedido listo")
            print("  4. Ver stock de ingredientes")
            print("  5. Cambiar contraseña")
            print("  0. Cerrar sesión")
            print("=" * 44)

            op = input("  Opción: ").strip()

            if op == "1":
                self.ver_pendientes()
            elif op == "2":
                self.iniciar_preparacion()
            elif op == "3":
                self.marcar_listo()
            elif op == "4":
                self.ver_stock()
            elif op == "5":
                cambiar_contrasena_ui(self.user)
            elif op == "0":
                break

    # ──────────────────────────────────────────
    def ver_pendientes(self):
        pendientes = get_ordenes_por_estado("pendiente")
        preparando = get_ordenes_por_estado("preparando")
        todas = pendientes + preparando

        limpiar()
        print("=" * 44)
        print("  COCINA — ÓRDENES ACTIVAS")
        separador()

        if not todas:
            print("  No hay órdenes en cocina.")
        else:
            for o in todas:
                estado = ESTADOS.get(o["estado"], o["estado"])
                print(f"  Orden #{o['id']}  Mesa {o['mesa']}  [{estado}]")
                mostrar_items(get_items_orden(o["id"]))
                print(f"     {o['creado_en']}")
                separador()

        print("=" * 44)
        input("  Presiona Enter para volver...")

    # ──────────────────────────────────────────
    def iniciar_preparacion(self):
        ordenes = get_ordenes_por_estado("pendiente")
        if not mostrar_ordenes(ordenes, "INICIAR PREPARACIÓN"):
            return

        op = input("  ¿Cuál empezás a preparar? (número): ").strip()
        if op == "0" or not op.isdigit() or not (1 <= int(op) <= len(ordenes)):
            return

        orden = ordenes[int(op) - 1]
        cambiar_estado(orden["id"], "preparando")
        print(f"\n  Orden #{orden['id']} marcada como EN PREPARACIÓN.")
        input("  Presiona Enter para continuar...")

    # ──────────────────────────────────────────
    def marcar_listo(self):
        ordenes = get_ordenes_por_estado("preparando")
        if not mostrar_ordenes(ordenes, "MARCAR PEDIDO LISTO"):
            return

        op = input("  ¿Cuál está lista? (número): ").strip()
        if op == "0" or not op.isdigit() or not (1 <= int(op) <= len(ordenes)):
            return

        orden = ordenes[int(op) - 1]
        alertas = marcar_listo(orden["id"])

        print(f"\n  Orden #{orden['id']} marcada como LISTA.")

        if alertas:
            print()
            print("  ⚠  STOCK BAJO:")
            for a in alertas:
                print(f"     {a['nombre']:<25} {a['cantidad']} unidades (mín. {a['minimo']})")

        input("  Presiona Enter para continuar...")

    # ──────────────────────────────────────────
    def ver_stock(self):
        limpiar()
        ingredientes = get_ingredientes()

        print("=" * 44)
        print("  STOCK DE INGREDIENTES")
        separador()
        print(f"  {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
        separador()

        for ing in ingredientes:
            icono = icono_stock(ing["cantidad"], ing["minimo"])
            print(f"  {ing['nombre']:<25} {ing['cantidad']:>6}  {ing['minimo']:>5}  {icono}")

        separador()
        print("=" * 44)
        input("  Presiona Enter para volver...")
