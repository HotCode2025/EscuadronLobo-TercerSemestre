package domain;

// Clase padre o superclase
public class Empleado {
    
    // Atributos protegidos:
    // protected permite que las clases hijas puedan acceder directamente
    protected String nombre;
    protected double sueldo;
    
    // Constructor de la clase Empleado
    public Empleado(String nombre, double sueldo){
        
        // Inicializamos los atributos con los valores recibidos
        this.nombre = nombre;
        this.sueldo = sueldo;
    }
    
    // Método pensado para ser sobrescrito por las clases hijas
    // Devuelve los detalles básicos del empleado
    public String obtenerDetalles(){
        return "Nombre: "+this.nombre+", Sueldo: "+this.sueldo;
    }
    
    // Método GET para obtener el nombre
    public String getNombre() {
        return nombre;
    }
    
    // Método SET para modificar el nombre
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    // Método GET para obtener el sueldo
    public double getSueldo() {
        return sueldo;
    }
    
    // Método SET para modificar el sueldo
     public void setSueldo(double sueldo) {
        this.sueldo = sueldo;
    }
     
     // Sobrescritura del método toString()
     // Permite mostrar el objeto de manera más legible
     @Override
     public String toString(){
         return "Empleado{" + "nombre=" + nombre + ", sueldo=" + sueldo +'}';
     }
    
}
