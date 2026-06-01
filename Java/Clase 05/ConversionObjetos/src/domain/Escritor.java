
package domain;

// Clase hija que hereda de Empleado
public class Escritor extends Empleado{
    
    // Atributo final:
    // una vez asignado no puede cambiar
    final TipoEscritura tipoEscritura;
    
    // Constructor de la clase Escritor
    public Escritor(String nombre, double sueldo, TipoEscritura tipoEscritura){
        
        // Llamamos al constructor de la clase padre
        super(nombre, sueldo);
        
        // Inicializamos el tipo de escritura
        this.tipoEscritura = tipoEscritura;
    }

    // Sobrescritura del método obtenerDetalles()
    @Override
    public String obtenerDetalles(){

        // super.obtenerDetalles() obtiene la información de Empleado
        // y agregamos el tipo de escritura
        return super.obtenerDetalles()+" Tipo Escritura: "+tipoEscritura.getDescripcion();
    }

    // Sobrescritura del método toString()
    @Override
    public String toString() {
        return "Escritor(" + " tipoEscritura= " + tipoEscritura + ')' +" "+super.toString();
    }
    
    // Método GET del tipo de escritura
    public TipoEscritura getTipoEscritura(){
        return this.tipoEscritura;
    }

}