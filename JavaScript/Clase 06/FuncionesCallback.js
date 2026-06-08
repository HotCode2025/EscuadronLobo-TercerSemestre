//FUNCIONES BÁSICAS
//definimos la funcion1 
function mifuncion1(){
    console.log("Función 1");
}
//Definimos la funcion 2
function mifuncion2(){
    console.log("Función 2");
}
//Llamamos a las funciones. Se ejecutan en el orden en que fueron llamadas
mifuncion2();
mifuncion1();

//FUNCIONES CALLBACK
//La función recibe un mensaje y lo muestra por consola
function imprimir(mensaje){
    console.log(mensaje);
}
//Función que recibe dos números y una función callback, suma los números y luego llama a la función callback con el resultado

function sumar(op1,op2,funcionCallback){
    //Calcula el resultado de la suma
    let resultado = op1 + op2;
    //Ejecuta la funcion callback enviándole el resultado de la suma
    funcionCallback(`Resultado: ${resultado}`); 
}
//Llamamos a la función sumar, pasando dos números y la función imprimir como callback
sumar(5,3,imprimir); //8

//LLAMADAS ASÍNCRONAS CON setTimeout()
//Función que se ejecuta después de un tiempo determinado, en este caso 3 seg(en milisegundos)
function miFuncionCallback(){
    console.log("Saludo asincrono despues de 3 segudos");
}
//setTimeout ejecuta una función después de un tiempo determinado, en este caso 3000 milisegundos (3segundos)
setTimeout(miFuncionCallback, 3000);
//Función anónima que se ejecuta después de 4 segundos
setTimeout(function(){
    console.log("Saludo asincrono 2") }, 4000)
    
//Función flecha que se ejecuta después de 5 segundos
setTimeout(() => console.log("Saludo asincrono 3"), 5000)  //No trabaja secuencialmente
/*
IMPORTANTE:
Las funciones programadas con setTimeout NO se ejecutan de forma secuencial.
JavaScript continúa ejecutando el resto del código mientras espera
que se cumpla el tiempo indicado.
*/
//FUNCION FLECHA (ARROW FUNCTION) PARA MOSTRAR LA HORA CADA SEGUNDO
let reloj = () => {
    //Obtiene la fecha y hora actual
    let fecha = new Date();
    //Muestra horas, minutos y segundos en formato HH:MM:SS
    console.log(`${fecha.getHours()}:${fecha.getMinutes()}:${fecha.getSeconds()}`);
}
/*
Para mostrar la hora cada segundo, utilizamos setInterval, que ejecuta la función reloj 
repetidamente cada intervalo de tiempo indicado. 
En este caso cada 1000 milisegundos (1 segundo) se ejecuta la función reloj, mostrando la hora actualizada cada segundo.   
*/
setInterval(reloj, 1000);