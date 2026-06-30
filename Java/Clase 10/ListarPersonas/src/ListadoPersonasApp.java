import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Aplicación principal para la gestión de un listado de personas.
 *
 * Permite al usuario interactuar mediante un menú en consola para:
 * - Agregar personas.
 * - Listar las personas registradas.
 * - Finalizar la ejecución del programa.
 */
public class ListadoPersonasApp {

    public static void main(String[] args) {

        // Objeto encargado de leer la entrada del usuario desde la consola.
        Scanner entrada = new Scanner(System.in);

        // Lista que almacenará todas las personas creadas durante la ejecución.
        // Se declara fuera del ciclo para conservar la información mientras
        // el programa permanezca en ejecución.
        List<Persona> personas = new ArrayList<>();

        // Variable de control utilizada para finalizar el menú cuando el usuario lo solicite.
        var salir = false;

        // Ciclo principal de la aplicación.
        // Se ejecuta continuamente hasta que la variable "salir" sea verdadera.
        while(!salir){

            // Muestra las opciones disponibles al usuario.
            mostrarMenu();

            try{

                // Ejecuta la opción seleccionada por el usuario.
                // El método devuelve true únicamente cuando se elige salir.
                salir = ejecutarOperacion(entrada, personas);

            } catch (Exception e){

                // Captura cualquier excepción producida durante la ejecución
                // (por ejemplo, si el usuario ingresa un dato inválido).
                System.out.println("Ocurrió un error: "+e.getMessage());

            }

            // Salto de línea para mejorar la presentación del menú.
            System.out.println();

        }//Fin del ciclo while

    }//Fin método main


    /**
     * Muestra el menú principal de opciones.
     */
    private static void mostrarMenu(){

        // Se utiliza un Text Block para mejorar la legibilidad
        // del menú mostrado en consola.
        System.out.print("""
                ******* Listado de Personas *******
                1. Agregar 
                2. Listar
                3. Salir
                """);

        // Solicita al usuario que seleccione una opción.
        System.out.print("Digite una de las opciones; ");

    }//Fin del método mostrar menú


    /**
     * Ejecuta la operación elegida por el usuario.
     *
     * @param entrada  Scanner utilizado para leer datos desde teclado.
     * @param personas Lista donde se almacenan las personas registradas.
     * @return true si el usuario decide salir del programa; false en caso contrario.
     */
    private static boolean ejecutarOperacion(Scanner entrada, List<Persona>personas){

        // Lee la opción ingresada y la convierte a entero.
        var opcion = Integer.parseInt(entrada.nextLine());

        // Variable que controla la continuidad del menú.
        var salir = false;

        // Evalúa la opción seleccionada utilizando la sintaxis moderna
        // de switch expressions (Java 14+).
        switch (opcion){

            case 1 -> {//Agregar una persona a la lista

                // Solicita los datos necesarios para crear una nueva persona.
                System.out.print("Digite el nombre: ");
                var nombre = entrada.nextLine();

                System.out.print("Digite el teléfono: ");
                var tel = entrada.nextLine();

                System.out.print("Digite el correo: ");
                var email = entrada.nextLine();

                // Se instancia un nuevo objeto Persona utilizando
                // la información ingresada por el usuario.
                var persona = new Persona(nombre, tel, email);

                // Agrega el nuevo objeto a la colección.
                personas.add(persona);

                // Informa la cantidad actual de elementos almacenados.
                System.out.println("La lista tiene: " + personas.size() + " elementos");

            }//Fin caso 1


            case 2 -> {//Listar a las personas

                System.out.println("Listado de personas: ");

                // Recorre toda la colección e imprime cada elemento.
                // Se utiliza una referencia al método println, lo que hace
                // el código más limpio y legible.
                //
                // Equivale a:
                // personas.forEach(persona -> System.out.println(persona));
                personas.forEach(System.out::println);

            }//Fin caso 2


            case 3 -> { //Salir del ciclo

                // Mensaje de despedida antes de finalizar la aplicación.
                System.out.println("Hasta Pronto... ");

                // Cambia el estado de la variable para que el ciclo principal termine.
                salir = true;

            }//Fin del caso 3


            default ->

                // Se ejecuta cuando el usuario ingresa una opción
                // que no existe dentro del menú.
                    System.out.println("Opción incorrecta: "+opcion);

        } //Fin del switch

        // Devuelve el estado de la variable para indicar si el programa
        // debe continuar ejecutándose o finalizar.
        return salir;

    }//Fin del método ejecutarOperacion

}//Fin de la clase ListadoPersonasApp


