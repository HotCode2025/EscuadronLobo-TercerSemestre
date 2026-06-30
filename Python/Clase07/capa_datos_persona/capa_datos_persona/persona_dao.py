from Clase07.capa_datos_persona.conexion import Conexion
from Clase07.capa_datos_persona.persona import Persona

class PersonaDAO:

    """
    DAO significa: Data Access Object
    CRUD significa:
                    Create -->  Insertar
                    Read    --> Seleccionar
                    Update -->  Actualizar
                    Delete -->  Eliminar
    """
    _SELECCINAR = 'SELECT * FROM persona ORDER BY id_persona'
    _INSERTAR = 'INSERT persona(nombre, apellido, email) VALUES (%S, %s, %S)'
    _ACTUALIZAR = 'UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s'
    _ELIMINAR ='dELETE FROM persona WHERE id_persona=%s'

    def __init__(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS persona (
            id_persona INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            apellido TEXT,
            email TEXT
        )
        """)

        conexion.commit()
        Conexion.cerrar(conexion)

    def insertar(self, persona):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO persona(nombre, apellido, email) VALUES(?,?,?)",
            (persona.nombre, persona.apellido, persona.email)
        )

        conexion.commit()
        Conexion.cerrar(conexion)

    def seleccionar(self):
        conexion = Conexion.obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM persona")
        registros = cursor.fetchall()

        personas = []
        for r in registros:
            personas.append(Persona(r[0], r[1], r[2], r[3]))

        Conexion.cerrar(conexion)
        return personas