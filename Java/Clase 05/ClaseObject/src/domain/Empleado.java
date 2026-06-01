package domain;

// Importamos la clase Objects
// Se utiliza para facilitar comparaciones y generación de hash
import java.util.Objects;

// Clase padre o superclase
public class Empleado {
    
    // =========================================
    // ATRIBUTOS
    // =========================================
    
    // protected permite acceso desde:
    // - la misma clase
    // - clases hijas
    // - mismo paquete
    protected String nombre;
    protected double sueldo;
    
    
    // =========================================
    // CONSTRUCTOR
    // =========================================
    
    // Constructor que inicializa los atributos
    public Empleado(String nombre, double sueldo){
        
        // this hace referencia al objeto actual
        this.nombre = nombre;
        this.sueldo = sueldo;
    }
    
    
    // =========================================
    // MÉTODO PERSONALIZABLE
    // =========================================
    
    // Método pensado para sobrescribirse
    // en clases hijas
    public String obtenerDetalles(){
        return "Nombre: "+this.nombre+", Sueldo: "+this.sueldo;
    }
    
    
    // =========================================
    // MÉTODOS GET Y SET
    // =========================================
    
    // Devuelve el nombre
    public String getNombre() {
        return nombre;
    }
    
    // Modifica el nombre
    public void setNombre(String nombre) {
        this.nombre = nombre;
    }
    
    // Devuelve el sueldo
    public double getSueldo() {
        return sueldo;
    }
    
    // Modifica el sueldo
     public void setSueldo(double sueldo) {
        this.sueldo = sueldo;
    }
    
    
    // =========================================
    // MÉTODO toString()
    // =========================================
    
     // Sobrescribimos toString()
     // para mostrar información legible del objeto
     @Override
     public String toString(){
         return "Empleado{" + "nombre=" + nombre + ", sueldo=" + sueldo +'}';
     }
     
     
    // =========================================
    // MÉTODO hashCode()
    // =========================================
     
     // Genera un código numérico del objeto
     // basado en sus atributos
     @Override
     public int hashCode(){
         
         // Valor inicial
         int hash = 7;
         
         // Generamos hash del nombre
         hash = 53 * hash + Objects.hashCode(this.nombre);
         
         // Generamos hash del sueldo
         hash = 53 * hash + 
                 (int) (Double.doubleToLongBits(this.sueldo) ^ 
                 (Double.doubleToLongBits(this.sueldo) >>> 32));
         
         return hash;
     }
     
    
    // =========================================
    // MÉTODO equals()
    // =========================================
    
    // Compara si dos objetos tienen el mismo contenido
    @Override
     public boolean equals(Object obj){
         
        // Verifica si ambos objetos son exactamente
        // la misma referencia en memoria
        if(this == obj){
            return true;
        }
        
        // Verifica si el objeto recibido es null
        if (obj == null){
            return false;
        }
          
        // Verifica si ambos objetos son de la misma clase
        if (getClass() != obj.getClass()){
            return false;
        }
        
        // Conversión del objeto genérico a Empleado
        final Empleado other = (Empleado) obj;
        
        // Comparación del atributo sueldo
        if (Double.doubleToLongBits(this.sueldo) != 
            Double.doubleToLongBits(other.sueldo)){
            return false;
        }
     
        // Comparación segura del atributo nombre
        if (!Objects.equals(this.nombre, other.nombre)){
            return false;
        }
        
        // Si todo coincide, los objetos son iguales
        return true;
     }
    
} 