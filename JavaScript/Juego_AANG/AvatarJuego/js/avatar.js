/**
 * ============================================================
 *  avatar.js — LOS ELEMENTOS: La Leyenda de Aang
 *  Lógica completa del juego (sin referencias a Simpsons)
 * ============================================================
 *
 *  Contenido:
 *  1. Datos de personajes y ataques
 *  2. Estado global del juego
 *  3. Referencias al DOM
 *  4. Selección de personaje
 *  5. Oponente aleatorio
 *  6. Ejecución del ataque
 *  7. Actualización del DOM (vidas, barras HP, expresiones)
 *  8. Expresiones por resultado (gana / pierde / empata)
 *  9. Verificar fin del juego
 *  10. Reiniciar
 *  11. Registro de eventos (addEventListener)
 * ============================================================
 */

// ─────────────────────────────────────────────────────────
//  1. DATOS DE PERSONAJES Y ATAQUES
// ─────────────────────────────────────────────────────────

/**
 * PERSONAJES: objeto con los datos de cada guerrero.
 * Clave = value del <input type="radio"> en el HTML.
 *
 * expresiones: textos que se muestran en el bocadillo
 *   según el resultado del turno (gana / pierde / empata).
 * imagen: nombre del archivo PNG del personaje.
 */
const PERSONAJES = {
  aang: {
    nombre:   "Aang",
    elemento: "Aire",
    emoji:    "🌪️",
    imagen:   "./assets/AANG.png",
    expresiones: {
      gana:   "¡YAAAH! ¡El viento nunca miente! 🌪️✨",
      pierde: "¡Auch! Eso dolió... ¡pero no me rindo! 😤",
      empata: "¡El equilibrio es la clave del Avatar! 🔵"
    }
  },
  katara: {
    nombre:   "Katara",
    elemento: "Agua",
    emoji:    "💧",
    imagen:   "./assets/KATARA.png",
    expresiones: {
      gana:   "¡El agua siempre encuentra su camino! 💧🏆",
      pierde: "¡Grrr! ¡El agua no se rinde, vuelvo más fuerte! 😠",
      empata: "¡Fluimos igual de fuerte... por ahora! 💧"
    }
  },
  zuko: {
    nombre:   "Zuko",
    elemento: "Fuego",
    emoji:    "🔥",
    imagen:   "./assets/ZUKO.png",
    expresiones: {
      gana:   "¡MI FUEGO ES IMPARABLE! 🔥👊 ¡HONOR!",
      pierde: "¡IMPOSIBLE! ¡Esto no ha terminado! 😡🔥",
      empata: "¡Ni tú ni yo... esta vez. 😤🔥"
    }
  },
  toph: {
    nombre:   "Toph",
    elemento: "Tierra",
    emoji:    "🌱",
    imagen:   "./assets/TOPH.png",
    expresiones: {
      gana:   "¡JA! ¿Eso fue todo? ¡Soy la mejor del mundo! 🌱💪",
      pierde: "¡Bien jugado! Pero la próxima te aplasto 😤🪨",
      empata: "¡Está bien, esta vez empatamos... ESTA VEZ! 🌱"
    }
  }
};

/**
 * ATAQUES: array de los 4 ataques disponibles.
 * id → coincide con el id del <button> en el HTML.
 * poder → número que se compara con el del CPU para decidir el turno.
 */
const ATAQUES = [
  { id: "boton-fuego",  nombre: "Fuego",  emoji: "🔥", poder: 4 },
  { id: "boton-agua",   nombre: "Agua",   emoji: "💧", poder: 3 },
  { id: "boton-tierra", nombre: "Tierra", emoji: "🌱", poder: 2 },
  { id: "boton-aire",   nombre: "Aire",   emoji: "🌪️", poder: 3 }
];

// ─────────────────────────────────────────────────────────
//  2. ESTADO GLOBAL DEL JUEGO
// ─────────────────────────────────────────────────────────

/**
 * Un solo objeto centraliza todas las variables que cambian.
 * Así el reinicio es simple: restaurar cada propiedad.
 */
let estado = {
  personajeJugador:  null,   // objeto del PERSONAJES elegido
  personajeOponente: null,   // objeto del oponente (aleatorio)
  vidasJugador:      3,      // vidas restantes del jugador
  vidasOponente:     3,      // vidas restantes del oponente
  ronda:             1,      // contador de rondas
  juegoTerminado:    false   // true cuando alguien llega a 0 vidas
};

// ─────────────────────────────────────────────────────────
//  3. REFERENCIAS AL DOM
// ─────────────────────────────────────────────────────────

// Secciones que se muestran/ocultan durante el juego
const secPersonaje  = document.getElementById("seleccionar-personaje");
const secAtaque     = document.getElementById("seleccionar-ataque");
const secMensajes   = document.getElementById("mensajes");
const secResultado  = document.getElementById("resultado-final");
const secReiniciar  = document.getElementById("reiniciar");

// Elementos dinámicos del HUD
const spanVidasJugador   = document.getElementById("vidas-jugador-num");
const spanVidasOponente  = document.getElementById("vidas-oponente-num");
const spanIconosJugador  = document.getElementById("vidas-jugador-iconos");
const spanIconosOponente = document.getElementById("vidas-oponente-iconos");
const barraHPJugador     = document.getElementById("hp-jugador-barra");
const barraHPOponente    = document.getElementById("hp-oponente-barra");
const divMensaje         = document.getElementById("mensaje-texto");
const divResultExpresion = document.getElementById("resultado-expresion");
const divResultadoTexto  = document.getElementById("resultado-texto");
const divResultadoDet    = document.getElementById("resultado-detalle");
const spanNombreJugador  = document.getElementById("nombre-jugador");
const divImgJugador      = document.getElementById("img-jugador");
const divImgOponente     = document.getElementById("img-oponente");
const divRonda           = document.getElementById("hud-ronda");

// ─────────────────────────────────────────────────────────
//  4. SELECCIONAR PERSONAJE JUGADOR
// ─────────────────────────────────────────────────────────

/**
 * seleccionarPersonajeJugador()
 *
 * Lee cuál <input type="radio"> está marcado.
 * Guarda el personaje en el estado.
 * Muestra la sección de batalla con las imágenes de los personajes.
 *
 * Se activa con el botón "¡ENTRAR AL COMBATE!"
 */
function seleccionarPersonajeJugador() {
  // Buscar el radio que está checked
  let valorSeleccionado = null;
  document.querySelectorAll('input[name="personaje"]').forEach(function(radio) {
    if (radio.checked) valorSeleccionado = radio.value;
  });

  // Validar que se haya elegido uno
  if (!valorSeleccionado) {
    alert("⚠️ ¡Debes seleccionar un guerrero elemental antes de combatir!");
    return;
  }

  // Guardar personaje del jugador en el estado
  estado.personajeJugador  = PERSONAJES[valorSeleccionado];

  // La CPU elige un personaje diferente al del jugador
  estado.personajeOponente = seleccionarOponenteAleatorio(valorSeleccionado);

  // Confirmación visual con expresión del personaje
  alert(`✅ ${estado.personajeJugador.expresiones.gana.split("!")[0]}!\n¡Tu personaje es ${estado.personajeJugador.nombre}!`);

  // Actualizar el HUD con los personajes elegidos
  spanNombreJugador.textContent = estado.personajeJugador.nombre.toUpperCase();

  // Mostrar imágenes reales en el HUD (en lugar de emojis)
  divImgJugador.innerHTML  = `<img src="${estado.personajeJugador.imagen}"
    alt="${estado.personajeJugador.nombre}" class="hud-char-real" />`;
  divImgOponente.innerHTML = `<img src="${estado.personajeOponente.imagen}"
    alt="${estado.personajeOponente.nombre}" class="hud-char-real" />`;

  // Ocultar selección, mostrar batalla y mensajes
  secPersonaje.classList.add("oculto");
  secAtaque.classList.remove("oculto");
  secMensajes.classList.remove("oculto");

  // Inicializar las barras de HP al 100%
  barraHPJugador.style.width  = "100%";
  barraHPOponente.style.width = "100%";
}

// ─────────────────────────────────────────────────────────
//  5. OPONENTE ALEATORIO
// ─────────────────────────────────────────────────────────

/**
 * seleccionarOponenteAleatorio(excluir)
 *
 * Obtiene las claves del objeto PERSONAJES, filtra la del jugador
 * y elige una al azar con Math.random().
 *
 * @param {string} excluir - key del personaje ya elegido
 * @returns {object} personaje oponente
 */
function seleccionarOponenteAleatorio(excluir) {
  const disponibles = Object.keys(PERSONAJES).filter(k => k !== excluir);
  const idx = Math.floor(Math.random() * disponibles.length);
  return PERSONAJES[disponibles[idx]];
}

// ─────────────────────────────────────────────────────────
//  6. EJECUTAR ATAQUE
// ─────────────────────────────────────────────────────────

/**
 * ejecutarAtaque(idAtaque)
 *
 * Compara el poder del jugador con el de la CPU.
 * Actualiza vidas, barras HP, ronda y mensaje de turno.
 * Llama a verificarFinJuego() al final.
 *
 * @param {string} idAtaque - id del <button> pulsado
 */
function ejecutarAtaque(idAtaque) {
  if (estado.juegoTerminado) return; // bloquear si el juego ya terminó

  // Buscar el ataque del jugador en el array ATAQUES
  const ataqueJug = ATAQUES.find(a => a.id === idAtaque);

  // La CPU elige su ataque al azar
  const ataqueCPU = ATAQUES[Math.floor(Math.random() * ATAQUES.length)];

  // ── COMPARAR PODERES Y GENERAR EXPRESIÓN ──────────────
  let expresion = "";
  let mensajeTurno = "";

  if (ataqueJug.poder > ataqueCPU.poder) {
    // Jugador gana el turno
    estado.vidasOponente--;
    expresion    = estado.personajeJugador.expresiones.gana;
    mensajeTurno = `
      <strong>${estado.personajeJugador.nombre}</strong> atacó con
      ${ataqueJug.emoji} <strong>${ataqueJug.nombre}</strong> (Poder ${ataqueJug.poder})
      y el oponente con ${ataqueCPU.emoji} ${ataqueCPU.nombre} (Poder ${ataqueCPU.poder}).
      <br><span class="msg-victoria">🏆 ¡GANASTE el turno! ${expresion}</span>
    `;
  } else if (ataqueJug.poder < ataqueCPU.poder) {
    // CPU gana el turno
    estado.vidasJugador--;
    expresion    = estado.personajeJugador.expresiones.pierde;
    mensajeTurno = `
      <strong>${estado.personajeJugador.nombre}</strong> atacó con
      ${ataqueJug.emoji} <strong>${ataqueJug.nombre}</strong> (Poder ${ataqueJug.poder})
      pero la CPU usó ${ataqueCPU.emoji} ${ataqueCPU.nombre} (Poder ${ataqueCPU.poder}).
      <br><span class="msg-derrota">💔 ¡Perdiste el turno! ${expresion}</span>
    `;
    sacudirElemento(secAtaque); // animación de sacudida al perder vida
  } else {
    // Empate de turno
    expresion    = estado.personajeJugador.expresiones.empata;
    mensajeTurno = `
      ${ataqueJug.emoji} <strong>${ataqueJug.nombre}</strong> (${ataqueJug.poder}) vs
      ${ataqueCPU.emoji} <strong>${ataqueCPU.nombre}</strong> (${ataqueCPU.poder}).
      <br><span class="msg-empate">🤝 ¡EMPATE de turno! ${expresion}</span>
    `;
  }

  // Mostrar el mensaje en el bocadillo
  divMensaje.innerHTML = mensajeTurno;

  // Avanzar el contador de ronda
  estado.ronda++;
  divRonda.textContent = `Ronda ${estado.ronda}`;

  // Actualizar el DOM (vidas, corazones y barras HP)
  actualizarVidasDOM();

  // Comprobar si alguien llegó a 0 vidas
  verificarFinJuego();
}

// ─────────────────────────────────────────────────────────
//  7. ACTUALIZAR VIDAS EN EL DOM
// ─────────────────────────────────────────────────────────

/**
 * actualizarVidasDOM()
 *
 * Sincroniza los <span> de vidas, los corazones y las barras HP
 * con los valores actuales del estado.
 */
function actualizarVidasDOM() {
  // Números de vidas
  spanVidasJugador.textContent  = estado.vidasJugador;
  spanVidasOponente.textContent = estado.vidasOponente;

  // Corazones emoji: ❤️ por vida restante, 💔 por vida perdida
  spanIconosJugador.textContent  = generarCorazones(estado.vidasJugador,  3);
  spanIconosOponente.textContent = generarCorazones(estado.vidasOponente, 3);

  // Barras HP: porcentaje = (vidas / 3) * 100
  const pctJug = Math.max(0, (estado.vidasJugador  / 3) * 100);
  const pctOpo = Math.max(0, (estado.vidasOponente / 3) * 100);
  barraHPJugador.style.width  = pctJug + "%";
  barraHPOponente.style.width = pctOpo + "%";

  // La barra cambia de color cuando queda poca vida
  if (pctJug <= 33)  barraHPJugador.classList.add("hp-critico");
  else               barraHPJugador.classList.remove("hp-critico");
  if (pctOpo <= 33)  barraHPOponente.classList.add("hp-critico");
  else               barraHPOponente.classList.remove("hp-critico");
}

/**
 * generarCorazones(actuales, max)
 * Devuelve string de emojis: ❤️ por vida que queda, 💔 por vida perdida.
 */
function generarCorazones(actuales, max) {
  let str = "";
  for (let i = 0; i < max; i++) {
    str += (i < actuales) ? "❤️" : "💔";
  }
  return str;
}

// ─────────────────────────────────────────────────────────
//  8. ANIMACIÓN DE SACUDIDA AL PERDER VIDA
// ─────────────────────────────────────────────────────────

/**
 * sacudirElemento(el)
 *
 * Agrega la clase CSS "sacudir" que dispara la animación @keyframes.
 * La quita 450ms después para que pueda dispararse de nuevo.
 */
function sacudirElemento(el) {
  el.classList.add("sacudir");
  setTimeout(() => el.classList.remove("sacudir"), 450);
}

// ─────────────────────────────────────────────────────────
//  9. VERIFICAR FIN DEL JUEGO
// ─────────────────────────────────────────────────────────

/**
 * verificarFinJuego()
 *
 * Comprueba si alguno (o ambos) llegaron a 0 vidas.
 * Muestra el resultado con la expresión del personaje.
 */
function verificarFinJuego() {
  let terminado   = false;
  let textoFinal  = "";
  let detalle     = "";
  let expresionFinal = "";

  if (estado.vidasJugador <= 0 && estado.vidasOponente <= 0) {
    // Empate total
    terminado      = true;
    textoFinal     = "🤝 ¡EMPATE TOTAL!";
    expresionFinal = "😤 " + estado.personajeJugador.expresiones.empata;
    detalle        = `¡Los dos guerreros cayeron al mismo tiempo! ¡Rematch!`;

  } else if (estado.vidasOponente <= 0) {
    // Jugador ganó
    terminado      = true;
    textoFinal     = `🏆 ¡${estado.personajeJugador.nombre.toUpperCase()} GANÓ!`;
    expresionFinal = "🌟 " + estado.personajeJugador.expresiones.gana;
    detalle        = `¡Dominaste los elementos y venciste al oponente en ${estado.ronda - 1} rondas!`;

  } else if (estado.vidasJugador <= 0) {
    // CPU ganó
    terminado      = true;
    textoFinal     = "💀 ¡DERROTA!";
    expresionFinal = "😤 " + estado.personajeJugador.expresiones.pierde;
    detalle        = `¡El oponente te venció! Entrena más y vuelve más fuerte, ${estado.personajeJugador.nombre}.`;
  }

  if (terminado) {
    estado.juegoTerminado = true;

    // Escribir resultado en el DOM
    divResultExpresion.textContent = expresionFinal;
    divResultadoTexto.innerHTML    = textoFinal;
    divResultadoDet.innerHTML      = detalle;

    // Ocultar sección de ataque, mostrar resultado y reinicio
    secAtaque.classList.add("oculto");
    secResultado.classList.remove("oculto");
    secReiniciar.classList.remove("oculto");
  }
}

// ─────────────────────────────────────────────────────────
//  10. REINICIAR EL JUEGO
// ─────────────────────────────────────────────────────────

/**
 * reiniciarJuego()
 *
 * Resetea el estado y el DOM al estado inicial.
 * No recarga la página: solo restaura variables y vuelve
 * a mostrar la sección de selección de personaje.
 */
function reiniciarJuego() {
  // Restaurar estado
  estado.personajeJugador  = null;
  estado.personajeOponente = null;
  estado.vidasJugador      = 3;
  estado.vidasOponente     = 3;
  estado.ronda             = 1;
  estado.juegoTerminado    = false;

  // Restaurar DOM
  spanVidasJugador.textContent   = "3";
  spanVidasOponente.textContent  = "3";
  spanIconosJugador.textContent  = "❤️❤️❤️";
  spanIconosOponente.textContent = "❤️❤️❤️";
  barraHPJugador.style.width     = "100%";
  barraHPOponente.style.width    = "100%";
  barraHPJugador.classList.remove("hp-critico");
  barraHPOponente.classList.remove("hp-critico");
  spanNombreJugador.textContent  = "TÚ";
  divImgJugador.innerHTML        = "🤺";
  divImgOponente.innerHTML       = "🤖";
  divRonda.textContent           = "Ronda 1";
  divMensaje.innerHTML           = "¡Elige tu ataque para comenzar!";
  divResultExpresion.textContent = "";
  divResultadoTexto.innerHTML    = "";
  divResultadoDet.innerHTML      = "";

  // Desmarcar todos los radios
  document.querySelectorAll('input[name="personaje"]').forEach(r => r.checked = false);

  // Mostrar selección; ocultar el resto
  secPersonaje.classList.remove("oculto");
  secAtaque.classList.add("oculto");
  secMensajes.classList.add("oculto");
  secResultado.classList.add("oculto");
  secReiniciar.classList.add("oculto");
}

// ─────────────────────────────────────────────────────────
//  11. REGISTRO DE EVENTOS
// ─────────────────────────────────────────────────────────

/**
 * addEventListener('click', función):
 * Asocia una función a un clic. Se ejecuta cada vez que el usuario pulsa.
 *
 * Para los 4 botones de ataque usamos forEach para no repetir 4 líneas.
 */

// Botón seleccionar personaje
document.getElementById("boton-personaje")
  .addEventListener("click", seleccionarPersonajeJugador);

// Botones de ataque (iterar el array evita repetir código)
ATAQUES.forEach(function(ataque) {
  document.getElementById(ataque.id)
    .addEventListener("click", function() {
      ejecutarAtaque(ataque.id);
    });
});

// Botón reiniciar
document.getElementById("boton-reiniciar")
  .addEventListener("click", reiniciarJuego);
