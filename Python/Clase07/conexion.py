import sqlite3

class Conexion:
    DB = "personas.db"

    @staticmethod
    def obtener_conexion():
        return sqlite3.connect(Conexion.DB)

    @staticmethod
    def cerrar(conexion):
        if conexion:
            conexion.close()