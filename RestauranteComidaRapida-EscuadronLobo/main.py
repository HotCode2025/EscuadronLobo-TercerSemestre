from database import init_db, get_connection, execute
from gestion.gestion_usuarios import hash_password, crear_usuario
from menus.utils import limpiar


def auto_seed():
    conn = get_connection()
    total = execute(conn, "SELECT COUNT(*) AS n FROM usuarios").fetchone()["n"]
    conn.close()
    if total == 0:
        from seed import seed
        seed()


def login():
    print("=" * 40)
    print("    RESTAURANTE ESCUADRON LOBO")
    print("=" * 40)
    print()
    print("  1. Iniciar sesión")
    print("  2. Registrarse (clientes)")
    print("  0. Salir")
    print()

    op = input("  Opción: ").strip()

    if op == "0":
        return "salir"
    if op == "2":
        return "registro"

    usuario = input("  Usuario   : ").strip()
    contrasena = input("  Contraseña: ").strip()

    conn = get_connection()
    user = execute(
        conn,
        "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s",
        (usuario, hash_password(contrasena)),
    ).fetchone()
    conn.close()

    return dict(user) if user else None


def registro_cliente():
    limpiar()
    print("=" * 40)
    print("  REGISTRO DE CLIENTE")
    print("=" * 40)

    nombre = input("  Nombre completo : ").strip()
    usuario = input("  Usuario         : ").strip()
    contrasena = input("  Contraseña      : ").strip()
    confirmar = input("  Confirmá la contraseña: ").strip()

    if not nombre or not usuario or not contrasena:
        print("\n  Todos los campos son obligatorios.")
        input("  Presiona Enter para volver...")
        return

    if contrasena != confirmar:
        print("\n  Las contraseñas no coinciden.")
        input("  Presiona Enter para volver...")
        return

    _, msg = crear_usuario(nombre, usuario, contrasena, "cliente")
    print(f"\n  {msg}")
    input("  Presiona Enter para continuar...")


def main():
    init_db()
    auto_seed()

    while True:
        limpiar()
        resultado = login()

        if resultado == "salir":
            break

        if resultado == "registro":
            registro_cliente()
            continue

        if resultado is None:
            print("\n  Usuario o contraseña incorrectos.")
            input("  Presiona Enter para intentar de nuevo...")
            continue

        user = resultado
        limpiar()
        rol = user["rol"]

        if rol == "admin":
            from menus.menu_admin import MenuAdmin
            MenuAdmin(user).ejecutar()
        elif rol == "mozo":
            from menus.menu_mozo import MenuMozo
            MenuMozo(user).ejecutar()
        elif rol == "cocinero":
            from menus.menu_cocinero import MenuCocinero
            MenuCocinero(user).ejecutar()
        elif rol == "cliente":
            from menus.menu_cliente import MenuCliente
            MenuCliente(user).ejecutar()


if __name__ == "__main__":
    main()
