// Paquete al que pertenece esta clase
package paquete2;

// Importamos Clase1
import paquete1.Clase1;

// Clase3 hereda de Clase1
public class Clase3 extends Clase1{

    // Constructor público
    public Clase3(){

        // Llama al constructor protected de la clase padre
        super("protected");

        // Accedemos al atributo protected heredado
        this.atributoProtected = "Accedemos desde la clase hija";

        // Mostramos el valor del atributo protected
        System.out.println("AtributoProtected = " + this.atributoProtected);

        // Accedemos al atributo public heredado
        this.atributoPublic = "Es totalmente publico";
    }
}