# ==========================================================
# MÓDULO DE GESTIÓN DE USUARIOS
# ==========================================================
# Este módulo contiene las operaciones relacionadas con:
# - Encriptación de contraseñas
# - Consulta de usuarios
# - Creación de usuarios
# - Cambio de contraseñas
# - Eliminación de usuarios
# - Búsqueda de usuarios por ID
# ==========================================================

# Biblioteca utilizada para generar hashes SHA-256
# y proteger las contraseñas almacenadas.
import hashlib

# Funciones auxiliares para conectarse y ejecutar
# consultas sobre PostgreSQL.
from database import get_connection, execute


# ==========================================================
# ROLES DISPONIBLES EN EL SISTEMA
# ==========================================================
# Define los roles permitidos para los usuarios.
ROLES = ("admin", "mozo", "cocinero", "cliente")


# ==========================================================
# FUNCIÓN: hash_password
# ==========================================================
# Convierte una contraseña de texto plano en un hash SHA-256.
#
# Parámetros:
#   password -> contraseña original
#
# Retorna:
#   Cadena cifrada en formato hexadecimal.
# ==========================================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================================================
# FUNCIÓN: get_todos
# ==========================================================
# Obtiene todos los usuarios registrados en el sistema.
#
# Retorna:
#   Lista de diccionarios con la información de usuarios.
#
# Orden:
#   Primero por rol y luego por nombre.
# ==========================================================
def get_todos():

    conn = get_connection()

    rows = execute(
        conn,
        "SELECT * FROM usuarios ORDER BY rol, nombre"
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ==========================================================
# FUNCIÓN: crear_usuario
# ==========================================================
# Crea un nuevo usuario en la base de datos.
#
# Parámetros:
#   nombre
#   usuario
#   contrasena
#   rol
#
# Retorna:
#   (True, mensaje)  -> si la operación fue exitosa
#   (False, mensaje) -> si ocurrió un error
# ==========================================================
def crear_usuario(nombre, usuario, contrasena, rol):

    conn = get_connection()

    try:

        execute(
            conn,
            """
            INSERT INTO usuarios
            (nombre, usuario, contrasena, rol)
            VALUES (%s,%s,%s,%s)
            """,
            (
                nombre,
                usuario,
                hash_password(contrasena),
                rol
            ),
        )

        conn.commit()

        return True, "Usuario creado."

    except Exception as e:

        conn.rollback()

        return False, f"Error: {e}"

    finally:

        conn.close()


# ==========================================================
# FUNCIÓN: cambiar_contrasena
# ==========================================================
# Permite modificar la contraseña de un usuario.
#
# Verifica:
#   1. Que el usuario exista.
#   2. Que la contraseña actual sea correcta.
#
# Parámetros:
#   usuario_id
#   contrasena_actual
#   nueva_contrasena
#
# Retorna:
#   Estado de la operación y mensaje descriptivo.
# ==========================================================
def cambiar_contrasena(
        usuario_id,
        contrasena_actual,
        nueva_contrasena):

    conn = get_connection()

    try:

        # Obtener contraseña almacenada
        user = execute(
            conn,
            """
            SELECT contrasena
            FROM usuarios
            WHERE id = %s
            """,
            (usuario_id,),
        ).fetchone()

        # Validar usuario y contraseña actual
        if not user or user["contrasena"] != hash_password(contrasena_actual):

            return False, "Contraseña actual incorrecta."

        # Actualizar contraseña
        execute(
            conn,
            """
            UPDATE usuarios
            SET contrasena = %s
            WHERE id = %s
            """,
            (
                hash_password(nueva_contrasena),
                usuario_id
            ),
        )

        conn.commit()

        return True, "Contraseña actualizada."

    except Exception as e:

        conn.rollback()

        return False, f"Error: {e}"

    finally:

        conn.close()


# ==========================================================
# FUNCIÓN: eliminar_usuario
# ==========================================================
# Elimina un usuario utilizando su ID.
#
# Parámetro:
#   usuario_id
# ==========================================================
def eliminar_usuario(usuario_id):

    conn = get_connection()

    execute(
        conn,
        "DELETE FROM usuarios WHERE id = %s",
        (usuario_id,)
    )

    conn.commit()

    conn.close()


# ==========================================================
# FUNCIÓN: get_usuario_por_id
# ==========================================================
# Busca un usuario específico utilizando su ID.
#
# Parámetro:
#   usuario_id
#
# Retorna:
#   Diccionario con los datos del usuario
#   o None si no existe.
# ==========================================================
def get_usuario_por_id(usuario_id):

    conn = get_connection()

    row = execute(
        conn,
        "SELECT * FROM usuarios WHERE id = %s",
        (usuario_id,)
    ).fetchone()

    conn.close()

    return dict(row) if row else None
