/**
 * ============================================================
 *  PROBLEMA DE LAS N REINAS — Lógica principal
 *  NueveReinas.js
 * ============================================================
 *
 *  El problema consiste en colocar N reinas en un tablero de
 *  ajedrez de N×N de forma que ninguna reina ataque a otra.
 *  Una reina ataca en la misma fila, columna o diagonal.
 *
 *  Algoritmo: Backtracking (retroceso)
 *  - Se intenta colocar una reina en cada fila.
 *  - Para cada columna de esa fila, se verifica si la posición
 *    es segura (no hay conflictos con reinas ya colocadas).
 *  - Si es segura, se coloca y se pasa a la siguiente fila.
 *  - Si ninguna columna es válida, se retrocede (backtrack).
 * ============================================================
 */

// ─────────────────────────────────────────────
//  1. VERIFICAR POSICIÓN SEGURA
// ─────────────────────────────────────────────

/**
 * isSafe(tablero, fila, columna, n)
 *
 * Verifica si colocar una reina en [fila][columna] es seguro.
 * Solo revisamos hacia ARRIBA porque las filas inferiores aún
 * no tienen reinas colocadas.
 *
 * @param {number[]} tablero  - Array donde tablero[i] = columna de la reina en fila i
 * @param {number}   fila     - Fila donde queremos colocar la nueva reina
 * @param {number}   columna  - Columna candidata para la nueva reina
 * @param {number}   n        - Tamaño del tablero (N×N)
 * @returns {boolean}         - true si la posición es segura
 */
function isSafe(tablero, fila, columna, n) {
  for (let filaAnterior = 0; filaAnterior < fila; filaAnterior++) {
    const columnaAnterior = tablero[filaAnterior];

    // ¿Misma columna?
    if (columnaAnterior === columna) return false;

    // ¿Misma diagonal? La diferencia de filas == diferencia de columnas
    if (Math.abs(filaAnterior - fila) === Math.abs(columnaAnterior - columna)) return false;
  }
  return true; // Ningún conflicto encontrado → posición segura
}

// ─────────────────────────────────────────────
//  2. ALGORITMO DE BACKTRACKING
// ─────────────────────────────────────────────

/**
 * resolver(tablero, fila, n, soluciones, pasos)
 *
 * Función recursiva que intenta colocar reinas fila por fila.
 * Cuando todas las N reinas están colocadas, guarda la solución.
 *
 * @param {number[]}   tablero   - Estado actual del tablero
 * @param {number}     fila      - Fila actual que intentamos llenar
 * @param {number}     n         - Tamaño del tablero
 * @param {number[][]} soluciones - Acumula todas las soluciones encontradas
 * @param {number[][]} pasos      - Registra cada intento (para animación)
 */
function resolver(tablero, fila, n, soluciones, pasos) {
  // CASO BASE: todas las filas fueron llenadas → solución encontrada
  if (fila === n) {
    soluciones.push([...tablero]); // Guardamos una copia de la solución
    return;
  }

  // CASO RECURSIVO: probamos cada columna en la fila actual
  for (let columna = 0; columna < n; columna++) {
    if (isSafe(tablero, fila, columna, n)) {
      tablero[fila] = columna;           // Colocamos la reina
      pasos.push([...tablero]);          // Registramos el paso para animación

      resolver(tablero, fila + 1, n, soluciones, pasos); // Recursión siguiente fila

      tablero[fila] = -1;               // BACKTRACK: quitamos la reina
    }
  }
}

// ─────────────────────────────────────────────
//  3. FUNCIÓN PRINCIPAL: ENCONTRAR SOLUCIONES
// ─────────────────────────────────────────────

/**
 * encontrarSoluciones(n)
 *
 * Inicializa el tablero y arranca el backtracking.
 *
 * @param {number} n - Tamaño del tablero (mínimo 8)
 * @returns {{ soluciones: number[][], pasos: number[][] }}
 */
function encontrarSoluciones(n) {
  const tablero = new Array(n).fill(-1); // -1 = sin reina en esa fila
  const soluciones = [];
  const pasos = [];

  resolver(tablero, 0, n, soluciones, pasos);

  return { soluciones, pasos };
}

// ─────────────────────────────────────────────
//  4. EXPORTAR PARA USO EN EL NAVEGADOR
// ─────────────────────────────────────────────

// Estas funciones se usan desde index.html a través de la etiqueta <script>
// No se requiere módulo ES6; todo queda en el scope global del navegador.
