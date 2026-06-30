package paquete2;

// Clase pública
// Puede ser utilizada desde cualquier paquete del proyecto
public class Clase4 {

    // Atributo private
    // Solo puede accederse dentro de esta misma clase
    // No puede usarse directamente desde otras clases
    private String atributoPrivate = "atributo Private";


    // Constructor privado
    // Solo puede ejecutarse dentro de esta clase
    // No permite crear objetos desde afuera usando:
    // new Clase4();
    private Clase4(){

        // Mensaje que se imprime al ejecutarse
        System.out.println("Constructor privado");
    }


    // Constructor público
    // Este constructor sí permite crear objetos desde otras clases
    // Recibe un parámetro llamado argumento
    public Clase4(String argumento){

        // this() llama al constructor vacío privado
        // Primero se ejecuta el constructor privado
        // y luego continúa este constructor público
        this();

        // Mensaje que se imprime después
        System.out.println("Constructor publico");
    }


    // Método private
    // Solo puede utilizarse dentro de Clase4
    // No puede llamarse desde otras clases
    private void metodoPrivado(){

        // Mensaje que imprime el método
        System.out.println("Metodo privado");
    }


    // Método GET
    // Sirve para obtener (leer) el valor del atributo privado
    // Es una forma controlada de acceder al atributo
    public String getAtributoPrivate() {

        // Retorna el valor del atributoPrivate
        return atributoPrivate;
    }


    // Método SET
    // Sirve para modificar el valor del atributo privado
    // Recibe un nuevo valor por parámetro
    public void setAtributoPrivate(String atributoPrivate) {

        // this.atributoPrivate hace referencia
        // al atributo de la clase
        //
        // atributoPrivate (sin this)
        // hace referencia al parámetro recibido
        this.atributoPrivate = atributoPrivate;
    }
}