/**
 * ============================================================
 *  avatar.js — Lógica del Juego Avatar Simpson Edition
 * ============================================================
 *
 *  Este archivo contiene TODA la lógica del juego:
 *  1. Datos de personajes y ataques (objetos JS)
 *  2. Estado global del juego (variables de control)
 *  3. Selección de personaje por el jugador
 *  4. Selección aleatoria del oponente (CPU)
 *  5. Lógica de ataque y comparación de poderes
 *  6. Actualización dinámica del DOM (vidas, mensajes)
 *  7. Detección del fin del juego
 *  8. Función de reinicio
 *
 *  Todos los cambios visuales se hacen con innerHTML y
 *  classList, sin recargar la página.
 * ============================================================
 */

// ─────────────────────────────────────────────
//  1. DATOS: PERSONAJES Y ATAQUES
// ─────────────────────────────────────────────

/**
 * PERSONAJES: objeto que guarda la info de cada personaje.
 * La clave es el value del <input type="radio"> en el HTML.
 *
 * Cada personaje tiene:
 * - nombre:    nombre mostrado en pantalla
 * - emoji:     ícono visual grande
 * - elemento:  tipo de bendición
 * - frase:     frase estilo Simpsons al ser seleccionado
 */
const PERSONAJES = {
  zuko:   {
    nombre:   "Zuko",
    emoji:    "🤴🔥",
    elemento: "Fuego",
    frase:    "¡Yo soy Zuko, Señor del Fuego! ¡Como Bart, pero con más drama! 🔥"
  },
  katara: {
    nombre:   "Katara",
    emoji:    "👧💧",
    elemento: "Agua",
    frase:    "¡Soy Katara, maestra del agua! ¡Tan sabia como Lisa! 💧"
  },
  aang:   {
    nombre:   "Aang",
    emoji:    "👦🌪️",
    elemento: "Aire",
    frase:    "¡Soy Aang, el Avatar! ¡Como Bart sin pelo y más budista! 🌪️"
  },
  toph:   {
    nombre:   "Toph",
    emoji:    "👩🌱",
    elemento: "Tierra",
    frase:    "¡Soy Toph! ¡Tan terca como Homero cuando hay donuts de por medio! 🌱"
  }
};

/**
 * ATAQUES: array con todos los ataques disponibles.
 * Cada ataque tiene:
 * - id:     coincide con el id del <button> en el HTML
 * - nombre: nombre mostrado en los mensajes
 * - emoji:  ícono del ataque
 * - poder:  número que se compara con el del oponente
 */
const ATAQUES = [
  { id: "boton-fuego",  nombre: "Fuego",  emoji: "🔥", poder: 4 },
  { id: "boton-agua",   nombre: "Agua",   emoji: "💧", poder: 3 },
  { id: "boton-tierra", nombre: "Tierra", emoji: "🌱", poder: 2 },
  { id: "boton-aire",   nombre: "Aire",   emoji: "🌪️", poder: 3 }
];

// ─────────────────────────────────────────────
//  2. ESTADO GLOBAL DEL JUEGO
// ─────────────────────────────────────────────

/**
 * El estado concentra todas las variables que cambian durante
 * el juego. Tener un objeto único hace fácil el reseteo.
 */
let estado = {
  personajeJugador:  null,  // objeto del personaje elegido (de PERSONAJES)
  personajeOponente: null,  // objeto del personaje del oponente (aleatorio)
  vidasJugador:      3,     // vidas iniciales del jugador
  vidasOponente:     3,     // vidas iniciales del oponente
  juegoTerminado:    false  // bandera: true cuando alguien llega a 0 vidas
};

// ─────────────────────────────────────────────
//  3. REFERENCIAS AL DOM
// ─────────────────────────────────────────────

// Secciones que se muestran/ocultan durante el juego
const secPersonaje    = document.getElementById("seleccionar-personaje");
const secAtaque       = document.getElementById("seleccionar-ataque");
const secMensajes     = document.getElementById("mensajes");
const secResultado    = document.getElementById("resultado-final");
const secReiniciar    = document.getElementById("reiniciar");

// Elementos de texto dinámico (vidas y mensajes)
const spanVidasJugador        = document.getElementById("vidas-jugador-num");
const spanVidasOponente       = document.getElementById("vidas-oponente-num");
const spanIconosJugador       = document.getElementById("vidas-jugador-iconos");
const spanIconosOponente      = document.getElementById("vidas-oponente-iconos");
const divMensaje              = document.getElementById("mensaje-texto");
const divResultadoTexto       = document.getElementById("resultado-texto");
const divResultadoDetalle     = document.getElementById("resultado-detalle");
const spanNombreJugador       = document.getElementById("nombre-jugador");
const spanEmojiJugador        = document.getElementById("emoji-jugador");
const spanEmojiOponente       = document.getElementById("emoji-oponente");

// ─────────────────────────────────────────────
//  4. FUNCIÓN: SELECCIONAR PERSONAJE JUGADOR
// ─────────────────────────────────────────────

/**
 * seleccionarPersonajeJugador()
 *
 * Lee cuál radio button está marcado y guarda el personaje
 * elegido en el estado. Luego muestra la sección de batalla.
 *
 * Se activa con el botón "Seleccionar".
 */
function seleccionarPersonajeJugador() {
  // Buscar cuál input tipo radio está marcado (checked)
  let valorSeleccionado = null;

  // querySelectorAll devuelve todos los radio del grupo "personaje"
  const radios = document.querySelectorAll('input[name="personaje"]');

  radios.forEach(function(radio) {
    if (radio.checked) {
      valorSeleccionado = radio.value; // guarda "zuko", "katara", etc.
    }
  });

  // Si ninguno fue seleccionado, alertamos y salimos
  if (!valorSeleccionado) {
    // Usamos alert (igual que en el código original)
    alert("⚠️ ¡D'OH! Debes seleccionar un personaje, como Homero necesita sus donuts.");
    return; // detiene la función aquí
  }

  // Guardar el personaje en el estado usando la clave
  estado.personajeJugador = PERSONAJES[valorSeleccionado];

  // Seleccionar oponente aleatorio
  estado.personajeOponente = seleccionarOponenteAleatorio(valorSeleccionado);

  // Mostrar frase de confirmación al jugador
  alert(`✅ ${estado.personajeJugador.frase}`);

  // Actualizar el DOM con los datos del jugador y oponente
  spanNombreJugador.textContent  = estado.personajeJugador.nombre.toUpperCase();
  spanEmojiJugador.textContent   = estado.personajeJugador.emoji;
  spanEmojiOponente.textContent  = estado.personajeOponente.emoji;

  // Ocultar la sección de selección y mostrar la de batalla
  secPersonaje.classList.add("oculto");
  secAtaque.classList.remove("oculto");
  secMensajes.classList.remove("oculto");
}

// ─────────────────────────────────────────────
//  5. FUNCIÓN: SELECCIONAR OPONENTE ALEATORIO
// ─────────────────────────────────────────────

/**
 * seleccionarOponenteAleatorio(excluir)
 *
 * Elige un personaje distinto al del jugador de forma aleatoria.
 * Math.random() devuelve un número entre 0 y 1.
 * Math.floor() redondea hacia abajo.
 *
 * @param {string} excluir - key del personaje ya elegido
 * @returns {object} - personaje oponente
 */
function seleccionarOponenteAleatorio(excluir) {
  // Obtener las claves del objeto PERSONAJES: ["zuko", "katara", "aang", "toph"]
  const claves = Object.keys(PERSONAJES);

  // Filtrar para excluir el personaje del jugador
  const disponibles = claves.filter(function(clave) {
    return clave !== excluir;
  });

  // Índice aleatorio entre 0 y disponibles.length - 1
  const indiceAleatorio = Math.floor(Math.random() * disponibles.length);

  // Retornar el personaje usando la clave aleatoria
  return PERSONAJES[disponibles[indiceAleatorio]];
}

// ─────────────────────────────────────────────
//  6. FUNCIÓN: ATAQUE DEL OPONENTE (CPU)
// ─────────────────────────────────────────────

/**
 * ataqueOponenteAleatorio()
 *
 * La CPU elige un ataque al azar del array ATAQUES.
 * Simula al oponente como "Homero pensando en donuts".
 *
 * @returns {object} - objeto ataque aleatorio
 */
function ataqueOponenteAleatorio() {
  const indice = Math.floor(Math.random() * ATAQUES.length);
  return ATAQUES[indice]; // devuelve { nombre, emoji, poder }
}

// ─────────────────────────────────────────────
//  7. FUNCIÓN: EJECUTAR UN ATAQUE
// ─────────────────────────────────────────────

/**
 * ejecutarAtaque(idAtaque)
 *
 * Se llama cuando el jugador hace clic en un botón de ataque.
 * Compara el poder del jugador con el del oponente y actualiza
 * vidas y mensajes.
 *
 * @param {string} idAtaque - id del botón pulsado
 */
function ejecutarAtaque(idAtaque) {
  // Si el juego ya terminó, no hacer nada
  if (estado.juegoTerminado) return;

  // Buscar el objeto del ataque del jugador por su id
  const ataquejugador = ATAQUES.find(function(a) {
    return a.id === idAtaque;
  });

  // El oponente elige su ataque al azar
  const ataqueOponente = ataqueOponenteAleatorio();

  // ── COMPARAR PODERES ──────────────────────
  let mensajeTurno = "";
  let jugadorPierdeVida  = false;
  let oponentePierdeVida = false;

  if (ataquejugador.poder > ataqueOponente.poder) {
    // Jugador gana este turno → el oponente pierde vida
    oponentePierdeVida = true;
    mensajeTurno = `
      ${estado.personajeJugador.nombre} atacó con ${ataquejugador.emoji} ${ataquejugador.nombre} 
      (Poder ${ataquejugador.poder}) y el oponente respondió con 
      ${ataqueOponente.emoji} ${ataqueOponente.nombre} (Poder ${ataqueOponente.poder}).
      <br><strong>🎉 ¡GANASTE el turno! ¡Como Bart escapando de Skinner!</strong>
    `;
  } else if (ataquejugador.poder < ataqueOponente.poder) {
    // Oponente gana este turno → el jugador pierde vida
    jugadorPierdeVida = true;
    mensajeTurno = `
      ${estado.personajeJugador.nombre} atacó con ${ataquejugador.emoji} ${ataquejugador.nombre} 
      (Poder ${ataquejugador.poder}) pero el oponente atacó con 
      ${ataqueOponente.emoji} ${ataqueOponente.nombre} (Poder ${ataqueOponente.poder}).
      <br><strong>😵 ¡Perdiste el turno! ¡D'OH! Como Homero tropezando...</strong>
    `;
  } else {
    // Empate → nadie pierde vida
    mensajeTurno = `
      ${estado.personajeJugador.nombre} atacó con ${ataquejugador.emoji} ${ataquejugador.nombre} 
      y el oponente con ${ataqueOponente.emoji} ${ataqueOponente.nombre}. ¡Mismo poder!
      <br><strong>🤝 ¡EMPATE! ¡Como Homero y Ned Flanders de acuerdo!</strong>
    `;
  }

  // ── ACTUALIZAR VIDAS ──────────────────────
  if (jugadorPierdeVida) {
    estado.vidasJugador--;           // restar una vida al jugador
    sacudirElemento(secAtaque);      // animación de sacudida
  }
  if (oponentePierdeVida) {
    estado.vidasOponente--;          // restar una vida al oponente
  }

  // Mostrar el mensaje del turno en el DOM
  divMensaje.innerHTML = mensajeTurno;

  // Actualizar los números y corazones en pantalla
  actualizarVidasDOM();

  // Verificar si el juego terminó
  verificarFinJuego();
}

// ─────────────────────────────────────────────
//  8. FUNCIÓN: ACTUALIZAR VIDAS EN EL DOM
// ─────────────────────────────────────────────

/**
 * actualizarVidasDOM()
 *
 * Sincroniza los <span> del HTML con los valores del estado.
 * Genera los corazones como string de emojis.
 */
function actualizarVidasDOM() {
  // Actualizar números
  spanVidasJugador.textContent  = estado.vidasJugador;
  spanVidasOponente.textContent = estado.vidasOponente;

  // Generar corazones: "❤️❤️❤️" para 3 vidas, "❤️❤️💔" para 2, etc.
  spanIconosJugador.textContent  = generarCorazones(estado.vidasJugador,  3);
  spanIconosOponente.textContent = generarCorazones(estado.vidasOponente, 3);
}

/**
 * generarCorazones(vidasActuales, vidasMax)
 *
 * Devuelve un string de emojis de corazón:
 * ❤️ por cada vida que queda, 💔 por cada vida perdida.
 *
 * @param {number} actuales - vidas restantes
 * @param {number} max      - vidas máximas iniciales
 * @returns {string}
 */
function generarCorazones(actuales, max) {
  let resultado = "";
  for (let i = 0; i < max; i++) {
    resultado += (i < actuales) ? "❤️" : "💔";
  }
  return resultado;
}

// ─────────────────────────────────────────────
//  9. FUNCIÓN: SACUDIR ELEMENTO (ANIMACIÓN)
// ─────────────────────────────────────────────

/**
 * sacudirElemento(elemento)
 *
 * Agrega la clase CSS "sacudir" al elemento, que dispara
 * la animación de keyframes. La quita después de 400ms
 * para que pueda volver a aplicarse en el siguiente golpe.
 *
 * @param {HTMLElement} elemento
 */
function sacudirElemento(elemento) {
  elemento.classList.add("sacudir");
  setTimeout(function() {
    elemento.classList.remove("sacudir");
  }, 400);
}

// ─────────────────────────────────────────────
//  10. FUNCIÓN: VERIFICAR FIN DE JUEGO
// ─────────────────────────────────────────────

/**
 * verificarFinJuego()
 *
 * Comprueba si alguno de los jugadores llegó a 0 vidas.
 * Si el juego terminó:
 * - Bloquea el juego (estado.juegoTerminado = true)
 * - Oculta los botones de ataque
 * - Muestra la sección de resultado
 * - Muestra el botón de reinicio
 */
function verificarFinJuego() {
  let mensajeFinal   = "";
  let detalleFinal   = "";
  let terminado      = false;

  if (estado.vidasJugador <= 0 && estado.vidasOponente <= 0) {
    // Empate total (ambos llegaron a 0 al mismo tiempo)
    mensajeFinal = "🤝 ¡EMPATE TOTAL!";
    detalleFinal = "¡Nadie gana, como cuando Homero olvida quién ganó!";
    terminado    = true;

  } else if (estado.vidasOponente <= 0) {
    // El jugador ganó
    mensajeFinal = `🏆 ¡${estado.personajeJugador.nombre.toUpperCase()} GANÓ!`;
    detalleFinal = `¡Excelente, ${estado.personajeJugador.nombre}! 
                   ¡Eres tan genial como Bart burlando a Skinner! 🎉`;
    terminado    = true;

  } else if (estado.vidasJugador <= 0) {
    // El oponente ganó
    mensajeFinal = "😵 ¡PERDISTE!";
    detalleFinal = `¡D'OH! Caíste como Homero en el sofá. ¡Intenta de nuevo! 🍩`;
    terminado    = true;
  }

  // Si el juego terminó, actualizar la pantalla
  if (terminado) {
    estado.juegoTerminado = true;

    // Mostrar el resultado en el DOM
    divResultadoTexto.innerHTML   = mensajeFinal;
    divResultadoDetalle.innerHTML = detalleFinal;

    // Ocultar ataques, mostrar resultado y reinicio
    secAtaque.classList.add("oculto");
    secResultado.classList.remove("oculto");
    secReiniciar.classList.remove("oculto");
  }
}

// ─────────────────────────────────────────────
//  11. FUNCIÓN: REINICIAR EL JUEGO
// ─────────────────────────────────────────────

/**
 * reiniciarJuego()
 *
 * Restablece el estado a los valores iniciales y vuelve
 * a mostrar la pantalla de selección de personaje.
 * No recarga la página: solo resetea variables y el DOM.
 */
function reiniciarJuego() {
  // Restablecer estado
  estado.personajeJugador  = null;
  estado.personajeOponente = null;
  estado.vidasJugador      = 3;
  estado.vidasOponente     = 3;
  estado.juegoTerminado    = false;

  // Resetear los corazones y números visualmente
  spanVidasJugador.textContent  = "3";
  spanVidasOponente.textContent = "3";
  spanIconosJugador.textContent  = "❤️❤️❤️";
  spanIconosOponente.textContent = "❤️❤️❤️";
  spanNombreJugador.textContent  = "TÚ";
  spanEmojiJugador.textContent   = "🤺";
  spanEmojiOponente.textContent  = "🤖";

  // Limpiar mensajes
  divMensaje.innerHTML        = "¡Espera el primer ataque!";
  divResultadoTexto.innerHTML = "";
  divResultadoDetalle.innerHTML = "";

  // Desmarcar todos los radio buttons
  document.querySelectorAll('input[name="personaje"]').forEach(function(r) {
    r.checked = false;
  });

  // Mostrar selección de personaje; ocultar el resto
  secPersonaje.classList.remove("oculto");
  secAtaque.classList.add("oculto");
  secMensajes.classList.add("oculto");
  secResultado.classList.add("oculto");
  secReiniciar.classList.add("oculto");
}

// ─────────────────────────────────────────────
//  12. REGISTRAR EVENT LISTENERS
// ─────────────────────────────────────────────

/**
 * addEventListener asocia una función a un evento del DOM.
 * Sintaxis: elemento.addEventListener('evento', función)
 *
 * Usamos 'click' para botones.
 * La función se ejecuta cada vez que el usuario hace clic.
 */

// Botón seleccionar personaje
document.getElementById("boton-personaje")
  .addEventListener('click', seleccionarPersonajeJugador);

// Botones de ataque: iteramos el array ATAQUES para no repetir código
ATAQUES.forEach(function(ataque) {
  document.getElementById(ataque.id)
    .addEventListener('click', function() {
      ejecutarAtaque(ataque.id); // pasamos el id del botón pulsado
    });
});

// Botón reiniciar
document.getElementById("boton-reiniciar")
  .addEventListener('click', reiniciarJuego);
