public class Persona {
    private int id;
    private String nombre;
    private String tel;
    private String email;
    private static int numeroPersonas = 0; //Inicializamos en 0
    //Constructor vacio
    public Persona(){
        this.id = ++Persona.numeroPersonas;
    }
    //Constructor con parámetros(Más de un constructor hablamos de sobrebarga de constructores)
    public Persona(String nombre, String tel, String email){
        this();
        this.nombre = nombre;
        this.tel = tel;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getTel() {
        return tel;
    }

    public void setTel(String tel) {
        this.tel = tel;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        return "Persona{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", tel='" + tel + '\'' +
                ", email='" + email + '\'' +
                '}'; //+super.toString() :con esto seguimos viendo el espacio de memoria que esté ocupando.La referencia.
    }

    public static void main(String[] args) {
        Persona persona1 = new Persona("Juan Perez", "2617077076", "jperez@mail.com");
        System.out.println(persona1);

    }
}

