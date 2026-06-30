// Paquete al que pertenece esta clase
package paquete1;

// Clase pública
// Puede utilizarse desde cualquier paquete
public class Clase1 {

    // Atributo public:
    // Puede accederse desde cualquier clase y cualquier paquete
    public String atributoPublic = "Valor atribuido public";

    // Atributo protected:
    // Puede accederse desde el mismo paquete
    // y desde clases hijas
    protected String atributoProtected = "Cecilia";

    // Constructor público
    // Se ejecuta al crear un objeto
    public Clase1(){

        // Mensaje que se muestra en consola
        System.out.println("Constructor publico");
    }

    // Constructor protected
    // Solo puede usarse dentro del paquete
    // o mediante herencia
    protected Clase1(String atributoPublico){

        // Mensaje que se muestra en consola
        System.out.println("Constructor protected");
    }

    // Método public
    // Puede llamarse desde cualquier clase
    public void metodoPublico(){

         // Mensaje que imprime el método
         System.out.println("Metodo public");
    }

    // Método protected
    // Accesible en el mismo paquete
    // y en clases hijas
    public void metodoProtected(){

        // Mensaje que imprime el método
        System.out.println("Metodo protected");
    }
}