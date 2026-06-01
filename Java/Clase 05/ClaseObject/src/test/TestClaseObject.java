package test;

// Importamos todas las clases del paquete domain
import domain.*;

// Clase de prueba
public class TestClaseObject {
    
    public static void main(String[] args){
        
        // Creamos dos objetos diferentes de tipo Empleado
        // Aunque tienen los mismos valores,
        // son objetos distintos en memoria
        
        Empleado empleado1 = new Empleado("Juan", 5000);
        Empleado empleado2 = new Empleado("Juan", 5000);
        
        
        // =========================================
        // Comparación de referencias con ==
        // =========================================
        
        // El operador == compara referencias en memoria
        // Pregunta si ambos apuntan exactamente al mismo objeto
        
        if(empleado1 == empleado2){
            System.out.println("Tienen la misma referencia en la memoria");
        }
        else{
          System.out.println("Tienen distinta referencia en memoria");  
        }   
        
        
        // =========================================
        // Comparación de contenido con equals()
        // =========================================
        
        // equals() compara el contenido de los objetos
        // siempre y cuando este método haya sido sobrescrito
        
        if(empleado1.equals(empleado2)){
            System.out.println("Los objetos son iguales en contenidos");
        }
        else{
          System.out.println("Los objetos son distintos en contenidos");  
        }
        
        
        // =========================================
        // Comparación de hashCode()
        // =========================================
        
        // hashCode() devuelve un valor numérico
        // asociado al objeto
        
        // Si dos objetos son iguales en contenido,
        // normalmente deberían tener el mismo hashCode
        
        if(empleado1.hashCode() == empleado2.hashCode()){
            System.out.println("El valor hasCode es igual");
        }
        else {
            System.out.println("El valor hasCode es diferente"); 
        }
    }
}