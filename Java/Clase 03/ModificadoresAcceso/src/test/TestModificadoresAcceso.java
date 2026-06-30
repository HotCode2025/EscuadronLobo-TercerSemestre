// Paquete al que pertenece esta clase
package test;

// Importamos la clase Clase1 del paquete paquete1
import paquete1.Clase1;

// Importamos la clase Clase3 del paquete paquete2
import paquete2.Clase3;

// Clase principal
public class TestModificadoresAcceso {

    // Método main: punto de entrada del programa
    public static void main(String[] arg){

        // Creamos un objeto de Clase1
        // Esto llama automáticamente al constructor
        Clase1 clase1 = new Clase1();

        // Accedemos al atributo public
        // Funciona porque es público
        System.out.println("clase1 = " + clase1.atributoPublic);

        // Llamamos al método public
        // También funciona porque es público
        clase1.metodoPublico();

        // Creamos un objeto de Clase3
        // Clase3 hereda de Clase1
        Clase3 claseHija = new Clase3();

        // Mostramos el objeto creado
        System.out.println("claseHija = " + claseHija);
    }
}