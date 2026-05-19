class Persona:
    def __init__(self, id_persona=None, nombre="", apellido="", email=""):
        self.id_persona = id_persona
        self.nombre = nombre
        self.apellido = apellido
        self.email = email

    def __str__(self):
        return f"{self.id_persona} - {self.nombre} {self.apellido} ({self.email})"