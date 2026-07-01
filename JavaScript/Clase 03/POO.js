class Empleado{
    constructor(nombre, sueldo){
        this._nombre = nombre;
        this._sueldo = sueldo;
    }
    obtenerDetalles(){
        return `Empleado: ${this._nombre},
        Sueldo: ${this._sueldo}`
    }
}

class Gerente extends Empleado{
    constructor(nombre, sueldo, departamento){
        super(nombre, sueldo);
        this._departamento = departamento;
    }

    //Agregamos la sobre escritura
    obtenerDetalles(){
        return `Gerente: ${super.obtenerDetalles()}, dept: ${this._departamento}`;
    }
}

//polimorfismo = multiples formas en metodo de ejecucion
function imprimir(tipo){//recibe una nariable
    console.log(tipo.obtenerDetalles());

    //instanceof = es un metodo que permite saber el tipo de dato que se usa
    if(tipo instanceof Gerente){
        console.log("es de tipo gerente");
    }else if(tipo instanceof Empleado){//
        console.log("es de tipop empleado");
    }else if(tipo instanceof Object){//el orden simpre sigue por jerarquia
        console.log("el tipo es Object");
    }
}

const gerente1 = new Gerente("zelada", 5000, "systemas")
console.log(gerente1);

const empleado1 = new Empleado("maicol", 3000)
console.log(empleado1);

imprimir(gerente1);
imprimir(empleado1);
