
package domain;

// Enumeración de tipos de escritura
public enum TipoEscritura {
    
    // Constantes del enum
    CLASICO ("Escritura a mano"),

    MODERNO ("Escritura digital");
    
    // Atributo privado y final
    private final String Descripcion;
    
    // Constructor del enum
    private TipoEscritura(String descripcion){
        this.Descripcion = descripcion;
    }

    // Método GET
    public String getDescripcion(){
        return this.Descripcion;
    }
}
