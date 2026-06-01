"use strict"; // Manejo de errores
//Veamos como evitar este error

try {
  let x = 10;
  miFuncion();
  throw "Mi Error";
} catch (error) {
  console.log(typeof error);
} finally {
  console.log("Termina la revisión de errores");
}

console.log("Continuemos..."); // Esto no se llega a ver porque esta bloqueado

let resultado = -5;

try {
  //y = 5;
  if (isNaN(resultado)) throw "El resultado no es un número válido";
  else if (resultado === "") throw "Es cadena vacía";
  else if (resultado >= 0) throw "El resultado es positivo";
  else if (resultado <= 0) throw "El resultado es negativo";
} catch (error) {
  console.log(error);
  console.log(error.name);
  console.log(error.message);
} finally {
  console.log("Termina la revisión de errores 2");
}
