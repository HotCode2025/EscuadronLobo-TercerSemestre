class Empleado {
    // Constructor de la clase Empleado que recibe nombre y sueldo
    constructor(nombre, sueldo){
        this._nombre = nombre;  // Asigna el nombre al atributo privado _nombre
        this._sueldo = sueldo;  // Asigna el sueldo al atributo privado _sueldo
    }

    obtenerDetalles(){
        return `Empleado: nombre: ${this._nombre},
                sueldo: ${this._sueldo}`;
    }    
}

class Gerente extends Empleado {
        super(nombre, sueldo);  // Llama al constructor de la clase padre para nombre y sueldo
        this._departamento = departamento;  // Asigna el departamento al atributo privado _departamento
    }

    // agregamos Sobrescritura
    obtenerDetalles(){
        return `Gerente: ${super.obtenerDetalles()} depto: ${this._departamento}`;
    }
}

let gerente1 = new Gerente("Carlos", 5000, "Sistemas"); 
console.log(gerente1); // Objeto de la clase hija 

let empleado1 = new Empleado("Juan", 3000); 
console.log(empleado1); // Objeto de la clase padre
