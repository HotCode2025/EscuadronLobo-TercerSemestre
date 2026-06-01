package test;

// Importamos las clases del paquete domain
import domain.*;

// Clase de prueba
public class TestAbstractas {
    
    public static void main(String[] args){
        
        // =========================================
        // POLIMORFISMO
        // =========================================
        
        // Variable tipo FiguraGeometrica
        // almacenando un objeto Rectangulo
        
        FiguraGeometrica figura = new Rectangulo("Rectangulo");
        
        
        // Llamamos al método dibujar()
        // Se ejecuta el método de Rectangulo
        figura.dibujar();
    }
}
//SEGUIR CON CLASE 6