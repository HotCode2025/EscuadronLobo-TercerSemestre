package domain;

// Clase abstracta:
// NO se puede crear objetos directamente de esta clase
public abstract class FiguraGeometrica {
    
    // Atributo protegido:
    // puede ser utilizado por las clases hijas
    protected String tipoFigura;
    
    
    // Constructor protegido
    // Solo puede ser utilizado por clases hijas
    protected FiguraGeometrica(String tipoFigura){
        
        // Inicializamos el atributo
        this.tipoFigura = tipoFigura;
    }
    
    
    // =========================================
    // MÉTODO ABSTRACTO
    // =========================================
    
    // Un método abstracto NO tiene implementación
    // Obliga a las clases hijas a implementarlo
    public abstract void dibujar();
    
    
    // =========================================
    // MÉTODOS GET Y SET
    // =========================================

    // Devuelve el tipo de figura
    public String getTipoFigura() {
        return tipoFigura;
    }

    // Modifica el tipo de figura
    public void setTipoFigura(String tipoFigura) {
        this.tipoFigura = tipoFigura;
    }

    
    // =========================================
    // MÉTODO toString()
    // =========================================
    
    // Convierte el objeto en texto
    @Override
    public String toString() {
        return "FiguraGeometrica{" + "tipoFigura=" + tipoFigura + '}';
    }  
}