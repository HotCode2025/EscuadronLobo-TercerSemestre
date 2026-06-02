import hashlib
from database import get_connection, execute

ROLES = ("admin", "mozo", "cocinero", "cliente")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_todos():
    conn = get_connection()
    rows = execute(conn, "SELECT * FROM usuarios ORDER BY rol, nombre").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def crear_usuario(nombre, usuario, contrasena, rol):
    conn = get_connection()
    try:
        execute(
            conn,
            "INSERT INTO usuarios (nombre, usuario, contrasena, rol) VALUES (%s,%s,%s,%s)",
            (nombre, usuario, hash_password(contrasena), rol),
        )
        conn.commit()
        return True, "Usuario creado."
    except Exception as e:
        conn.rollback()
        return False, f"Error: {e}"
    finally:
        conn.close()


def cambiar_contrasena(usuario_id, contrasena_actual, nueva_contrasena):
    conn = get_connection()
    try:
        user = execute(
            conn,
            "SELECT contrasena FROM usuarios WHERE id = %s",
            (usuario_id,),
        ).fetchone()

        if not user or user["contrasena"] != hash_password(contrasena_actual):
            return False, "Contraseña actual incorrecta."

        execute(
            conn,
            "UPDATE usuarios SET contrasena = %s WHERE id = %s",
            (hash_password(nueva_contrasena), usuario_id),
        )
        conn.commit()
        return True, "Contraseña actualizada."
    except Exception as e:
        conn.rollback()
        return False, f"Error: {e}"
    finally:
        conn.close()


def eliminar_usuario(usuario_id):
    conn = get_connection()
    execute(conn, "DELETE FROM usuarios WHERE id = %s", (usuario_id,))
    conn.commit()
    conn.close()


def get_usuario_por_id(usuario_id):
    conn = get_connection()
    row = execute(conn, "SELECT * FROM usuarios WHERE id = %s", (usuario_id,)).fetchone()
    conn.close()
    return dict(row) if row else None
