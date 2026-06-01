
/**************************************************************
 * EJEMPLO 1: FUNCIÓN CLÁSICA (FUNCTION DECLARATION)
 **************************************************************/

// Llamada a la función antes de su declaración.
// Esto es posible gracias al Hoisting (elevación),
// característica que mueve las declaraciones de funciones
// al inicio del contexto de ejecución.
miFuncion();

/**
 * Función tradicional que muestra un mensaje en consola.
 * Las Function Declarations permiten ser invocadas
 * antes de aparecer físicamente en el código.
 */
function miFuncion() {
    console.log('¡Saludos desde mi función!');
}


/**************************************************************
 * EJEMPLO 2: FUNCIÓN ANÓNIMA ASIGNADA A UNA VARIABLE
 **************************************************************/

/**
 * Se crea una función sin nombre (anónima) y se almacena
 * dentro de la variable myFuncion.
 *
 * A diferencia de las Function Declarations, estas funciones
 * NO pueden ejecutarse antes de ser definidas porque la
 * variable aún no ha sido inicializada.
 */
let myFuncion = function () {
    console.log('¡Saludos desde mi función anónima!');
};


/**************************************************************
 * EJEMPLO 3: FUNCIÓN FLECHA (ARROW FUNCTION)
 **************************************************************/

/**
 * Las Arrow Functions son una sintaxis moderna introducida
 * en ECMAScript 6 (ES6).
 *
 * Características:
 * - Son más compactas.
 * - No poseen su propio contexto "this".
 * - No aplican Hoisting como las funciones tradicionales.
 */
let miFuncionFlecha = () => {
    console.log('¡Saludos desde mi función flecha!');
};

// Ejecución de la función flecha.
miFuncionFlecha();


/**************************************************************
 * EJEMPLO 4: FUNCIÓN FLECHA DE UNA SOLA LÍNEA
 **************************************************************/

/**
 * Cuando una Arrow Function contiene una sola instrucción,
 * se pueden omitir las llaves {}.
 */
const saludar = () =>
    console.log('Saludos a todos desde esta función flecha.');

saludar();

/*
 * Si intentáramos:
 * console.log(saludar());
 *
 * Primero se ejecutaría el console.log interno.
 * Luego la función retornaría undefined porque no tiene
 * una instrucción return explícita.
 */


/**************************************************************
 * EJEMPLO 5: ARROW FUNCTION CON RETURN EXPLÍCITO
 **************************************************************/

/**
 * Función que retorna una cadena de texto.
 * Al utilizar llaves, es obligatorio escribir "return".
 */
const saludar2 = () => {
    return 'Saludos desde la función flecha dos';
};

console.log(saludar2());


/**************************************************************
 * EJEMPLO 6: ARROW FUNCTION CON RETURN IMPLÍCITO
 **************************************************************/

/**
 * Cuando la función devuelve una única expresión,
 * JavaScript realiza el retorno automáticamente.
 */
const saludar3 = () => 'Saludos desde la función flecha tres.';

console.log(saludar3());


/**************************************************************
 * EJEMPLO 7: RETORNAR OBJETOS CON ARROW FUNCTIONS
 **************************************************************/

/**
 * Para devolver un objeto literal se debe encerrar
 * entre paréntesis (), evitando que las llaves sean
 * interpretadas como el cuerpo de la función.
 */
const regresaObjeto = () => ({
    Nombre: 'Cecilia',
    Apellido: 'Farias'
});

console.log(regresaObjeto());


/**************************************************************
 * EJEMPLO 8: ARROW FUNCTION CON PARÁMETROS
 **************************************************************/

/**
 * Recibe un parámetro y lo muestra en consola.
 */
const funcionParametros = (mensaje) => {
    console.log(mensaje);
};

funcionParametros('Saludos desde la función con parámetros.');


/**************************************************************
 * EJEMPLO 9: FUNCIÓN CLÁSICA CON PARÁMETROS
 **************************************************************/

/**
 * Mismo comportamiento que el ejemplo anterior,
 * utilizando sintaxis tradicional.
 */
const funcionParametrosClasica = function (mensaje) {
    console.log(mensaje);
};

funcionParametrosClasica(
    'Saludos desde la función con parámetros clásica.'
);


/**************************************************************
 * EJEMPLO 10: ARROW FUNCTION CON UN SOLO PARÁMETRO
 **************************************************************/

/**
 * Cuando existe un único parámetro,
 * los paréntesis son opcionales.
 */
const funcionConParametros = mensaje =>
    console.log(mensaje);

funcionConParametros(
    'Otra forma de trabajar con la función flecha.'
);


/**************************************************************
 * EJEMPLO 11: ARROW FUNCTION CON VARIOS PARÁMETROS
 **************************************************************/

/**
 * Recibe dos valores y retorna la suma.
 * El return es implícito.
 */
const funcionConParametros2 = (op1, op2) => op1 + op2;

console.log(funcionConParametros2(3, 5));


/**************************************************************
 * EJEMPLO 12: ARROW FUNCTION CON RETURN EXPLÍCITO
 **************************************************************/

/**
 * Versión extendida del ejemplo anterior.
 * Permite realizar operaciones adicionales antes
 * de devolver el resultado.
 */
const funcionConParametros3 = (op1, op2) => {
    let resultado = op1 + op2;
    return resultado;
};

console.log(funcionConParametros3(2, 8));