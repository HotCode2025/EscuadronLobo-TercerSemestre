// Paquete al que pertenece esta clase
package paquete1;

// ClaseHija2 hereda de Clase2
public class ClaseHija2 extends Clase2{

    // Constructor público
    public ClaseHija2(){

        // Llama al constructor de la clase padre
        super();

        // Modificamos el atributo default heredado
        this.atributoDefault = "Modificacion del atributo Default";

        // Mostramos el nuevo valor del atributo
        System.out.println("atributoDefault = " + this.atributoDefault);

        // Llamamos al método default heredado
        this.metodoDefault();
    }
}
