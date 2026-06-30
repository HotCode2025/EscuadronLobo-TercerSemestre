// Paquete al que pertenece la clase
package test;

// Clase principal
public class TestAutoboxingUnboxing {

    // Método main: punto de entrada del programa
    public static void main(String[] arg) {

        // =====================================================
        // CLASES ENVOLVENTES (WRAPPER CLASSES)
        // =====================================================

        /*
         * Java posee clases especiales llamadas Wrapper
         * (clases envolventes).
         *
         * Estas clases permiten convertir tipos primitivos
         * en objetos.
         *
         * Relación entre primitivos y Wrapper:
         *
         * int     -> Integer
         * long    -> Long
         * float   -> Float
         * double  -> Double
         * boolean -> Boolean
         * byte    -> Byte
         * char    -> Character
         * short   -> Short
         */

        // =====================================================
        // TIPO PRIMITIVO
        // =====================================================

        // Variable primitiva de tipo int
        int enteroPrim = 10;

        // Se imprime el valor del entero primitivo
        System.out.println("enteroPrim = " + enteroPrim);

        // =====================================================
        // AUTOBOXING
        // =====================================================

        /*
         * Integer es una clase (objeto).
         *
         * Aquí Java convierte automáticamente el valor
         * primitivo 10 en un objeto Integer.
         *
         * Ese proceso se llama AUTOBOXING.
         */

        Integer entero = 10;

        /*
         * doubleValue()
         * convierte el valor Integer a double.
         *
         * Resultado:
         * 10.0
         */

        System.out.println("entero = " + entero.doubleValue());

        // =====================================================
        // UNBOXING
        // =====================================================

        /*
         * Aquí Java convierte automáticamente el objeto Integer
         * nuevamente a un tipo primitivo int.
         *
         * Ese proceso se llama UNBOXING.
         */

        int entero2 = entero;

        // Se imprime el valor convertido nuevamente a int
        System.out.println("entero2 = " + entero2);
    }
}