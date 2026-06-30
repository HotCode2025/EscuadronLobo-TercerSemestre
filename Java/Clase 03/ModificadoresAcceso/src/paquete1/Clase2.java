// Paquete al que pertenece esta clase
package paquete1;

// Clase con acceso default
// Solo puede utilizarse dentro del mismo paquete
class Clase2{

    // Atributo default
    // Solo accesible dentro del paquete
    String atributoDefault = "Valor del atributo default";

    /*
    // Constructor comentado
    Clase2(){
       System.out.println("Constructor Default");
    }
    */

    // Constructor default
    Clase2(){

        // Mensaje que se muestra al crear el objeto
        System.out.println("Constructor Default");
    }

    // Método default
    void metodoDefault(){

         // Mensaje que imprime el método
         System.out.println("Metodo Default");

    }
}