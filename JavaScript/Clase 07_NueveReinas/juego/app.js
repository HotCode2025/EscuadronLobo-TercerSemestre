/**
 * ============================================================
 *  app.js — Interfaz de Usuario del Visualizador N Reinas
 * ============================================================
 *
 *  Este archivo conecta la lógica del algoritmo (NueveReinas.js)
 *  con los elementos HTML.
 *
 *  Responsabilidades:
 *  - Dibujar tableros en el DOM
 *  - Animar el proceso de backtracking paso a paso
 *  - Navegar entre múltiples soluciones
 *  - Mostrar el arreglo de índices de cada solución
 * ============================================================
 */

// ─────────────────────────────────────────────
//  ESTADO GLOBAL DE LA APLICACIÓN
// ─────────────────────────────────────────────

/**
 * Estado centralizado. Todas las funciones lo leen / modifican.
 * Usar un objeto único facilita el reset y evita variables sueltas.
 */
const estado = {
  n:               8,          // Tamaño actual del tablero
  soluciones:      [],         // Array de soluciones encontradas
  pasos:           [],         // Array de pasos (para animación)
  indiceSolucion:  0,          // Índice de la solución actualmente visible
  animacionId:     null,       // ID del setTimeout de animación (para cancelarla)
  animando:        false,      // ¿Está corriendo la animación?
};

// ─────────────────────────────────────────────
//  REFERENCIAS A ELEMENTOS DEL DOM
// ─────────────────────────────────────────────

const elTableroProceso   = document.getElementById('tableroProceso');
const elTableroSolucion  = document.getElementById('tableroSolucion');
const elInputN           = document.getElementById('inputN');
const elBtnResolver      = document.getElementById('btnResolver');
const elBtnSiguiente     = document.getElementById('btnSiguiente');
const elInfoSoluciones   = document.getElementById('infoSoluciones');
const elIndicesSection   = document.getElementById('indicesSection');
const elIndicesDisplay   = document.getElementById('indicesDisplay');

// ─────────────────────────────────────────────
//  CREAR Y DIBUJAR UN TABLERO EN EL DOM
// ─────────────────────────────────────────────

/**
 * crearTablero(contenedor, n)
 *
 * Genera el grid de celdas vacías dentro de un elemento contenedor.
 * El tablero tiene N filas × N columnas = N² celdas.
 *
 * @param {HTMLElement} contenedor - Div donde se insertará el tablero
 * @param {number}      n          - Tamaño del tablero
 */
function crearTablero(contenedor, n) {
  // Limpia cualquier contenido anterior
  contenedor.innerHTML = '';

  // Define el CSS Grid: N columnas de igual tamaño
  contenedor.style.gridTemplateColumns = `repeat(${n}, 1fr)`;

  // Crea cada celda
  for (let fila = 0; fila < n; fila++) {
    for (let col = 0; col < n; col++) {
      const celda = document.createElement('div');

      // Clase "clara" u "oscura" siguiendo el patrón del ajedrez
      // (fila + col) par → clara; impar → oscura
      celda.className = `celda ${(fila + col) % 2 === 0 ? 'clara' : 'oscura'}`;

      // ID único para encontrar la celda rápidamente: p. ej. "proc-2-5"
      celda.id = `${contenedor.id}-${fila}-${col}`;

      contenedor.appendChild(celda);
    }
  }
}

// ─────────────────────────────────────────────
//  DIBUJAR REINAS EN UN TABLERO
// ─────────────────────────────────────────────

/**
 * dibujarReinas(prefijo, tableroArray, n)
 *
 * Limpia las reinas actuales y dibuja las del tableroArray recibido.
 *
 * @param {string}   prefijo      - 'tableroProceso' o 'tableroSolucion'
 * @param {number[]} tableroArray - Array donde tableroArray[fila] = columna (-1 = vacía)
 * @param {number}   n            - Tamaño del tablero
 */
function dibujarReinas(prefijo, tableroArray, n) {
  // Primero limpiar todas las celdas de reinas anteriores
  for (let fila = 0; fila < n; fila++) {
    for (let col = 0; col < n; col++) {
      const celda = document.getElementById(`${prefijo}-${fila}-${col}`);
      if (!celda) continue;
      celda.classList.remove('reina');
      celda.innerHTML = '';
    }
  }

  // Luego colocar las reinas actuales
  for (let fila = 0; fila < n; fila++) {
    const col = tableroArray[fila];
    if (col === -1) continue; // Celda vacía, saltar

    const celda = document.getElementById(`${prefijo}-${fila}-${col}`);
    if (!celda) continue;

    celda.classList.add('reina');

    // Insertar el símbolo de la reina como elemento span
    const span = document.createElement('span');
    span.className = 'reina-simbolo';
    span.textContent = '♛';
    celda.appendChild(span);
  }
}

// ─────────────────────────────────────────────
//  MOSTRAR ARREGLO DE ÍNDICES
// ─────────────────────────────────────────────

/**
 * mostrarIndices(solucion)
 *
 * Muestra visualmente el arreglo de índices de la solución actual.
 * Ejemplo: [0, 4, 7, 5, 2, 6, 1, 3]
 * → Fila 0: columna 0, Fila 1: columna 4, etc.
 *
 * @param {number[]} solucion - Array de columnas de la solución
 */
function mostrarIndices(solucion) {
  // Hacer visible la sección
  elIndicesSection.classList.remove('hidden');

  // Limpiar contenido previo
  elIndicesDisplay.innerHTML = '';

  // Crear un badge por cada posición
  solucion.forEach((columna, fila) => {
    const badge = document.createElement('div');
    badge.className = 'indice-badge';
    badge.textContent = `F${fila}: C${columna}`; // Fila N → Columna M
    elIndicesDisplay.appendChild(badge);
  });
}

// ─────────────────────────────────────────────
//  ACTUALIZAR INFO DE SOLUCIONES
// ─────────────────────────────────────────────

/**
 * actualizarInfoSoluciones()
 *
 * Muestra "Solución #X de Y" en el badge de información.
 */
function actualizarInfoSoluciones() {
  const total = estado.soluciones.length;
  const actual = estado.indiceSolucion + 1;

  elInfoSoluciones.textContent = `Solución #${actual} de ${total}`;
  elInfoSoluciones.classList.remove('hidden');
}

// ─────────────────────────────────────────────
//  ANIMACIÓN DEL PROCESO (BACKTRACKING)
// ─────────────────────────────────────────────

/**
 * animarPasos(pasos, n, callback)
 *
 * Reproduce los pasos del backtracking paso a paso con un delay
 * entre cada uno, para que el usuario pueda ver el proceso.
 *
 * @param {number[][]} pasos    - Lista de estados del tablero en cada paso
 * @param {number}     n        - Tamaño del tablero
 * @param {Function}   callback - Se llama cuando la animación termina
 */
function animarPasos(pasos, n, callback) {
  // Limitamos la cantidad de pasos animados para evitar esperas largas
  // En N=8 hay miles de pasos; mostramos como máximo 300
  const MAX_PASOS_ANIMADOS = 300;
  const pasosAMostrar = pasos.length > MAX_PASOS_ANIMADOS
    ? pasos.filter((_, i) => i % Math.ceil(pasos.length / MAX_PASOS_ANIMADOS) === 0)
    : pasos;

  let i = 0; // Índice del paso actual

  function siguientePaso() {
    if (i >= pasosAMostrar.length) {
      // Animación terminada
      estado.animando = false;
      if (callback) callback();
      return;
    }

    // Dibujar el estado actual en el tablero de "Proceso"
    dibujarReinas('tableroProceso', pasosAMostrar[i], n);
    i++;

    // Programar el siguiente paso con un pequeño delay (60ms)
    estado.animacionId = setTimeout(siguientePaso, 60);
  }

  siguientePaso(); // Arrancar la animación
}

// ─────────────────────────────────────────────
//  MOSTRAR SOLUCIÓN ACTUAL
// ─────────────────────────────────────────────

/**
 * mostrarSolucionActual()
 *
 * Dibuja la solución actual en el tablero "Solución" y actualiza
 * el arreglo de índices y el badge de información.
 */
function mostrarSolucionActual() {
  const solucion = estado.soluciones[estado.indiceSolucion];
  const n = estado.n;

  // Dibujar en tablero de solución
  dibujarReinas('tableroSolucion', solucion, n);

  // También en tablero de proceso (para que coincidan al terminar la animación)
  dibujarReinas('tableroProceso', solucion, n);

  // Mostrar índices
  mostrarIndices(solucion);

  // Actualizar badge "Solución #X de Y"
  actualizarInfoSoluciones();
}

// ─────────────────────────────────────────────
//  FUNCIÓN PRINCIPAL: RESOLVER
// ─────────────────────────────────────────────

/**
 * resolverJuego()
 *
 * Se activa al pulsar el botón "▶ Resolver".
 * 1. Lee el valor N del input
 * 2. Ejecuta el algoritmo de backtracking
 * 3. Crea los tableros vacíos
 * 4. Anima el proceso
 * 5. Muestra la primera solución al terminar
 */
function resolverJuego() {
  // Leer y validar N
  const n = parseInt(elInputN.value, 10);

  if (isNaN(n) || n < 8) {
    alert('⚠ El valor mínimo de N es 8.');
    elInputN.value = 8;
    return;
  }

  if (n > 14) {
    alert('⚠ Para evitar bloqueos en el navegador, el máximo permitido es 14.');
    elInputN.value = 14;
    return;
  }

  // Cancelar animación previa si hay alguna en curso
  if (estado.animacionId) clearTimeout(estado.animacionId);

  // Actualizar estado
  estado.n              = n;
  estado.indiceSolucion = 0;
  estado.animando       = true;

  // Deshabilitar controles durante el proceso
  elBtnResolver.disabled  = true;
  elBtnSiguiente.disabled = true;

  // ── EJECUTAR EL ALGORITMO ──────────────────────
  // encontrarSoluciones() está en NueveReinas.js
  const resultado = encontrarSoluciones(n);
  estado.soluciones = resultado.soluciones;
  estado.pasos      = resultado.pasos;

  // ── CREAR TABLEROS VACÍOS ──────────────────────
  crearTablero(elTableroProceso, n);
  crearTablero(elTableroSolucion, n);

  // Mostrar solución final ya en el tablero de la derecha
  dibujarReinas('tableroSolucion', estado.soluciones[0], n);
  mostrarIndices(estado.soluciones[0]);
  actualizarInfoSoluciones();

  // ── ANIMAR EL PROCESO ──────────────────────────
  animarPasos(estado.pasos, n, () => {
    // Callback: al terminar la animación, mostrar la solución #1
    mostrarSolucionActual();

    // Rehabilitar botones
    elBtnResolver.disabled  = false;
    elBtnSiguiente.disabled = estado.soluciones.length <= 1;
  });
}

// ─────────────────────────────────────────────
//  NAVEGAR A LA SIGUIENTE SOLUCIÓN
// ─────────────────────────────────────────────

/**
 * siguienteSolucion()
 *
 * Avanza al siguiente índice de solución (en ciclo).
 * Si llegamos al final, volvemos al principio.
 */
function siguienteSolucion() {
  if (estado.soluciones.length === 0) return;

  // Avanzar en ciclo
  estado.indiceSolucion = (estado.indiceSolucion + 1) % estado.soluciones.length;

  // Mostrar la nueva solución
  mostrarSolucionActual();
}

// ─────────────────────────────────────────────
//  REINICIAR EL JUEGO
// ─────────────────────────────────────────────

/**
 * resetJuego()
 *
 * Cancela cualquier animación en curso y vuelve al estado inicial.
 */
function resetJuego() {
  // Cancelar animación
  if (estado.animacionId) clearTimeout(estado.animacionId);

  // Restaurar estado
  estado.soluciones      = [];
  estado.pasos           = [];
  estado.indiceSolucion  = 0;
  estado.animando        = false;

  // Limpiar tableros
  elTableroProceso.innerHTML  = '';
  elTableroSolucion.innerHTML = '';

  // Ocultar secciones opcionales
  elInfoSoluciones.classList.add('hidden');
  elIndicesSection.classList.add('hidden');

  // Rehabilitar / deshabilitar botones
  elBtnResolver.disabled  = false;
  elBtnSiguiente.disabled = true;

  // Restaurar valor por defecto del input
  elInputN.value = 8;
}

// ─────────────────────────────────────────────
//  INICIALIZACIÓN AL CARGAR LA PÁGINA
// ─────────────────────────────────────────────

/**
 * Al cargar la página, creamos tableros vacíos de 8×8 para que
 * el usuario vea la cuadrícula antes de pulsar "Resolver".
 */
(function init() {
  crearTablero(elTableroProceso, 8);
  crearTablero(elTableroSolucion, 8);
})();
