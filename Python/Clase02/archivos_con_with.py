from ManejoArchivos import ManejoArchivos  # Importa la clase ManejoArchivos desde el módulo ManejoArchivos

# MANEJO DE CONTEXTO WITH: sintaxis simplificada, abre y cierra el archivo automáticamente
# El siguiente bloque comentado muestra la forma tradicional con open():
# with open('prueba.txt', 'r', encoding='utf8') as archivo:
#     print(archivo.read())

# No hace falta usar try ni finally 
# El contexto with lo que se ejecuta de manera automática
# Utiliza diferentes metodos: __enter__ este es el que abre
# ahora el siquiente metodo es el que cierra: __exit__

with ManejoArchivos('prueba.txt') as archivo:  
    print(archivo.read())
