package domain;

public class Persona {
    private final int idPersona;
    //private static int contadorPersonas;
    private static int contadorPersonas = 1; //reemplaza bloque static
    
    // Contructor -> reemplaza bloque no static
    
    //static{ //Bloque de inicialización estático
        //System.out.println("Ejecución del bloque estático");
        //++Persona.contadorPersonas;
        //idPersona = 10; No es estático un atributo por eso tenemos error
    //}
    
    //{ //Bloque de inicialización No estático (Contexto dinámico)
        //System.out.println("Ejecución del bloque No estático");
        //this.idPersona = Persona.contadorPersonas++; //Incrementamos al atributo
    //}
    
    //Los bloques de inicialización se ejecutan antes del constructor
    
    public Persona(){
        System.out.println("Ejecución del constructor");
        System.out.println("Inicialización atributos");
        
        this.idPersona = contadorPersonas++;        
    }
    
    
    //public Persona(){
    //    System.out.println("Ejecucion del constructor");
    //}
    
    public int getIdPersona(){
        return this.idPersona;
    }

    @Override
    public String toString() {
        return "Persona{" + "idPersona=" + idPersona + '}';
    }
       
}
