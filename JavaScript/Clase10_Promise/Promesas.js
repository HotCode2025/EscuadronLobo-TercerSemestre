// ======================================================
// PROMESAS EN JAVASCRIPT
// ======================================================

// Se crea una nueva promesa.
// Una promesa representa una operación que puede completarse
// correctamente (resolve) o fallar (reject).
let miPromesa = new Promise((resolver, rechazar) => {

    // Variable que determina el resultado de la promesa.
    let expresion = true;

    // Si la condición es verdadera, la promesa se resuelve.
    if (expresion) {
        resolver("La promesa se cumplió");
    } 
    // Si la condición es falsa, la promesa se rechaza.
    else {
        rechazar("La promesa no se cumplió");
    }
});

// ------------------------------------------------------
// MANEJO DE PROMESAS CON .then()
// ------------------------------------------------------

// miPromesa.then(
//     valor => console.log(valor),
//     error => console.log(error)
// );

// ------------------------------------------------------
// MANEJO DE PROMESAS CON .then() Y .catch()
// ------------------------------------------------------

// miPromesa
//     .then(valor => console.log(valor))
//     .catch(error => console.log(error));


// ======================================================
// PROMESA CON RETARDO UTILIZANDO setTimeout()
// ======================================================

// let promesa = new Promise((resolver) => {
//     console.log("Inicio de la promesa");

//     // Simula una tarea asíncrona de 3 segundos.
//     setTimeout(
//         () => resolver("Saludos con promesa, callback, función flecha y setTimeout"),
//         3000
//     );

//     console.log("Fin de la promesa");
// });

// La ejecución del método then ocurrirá cuando la promesa
// se resuelva luego de los 3 segundos.
// promesa.then(valor => console.log(valor));


// ======================================================
// FUNCIONES ASÍNCRONAS (async)
// ======================================================

// La palabra reservada async indica que la función
// devuelve automáticamente una promesa.
async function miFuncionConPromesa() {
    return "Saludos con promesa y async";
}

// miFuncionConPromesa().then(valor => console.log(valor));


// ======================================================
// USO DE async Y await
// ======================================================

// await permite esperar el resultado de una promesa
// antes de continuar con la ejecución.
async function funcionConPromesaYAwait() {

    let miPromesa = new Promise((resolver) => {
        resolver("Promesa con await");
    });

    // Espera la resolución de la promesa y luego muestra el resultado.
    console.log(await miPromesa);
}

// funcionConPromesaYAwait();


// ======================================================
// COMBINACIÓN DE PROMESAS, async, await Y setTimeout
// ======================================================

// Ejemplo completo de programación asíncrona.
async function funcionConPromesaAwaitYSetTimeout() {

    let miPromesa = new Promise((resolver) => {

        console.log("Inicio de la promesa con await y setTimeout");

        // Simula una operación que tarda 3 segundos.
        setTimeout(() => {
            resolver("Promesa con await y setTimeout");
        }, 3000);

        console.log("Fin de la promesa con await y setTimeout");
    });

    // La ejecución se pausa hasta que la promesa sea resuelta.
    console.log(await miPromesa);
}

// Se ejecuta la función asíncrona.
// El resultado final se mostrará después de 3 segundos.
funcionConPromesaAwaitYSetTimeout();