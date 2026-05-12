# Definimos la clase Pelicula
class Pelicula:

    # Constructor: se ejecuta cuando creamos un objeto
    def __init__(self, nombre):
        # self representa el objeto actual
        # Guardamos el nombre que recibimos en el atributo del objeto
        self._nombre = nombre

    # Método especial (__str__)
    # Define cómo se muestra el objeto cuando usamos print()
    def __str__(self):
        # Retornamos un texto formateado con el nombre de la película
        return f"Pelicula: {self._nombre}"

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
