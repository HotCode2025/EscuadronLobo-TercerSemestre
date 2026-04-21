# Importamos la clase Pelicula desde el archivo pelicula.py
from catalogo_peliculas.dominio.pelicula import Pelicula

# Importamos la clase CatalogoPeliculas desde catalogo_peliculas.py
from catalogo_peliculas.servicio.catalogo_peliculas import CatalogoPeliculas


# Función que muestra el menú en pantalla
def mostrar_menu():
    print("\n--- Menú del Catálogo de Películas ---")
    print("1. Agregar película")
    print("2. Listar películas")
    print("3. Eliminar archivo de películas")
    print("4. Salir")


# Variable que guarda la opción del usuario
opcion = 0

# Bucle principal del programa
# Se repite hasta que el usuario elija la opción 4 (salir)
while opcion != 4:

    # Mostramos el menú
    mostrar_menu()

    try:
        # Pedimos una opción al usuario
        # input() devuelve texto, por eso lo convertimos a entero
        opcion = int(input("Selecciona una opción: "))

    except ValueError:
        # Si el usuario escribe algo que no es número
        print("Por favor, ingresa un número válido.")
        continue  # vuelve al inicio del while

    # -------- OPCIONES DEL MENÚ --------

    # OPCIÓN 1: Agregar película
    if opcion == 1:

        # Pedimos el nombre de la película
        nombre = input("Escribe el nombre de la película: ")

        # Creamos un objeto de la clase Pelicula
        pelicula = Pelicula(nombre)

        # Llamamos al método para guardarla en el archivo
        CatalogoPeliculas.agregar_pelicula(pelicula)

        print("Película agregada con éxito.")


    # OPCIÓN 2: Listar películas
    elif opcion == 2:

        # Llama al método que lee el archivo y muestra las películas
        CatalogoPeliculas.listar_peliculas()


    # OPCIÓN 3: Eliminar archivo
    elif opcion == 3:

        # Llama al método que elimina el archivo
        CatalogoPeliculas.eliminar()


    # OPCIÓN 4: Salir del programa
    elif opcion == 4:
        print("¡Hasta luego!")


    # Si el usuario ingresa un número fuera de las opciones
    else:
        print("Opción no válida, intenta nuevamente.")