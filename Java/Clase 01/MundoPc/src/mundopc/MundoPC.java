
package mundopc;

import ar.com.system2026.mundopc.*;

public class MundoPC {
    public static void main(String[] args) {
        Monitor monitorHP = new Monitor("HP", 19); //Importar la clase
        Teclado tecladoHP = new Teclado("Bluetooth","HP"); 
        Raton ratonHP = new Raton("Bluetooth", "HP");
        Computadora computadoraHP = new Computadora("Computadora HP", monitorHP, tecladoHP, ratonHP);
        
        Monitor monitorGamer = new Monitor("Gamer", 24); //Importar la clase
        Teclado tecladoGamer = new Teclado("USB","Gamer"); 
        Raton ratonGamer = new Raton("USB", "Gamer");
        Computadora computadoraGamer = new Computadora("Computadora Gamer", monitorGamer, tecladoGamer, ratonGamer);
        
        Monitor monitorASUS = new Monitor("ASUS", 27); //Importar la clase
        Teclado tecladoASUS = new Teclado("Bluetooth","ASUS"); 
        Raton ratonASUS = new Raton("USB", "ASUS");
        Computadora computadoraASUS = new Computadora("Computadora ASUS", monitorASUS, tecladoASUS, ratonASUS);
        
        Monitor monitorMSI = new Monitor("MSI", 24); //Importar la clase
        Teclado tecladoMSI = new Teclado("PS/2","MSI"); 
        Raton ratonMSI = new Raton("PS/2", "MSI");
        Computadora computadoraMSI = new Computadora("Computadora MSI", monitorMSI, tecladoMSI, ratonMSI);
        
        Computadora computadorasVarias = new Computadora("Computadora de diferentes marcas", monitorHP, tecladoGamer, ratonHP);
        
        Orden orden1 = new Orden(); //Inicializando el arreglo vacio
        Orden orden2 = new Orden(); //Nueva lista para el objeto orden2
        orden1.agregarComputadora(computadoraHP);
        orden1.agregarComputadora(computadoraGamer);
        orden1.agregarComputadora(computadoraASUS);
        orden1.agregarComputadora(computadoraMSI);
        orden1.agregarComputadora(computadorasVarias);
        orden1.agregarComputadora(computadoraHP);
        orden1.agregarComputadora(computadoraGamer);
        orden1.agregarComputadora(computadoraASUS);
        orden1.agregarComputadora(computadoraMSI);
        orden1.agregarComputadora(computadoraHP);

        orden1.mostrarOrden();        
        
        orden2.agregarComputadora(computadorasVarias);
        orden2.mostrarOrden();
       
        //Crear mas objetos de tipo computadora con todos sus elementos
        //completar una lista en el objeto orden1 que llegue a 10 elementos
        //probar de esta manera los metodos al maximo rendimiento
        
        
    }
}
