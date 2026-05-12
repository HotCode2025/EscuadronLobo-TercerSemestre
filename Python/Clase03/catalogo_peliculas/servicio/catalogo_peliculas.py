# Importamos el módulo os
# Sirve para trabajar con archivos y verificar si existen
import os
from catalogo_peliculas.dominio.pelicula import Pelicula

# Definimos la clase CatalogoPeliculas
class CatalogoPeliculas:
    # Atributo de clase (compartido por todos)
    # Guarda el nombre del archivo donde se almacenan las películas
    ruta_archivo = 'peliculas.txt'

    # Método estático: no necesita crear un objeto para usarse
    @staticmethod
    def agregar_pelicula(pelicula):
        # Abrimos el archivo en modo 'a' (append = agregar al final)
        # encoding='utf-8' permite usar acentos y caracteres especiales
        with open(CatalogoPeliculas.ruta_archivo, 'a', encoding='utf-8') as archivo:
            # Escribimos el nombre de la película en el archivo
            # \n sirve para hacer un salto de línea
            archivo.write(pelicula.nombre + '\n')

    # Método estático para listar las películas
    @staticmethod
    def listar_peliculas():
        # Abrimos el archivo en modo lectura ('r')
        with open(CatalogoPeliculas.ruta_archivo, 'r', encoding='utf-8') as archivo:
            print('Catalogo de peliculas'.center(50, '-'))
            print(archivo.read())

    # Método estático para eliminar el archivo
    @staticmethod
    def eliminar():
        os.remove(CatalogoPeliculas.ruta_archivo)
