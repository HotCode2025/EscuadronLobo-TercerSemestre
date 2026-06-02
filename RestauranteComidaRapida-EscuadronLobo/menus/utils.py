import os
from gestion.gestion_usuarios import cambiar_contrasena as _cambiar_contrasena_db


CATEGORIAS = [
    ("hamburguesa",    "Hamburguesas"),
    ("pizza",          "Pizzas"),
    ("acompanamiento", "Acompañamientos"),
    ("bebida",         "Bebidas"),
]


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def separador(ancho=44):
    print("─" * ancho)


def icono_stock(cantidad, minimo):
    if cantidad <= minimo:
        return "BAJO"
    if cantidad <= minimo * 2:
        return "MEDIO"
    return "ALTO"


def cambiar_contrasena_ui(user, ancho=44):
    limpiar()
    print("=" * ancho)
    print("  CAMBIAR CONTRASEÑA")
    print("=" * ancho)
    actual = input("  Contraseña actual  : ").strip()
    nueva = input("  Nueva contraseña   : ").strip()
    confirmar = input("  Confirmá la nueva  : ").strip()

    if nueva != confirmar:
        print("\n  Las contraseñas no coinciden.")
        input("  Presiona Enter para volver...")
        return

    ok, msg = _cambiar_contrasena_db(user["id"], actual, nueva)
    print(f"\n  {msg}")
    input("  Presiona Enter para continuar...")
