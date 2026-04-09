//creamos clase DispositivoEntrada
class DispositivoEntrada {
    constructor(tipoEntrada, marca){
        this._tipoEntrada = tipoEntrada;
        this._marca = marca;
    }

    get tipoEntrada(){
        return this._tipoEntrada;
    }
    
    set tipoEntrada(tipoEntrada){
        this._tipoEntrada = tipoEntrada;
    }
    
    get marca(){
        return this._marca;
    }

    set marca(marca){
        this._marca = this.marca;
    }
}

//creamos clase Raton
class Raton extends DispositivoEntrada {
    static contadorRatones = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idRaton = ++Raton.contadorRatones;        
    }

    get idRaton(){
        return this._idRaton;
    }
    //devolvemos en un string los valores que recibimos
    toString(){
        return `Raton: [idRaton: ${this._idRaton}, tipoEntrada: ${this._tipoEntrada}, Marca: ${this._marca}]`;
    }
}

//creamos ratones
let raton1 = new Raton('USB', 'HyperX');
let raton2 = new Raton('PS2', 'Genius');
//mostramos en consola
console.log(raton1.toString());
console.log(raton2.toString());

//creamos la clase teclado
class Teclado extends DispositivoEntrada{
    static contadorTeclado = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idTeclado = ++Teclado.contadorTeclado;
    }    
    get idTeclado(){
        return this._idTeclado;
    }
    //devolvemos en un string los valores que recibimos
    toString(){
        return `Teclado: [idTeclado: ${this._idTeclado}, tipoEntrada: ${this._tipoEntrada}, Marca: ${this._marca}]`;
    }
}

//creamos los teclados
let teclado1 = new Teclado('Bluetooth', 'Logitec');
let teclado2 = new Teclado('USB', 'HP');
//mostramos en consola
console.log(teclado1.toString());
console.log(teclado2.toString());

//creamos clase Monitor
class Monitor {
    static contadorMonitores = 0;

    constructor(marca, tamaño){
        this._idMonitor = ++Monitor.contadorMonitores;
        this._marca = marca;
        this._tamaño = tamaño;
    }

    get marca(){
        return this._marca;
    }

    set marca(marca){
        this._marca = marca;
    }

    get tamaño(){
        return this._tamaño;
    }

    set tamaño(tamaño){
        this._tamaño = tamaño;
    }

    toString(){
        return `Monitor: [idMonitor: ${this._idMonitor}, Marca: ${this._marca}, Tamaño: ${this._tamaño}]`;
    }
}

//creamos Monitores
let monitor1 = new Monitor('Samsung', '24 pulgadas');
let monitor2 = new Monitor('LG', '27 pulgadas');
//mostramos en consola
console.log(monitor1.toString());
console.log(monitor2.toString());

//creamos la clase Computadoras
class Computadoras{
    static contadorComputadoras = 0;

    constructor(nombre, monitor, teclado, raton){
        this._idComputadora = ++Computadoras.contadorComputadoras;
        this._nombre = nombre;
        this._monitor = monitor;
        this._teclado = teclado;
        this._raton = raton;
    }
    toString(){
        return `Computadora ${this._idComputadora}: ${this._nombre}\n ${this._monitor}\n ${this._raton}\n ${this._teclado}`
    }
}

//creamos las computadoras y asignamos un monitor, un teclado y un raton a cada una
let computadora1 = new Computadoras ('PC GAMER', monitor1, raton1, teclado1);
let computadora2 = new Computadoras ('ACER', monitor2, raton2, teclado2);
//mostramos en consola
console.log(computadora1.toString());
console.log(computadora2.toString());

//creamos la clase Orden
class Orden {
    static contadorOrdenes = 0;

    constructor(){
        this._idOrden = ++Orden.contadorOrdenes;
        this._computadoras = [];
    }
    
    agregarComputadora(computadora){
        this._computadoras.push(computadora);
    }

    mostrarOrden(){
        let computadorasStr = '';
        //agregamos computadoras a la orden
        for(let computadora of this._computadoras){
            computadorasStr += '\n' + computadora.toString();
        }

        console.log(`Orden: ${this._idOrden} ${computadorasStr}`);
    }  
}

//creamos las ordenes, agregamos computadoras y mostramos la orden
let orden1 = new Orden();
orden1.agregarComputadora(computadora1);
orden1.agregarComputadora(computadora2);
orden1.mostrarOrden();

let orden2 = new Orden();
orden2.agregarComputadora(computadora1);
orden2.agregarComputadora(computadora2);
orden2.mostrarOrden();