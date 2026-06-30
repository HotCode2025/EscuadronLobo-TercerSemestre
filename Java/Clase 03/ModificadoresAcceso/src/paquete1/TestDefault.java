package paquete1;

import paquete2.Clase4;

public class TestDefault {
    public static void main(String[] arg) {

       /*
        * Creamos objeto de ClaseHija2.
        */
       ClaseHija2 claseH2 = new ClaseHija2();

       /*
        * Accedemos al atributo default.
        *
        * Funciona porque estamos
        * en el mismo paquete.
        */
       claseH2.atributoDefault = "Cambio desde la prueba";
       System.out.println("claseH2 atributo default = " + claseH2.atributoDefault);

       /*
        * Creamos objeto de Clase4.
        */
       Clase4 clase4 = new Clase4("Publico");

       /*
        * Obtenemos el atributo privado
        * usando GET.
        */
       System.out.println(clase4.getAtributoPrivate());

       /*
        * Modificamos el atributo privado
        * usando SET.
        */
       clase4.setAtributoPrivate("Cambio");

       System.out.println("clase4 = " + clase4.getAtributoPrivate());
    }
}

