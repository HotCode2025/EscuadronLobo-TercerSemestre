package test;

import domain.*;

// Clase de prueba
public class TestConversionObjetos {
    
    public static void main(String[] args){
        
        // Variable tipo Empleado
        Empleado empleado;
        
        // Upcasting implícito:
        // Un objeto Escritor se guarda en una variable Empleado
        empleado = new Escritor("Juan", 5000, TipoEscritura.CLASICO);
        
        // Se ejecuta el método sobrescrito de Escritor
        System.out.println(empleado.obtenerDetalles());

        // empleado.getTipoEscritura();
        // No se puede porque la referencia es tipo Empleado
        
        
        // ==============================
        // DOWNCASTING
        // ==============================
        
        // Convertimos la referencia padre a hija
        
        // Opción 1:
        // ((Escritor)empleado).getTipoEscritura();

        // Opción 2:
        Escritor escritor = (Escritor)empleado;
        
        // Ahora sí podemos acceder al método propio de Escritor
        escritor.getTipoEscritura();
        
        
        // ==============================
        // UPCASTING
        // ==============================
        
        // Convertimos nuevamente a tipo Empleado
        Empleado empleado2 = escritor;
        
        // Sigue ejecutando el método sobrescrito
        System.out.println(empleado2.obtenerDetalles());
        
    }
    
}
