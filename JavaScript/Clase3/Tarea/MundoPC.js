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
        this._marca = marca;
    }
}

class Raton extends DispositivoEntrada {
    static contadorRatones = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idRaton = ++Raton.contadorRatones;        
    }

    get idRaton(){
        return this._idRaton;
    }
    toString(){
        return `Raton: [idRaton: ${this._idRaton}, tipoEntrada: ${this._tipoEntrada}, Marca: ${this._marca}]`;
    }
}

let raton1 = new Raton('USB', 'HyperX');
let raton2 = new Raton('PS2', 'Genius');

console.log(raton1);
console.log(raton2);

class Teclado extends DispositivoEntrada{
    static contadorTeclado = 0;

    constructor(tipoEntrada, marca) {
        super(tipoEntrada, marca);
        this._idTeclado = ++Teclado.contadorTeclado;
    }    
    get idTeclado(){
        return this._idTeclado;
    }
    toString(){
        return `Teclado: [idTeclado: ${this._idTeclado}, tipoEntrada: ${this._tipoEntrada}, Marca: ${this._marca}]`;
    }
}

let teclado1 = new Teclado('Bluetooth', 'Logitec');
let teclado2 = new Teclado('USB', 'HP');

console.log(teclado1);
console.log(teclado2);

class Monitor {
    static contadorMonitores = 0;

    constructor(marca, tamanio) {
        this._idMonitor = ++Monitor.contadorMonitores;
        this._marca = marca;
        this._tamanio = tamanio;
        
    }   

    get marca(){
        return this._marca;
    }
    set marca(marca){
        this._marca = marca;
    }

    get tamanio(){
        return this._tamanio;
    }
    set tamanio(tamanio){
        this._tamanio = tamanio;
    }
    toString(){
        return `Monitor: [idMonitor: ${this._idMonitor}, Marca: ${this._marca}, Tamaño: ${this._tamanio}]`;
    }
}

let monitor1 = new Monitor('Samsung', '24');
let monitor2 = new Monitor('MSI','27');
console.log(monitor1.toString());
console.log(monitor2.toString());

class Computadoras{
    static contadorComputadoras = 0;

    constructor(nombre, monitor, teclado, raton){
        this._idComputadora = ++Computadoras.contadorComputadoras;
        this._nombre = nombre;
        this._monitor = monitor;
        this._teclado = teclado;
        this._raton = raton;
    }
    //APLICAMOS POLIMORFISMO
    toString(){
        return `Computadora ${this._idComputadora}: ${this._nombre}
        ${this._monitor.toString()}
        ${this._raton.toString()}
        ${this._teclado.toString()}`
}
}

let computadora1 = new Computadoras ('PC GAMER', monitor1, raton1, teclado1);
let computadora2 = new Computadoras ('ACER', monitor2, raton2, teclado2);
console.log(computadora1.toString());
console.log(computadora2.toString());

class Orden{
    static contadorOrdenes = 0;

    constructor(){
        this._idOrden = ++Orden.contadorOrdenes;
        this._computadoras = [];
    }
    get idOrden(){
        return this._idOrden;
    }
    agregarComputadora(computadora){
        this._computadoras.push(computadora);
    }
    mostrarOrden(){
        let computadorasOrden = '';
        for (let computadora of this._computadoras){
            computadorasOrden += `\n${computadora}`;
        }
        console.log(`Orden; ${this._idOrden}, Computadoras: ${computadorasOrden}`);
    }
}

let orden1 = new Orden();
orden1.agregarComputadora(computadora1);
orden1.agregarComputadora(computadora2);
orden1.agregarComputadora(computadora2);
orden1.mostrarOrden();

let orden2 = new Orden();
orden2.agregarComputadora(computadora1);
orden2.agregarComputadora(computadora1);
orden2.agregarComputadora(computadora2);
orden2.mostrarOrden();
