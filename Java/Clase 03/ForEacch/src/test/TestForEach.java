// Paquete al que pertenece esta clase
package test;

// Importamos la clase Persona que está en el paquete domain
import domain.Persona;

// Clase principal
public class TestForEach {

    // Método main: punto de entrada del programa
    public static void main(String[] arg) {

        // Declaración e inicialización de un arreglo de enteros
        // Sintaxis resumida para crear el arreglo
        int edades[] = {5, 6, 8, 9};

        /*
         * FOR NORMAL:
         * Recorre el arreglo usando una variable índice (i)
         * edades.length devuelve la cantidad de elementos del arreglo
         */

        // for (int i = 0; i < edades.length; i++) {
        //     System.out.println("edad = " + edades[i]);
        // }

        /*
         * FOR EACH:
         * Recorre automáticamente cada elemento del arreglo.
         * No necesitamos usar índices.
         *
         * Sintaxis:
         * for(tipo variable : arreglo)
         */

        for (int edad : edades) {

            // Imprime cada valor del arreglo
            System.out.println("edad = " + edad);
        }

        /*
         * Arreglo de objetos Persona.
         * Se crean 3 objetos usando el constructor Persona("nombre")
         */

        Persona personas[] = {
            new Persona("Juan"),
            new Persona("Carla"),
            new Persona("Beatriz")
        };

        // ForEach para recorrer objetos Persona
        for (Persona persona : personas) {

            /*
             * Se imprime cada objeto.
             * Automáticamente Java llama al método toString()
             * definido en la clase Persona.
             */

            System.out.println("persona = " + persona);
        }
    }
}