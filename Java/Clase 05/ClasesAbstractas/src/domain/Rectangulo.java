package domain;

// Clase Rectangulo que hereda de FiguraGeometrica
public class Rectangulo extends FiguraGeometrica{
    
    // =========================================
    // CONSTRUCTOR
    // =========================================
    
    // Constructor de Rectangulo
    public Rectangulo (String tipoFigura){
        
        // Llamamos al constructor de la clase padre
        super(tipoFigura);
    }
    
    
    // =========================================
    // IMPLEMENTACIÓN DEL MÉTODO ABSTRACTO
    // =========================================
    
    @Override
    public void dibujar() {
        
        // getClass() obtiene la clase actual
        // getSimpleName() obtiene el nombre simple de la clase
        
        System.out.println("Se imprime un: "
                + this.getClass().getSimpleName());
    }
}