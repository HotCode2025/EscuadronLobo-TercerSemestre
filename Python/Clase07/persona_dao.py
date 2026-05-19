from conexion import Conexion
from persona import Persona

class PersonaDao:

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