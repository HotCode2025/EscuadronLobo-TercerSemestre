// Paquete al que pertenece la clase
package domain;

// Clase Persona
public class Persona {

    // Atributo privado de la clase
    // Guarda el nombre de la persona
    private String nombre;

    /*
     * Constructor de la clase.
     * Se ejecuta al crear un objeto Persona.
     */
    public Persona(String nombre) {

        // this.nombre hace referencia al atributo de la clase
        // nombre hace referencia al parámetro recibido
        this.nombre = nombre;
    }

    // Método GET
    // Devuelve el valor del atributo nombre
    public String getNombre() {
        return nombre;
    }

    // Método SET
    // Permite modificar el nombre
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    /*
     * Método toString()
     * Se usa para mostrar el objeto como texto.
     */
    @Override
    public String toString() {

        return "Persona{" + "nombre=" + nombre + '}';
    }
}