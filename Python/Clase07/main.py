from persona import Persona
from persona_dao import PersonaDao

dao = PersonaDao()

print("Probando base de datos...")

dao.insertar(Persona(nombre="Juan", apellido="Perez", email="juan@mail.com"))

print("\nLista de personas:")

for p in dao.seleccionar():
    print(p)