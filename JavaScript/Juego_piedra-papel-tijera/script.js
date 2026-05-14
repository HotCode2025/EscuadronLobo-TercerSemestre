/* ╔══════════════════════════════════════════════════════════════════════╗
  ║  script.js — Piedra · Papel · Tijera                                ║
  ║  Contiene toda la lógica del juego: reglas, cálculos y              ║
  ║  actualizaciones dinámicas de la interfaz (DOM).                    ║
   ╚══════════════════════════════════════════════════════════════════════╝ */


/* ════════════════════════════════════════════════════════════════════════
  CONSTANTES DEL JUEGO
  Se usan const porque estos valores nunca cambian durante la partida.
  Los objetos {} permiten acceder al valor usando la clave numérica (1, 2 o 3).
   ════════════════════════════════════════════════════════════════════════ */

/* Misma convención del código original: 1=Piedra, 2=Papel, 3=Tijera    */
const NAMES  = { 1: 'Piedra', 2: 'Papel', 3: 'Tijera' };
const EMOJIS = { 1: '🪨',     2: '📄',    3: '✂️'     };

/*
 * Tabla de victoria: VENCE[X] = Y significa "X le gana a Y"
 *   Piedra (1) vence a Tijera  (3)
 *   Papel  (2) vence a Piedra  (1)
 *   Tijera (3) vence a Papel   (2)
 * Esta estructura reemplaza los múltiples if/else del código original.
 */
const VENCE = { 1: 3, 2: 1, 3: 2 };

/* Frases aleatorias según el resultado (varían en cada ronda)           */
const FRASES = {
  win:  [
    '¡Sos una estrella! ⭐',
    '¡Jugada perfecta! 💪',
    'La compu no te pudo parar 🚀',
    '¡Mente maestra! 🧠',
    '¡Campeón del universo! 🏆',
  ],
  lose: [
    '¡La revancha es tuya! 🔥',
    'La compu te leyó la mente 🤖',
    '¡Seguí intentando, campeón! 💪',
    'Nadie dijo que sería fácil 😅',
    '¡La próxima es tuya! ⚡',
  ],
  draw: [
    '¡Igualados! Mente vs Máquina ⚡',
    '¡Coincidencia perfecta! 🎯',
    'Ninguno puede con el otro 🤝',
    '¡Dos cerebros iguales! 🧠🧠',
  ],
};


/* ════════════════════════════════════════════════════════════════════════
  ESTADO DEL JUEGO
  Objeto que almacena todos los datos de la partida actual.
  Se usa let porque estos valores sí cambian durante el juego.
   ════════════════════════════════════════════════════════════════════════ */
let state = {
  wins:    0,   /* Victorias acumuladas                                   */
  draws:   0,   /* Empates acumulados                                     */
  loses:   0,   /* Derrotas acumuladas                                    */
  round:   0,   /* Número de ronda actual                                 */
  history: [],  /* Array (lista) con el registro de cada ronda jugada     */
};


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN: numeroAleatorio(min, max)
  ════════════════════════════════════════════════════════════════════════
  Genera un entero al azar entre min y max (inclusive ambos).
  Esta es exactamente la misma función del código original.

  Cómo funciona paso a paso:
    Math.random()        → decimal entre 0.000 y 0.999
     * (max - min + 1)    → escala al rango deseado
    + min                → desplaza para que empiece en min
    Math.floor(...)      → redondea hacia abajo → entero final

  Ejemplo con min=1, max=3:
     Math.random() = 0.7 → 0.7 * 3 = 2.1 + 1 = 3.1 → floor → 3
*/
function numeroAleatorio(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN PRINCIPAL: play(jugador)
  ════════════════════════════════════════════════════════════════════════
  Se ejecuta cuando el usuario hace click en Piedra, Papel o Tijera.
  Parámetro:
    jugador → número 1, 2 o 3 enviado por el onclick del botón HTML

  Proceso completo:
    1. La PC genera su elección al azar (igual que en el código original)
    2. Se compara con la del jugador para determinar el resultado
    3. Se actualiza el estado (state)
    4. Se actualizan todas las partes visuales de la interfaz
*/
function play(jugador) {

  /* La PC elige al azar entre 1, 2 y 3 (misma lógica del original)     */
  const pc = numeroAleatorio(1, 3);

  /* Suma 1 al contador de rondas                                        */
  state.round++;

  /* ── LÓGICA DE COMBATE ───────────────────────────────────────────────
    Reemplaza los alert() del código original con una variable resultado.
    Mismas reglas: piedra gana tijera, papel gana piedra, tijera gana papel.
     ── */
  let resultado; /* Guardará 'win', 'draw' o 'lose'                       */

  if (jugador === pc) {
    /* Ambos eligieron lo mismo → empate                                  */
    resultado = 'draw';
    state.draws++;

  } else if (VENCE[jugador] === pc) {
    /*
     * VENCE[jugador] devuelve a quién derrota el jugador.
     * Si ese valor coincide con la elección de la PC, el jugador ganó.
     * Ejemplo: jugador=1 (Piedra), VENCE[1]=3 (Tijera), pc=3 → ¡ganó!
     */
    resultado = 'win';
    state.wins++;

  } else {
    /* En cualquier otro caso, la PC gana                                 */
    resultado = 'lose';
    state.loses++;
  }

  /*
   * Guarda la ronda al inicio del array (más reciente primero).
   * unshift() agrega al principio, a diferencia de push() que agrega al final.
   * Se guarda un objeto con todos los datos de la ronda.
   */
  state.history.unshift({ jugador, pc, resultado, round: state.round });

  /* Actualiza cada parte de la interfaz visual                          */
  updateArena(jugador, pc, resultado);   /* Emojis y mensaje de resultado  */
  updateScoreboard(resultado);           /* Marcador de puntos             */
  updateHistory();                       /* Lista de rondas jugadas        */

  /* Lanza confeti solo si el jugador ganó esta ronda                    */
  if (resultado === 'win') launchConfetti();
}


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN: updateArena(jugador, pc, resultado)
  ════════════════════════════════════════════════════════════════════════
  Actualiza la zona central de combate:
    - Muestra los emojis de lo que eligió cada uno
    - Activa la animación de sacudida en los emojis
    - Muestra el texto del resultado con su color
    - Muestra una frase aleatoria según el resultado
*/
function updateArena(jugador, pc, resultado) {

  /* Obtiene referencias a los elementos HTML usando su id               */
  const arena        = document.getElementById('arena');
  const playerEmoji  = document.getElementById('player-emoji');
  const pcEmoji      = document.getElementById('pc-emoji');
  const resultText   = document.getElementById('result-text');
  const resultDetail = document.getElementById('result-detail');

  /* Actualiza el emoji y la etiqueta de texto de cada jugador           */
  playerEmoji.textContent = EMOJIS[jugador];
  pcEmoji.textContent     = EMOJIS[pc];
  document.getElementById('player-label').textContent = NAMES[jugador];
  document.getElementById('pc-label').textContent     = NAMES[pc];

  /* ── TRUCO PARA REINICIAR ANIMACIÓN CSS ──────────────────────────────
    Si la clase ya existe, la animación no se reinicia sola.
    Solución en 3 pasos:
      1. Quitar la clase "shake"
      2. Leer offsetWidth (fuerza al navegador a actualizar el DOM)
      3. Agregar la clase "shake" de nuevo → la animación reinicia
     ── */
  playerEmoji.classList.remove('shake');
  pcEmoji.classList.remove('shake');
  void playerEmoji.offsetWidth; /* Fuerza reflow del navegador             */
  playerEmoji.classList.add('shake');
  pcEmoji.classList.add('shake');

  /* Configuración visual para cada tipo de resultado                    */
  const cfg = {
    win:  { text: '🏆 ¡GANASTE!',  cls: 'win',  arenaCls: 'result-win'  },
    lose: { text: '💀 ¡PERDISTE!', cls: 'lose', arenaCls: 'result-lose' },
    draw: { text: '🤝 ¡EMPATE!',   cls: 'draw', arenaCls: 'result-draw' },
  };

  /* Limpia clases de resultado anteriores y aplica la nueva             */
  arena.classList.remove('result-win', 'result-lose', 'result-draw');
  arena.classList.add(cfg[resultado].arenaCls);

  /* Actualiza el texto grande y su clase CSS (que define el color)      */
  resultText.textContent = cfg[resultado].text;
  resultText.className   = 'result-text ' + cfg[resultado].cls;

  /* Elige una frase aleatoria del array correspondiente al resultado    */
  const pool = FRASES[resultado];
  resultDetail.textContent = pool[Math.floor(Math.random() * pool.length)];
}


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN: updateScoreboard(resultado)
  ════════════════════════════════════════════════════════════════════════
  Actualiza el número del marcador que corresponde al resultado y
  dispara la animación de "bump" (rebote) para llamar la atención.
*/
function updateScoreboard(resultado) {

  /* Mapea el resultado ('win','draw','lose') al id del span en HTML     */
  const map = { win: 'wins', draw: 'draws', lose: 'loses' };

  /* Busca el elemento por id (ej: "score-wins")                         */
  const el = document.getElementById('score-' + map[resultado]);

  /* Muestra el nuevo valor del estado                                   */
  el.textContent = state[map[resultado]];

  /* Reinicia y dispara la animación de rebote                           */
  el.classList.remove('bump');
  void el.offsetWidth;       /* Fuerza reflow para que la animación reinicie */
  el.classList.add('bump');
}


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN: updateHistory()
  ════════════════════════════════════════════════════════════════════════
  Renderiza el historial de rondas en la sección correspondiente.
  Usa template literals (backtick ``) para construir HTML dinámico.
*/
function updateHistory() {

  const section = document.getElementById('history-section');
  const list    = document.getElementById('history-list');

  /* Muestra la sección (estaba oculta con display:none al inicio)       */
  section.style.display = 'block';

  /* Etiquetas para los badges de cada tipo de resultado                 */
  const labels = { win: '✅ Victoria', lose: '❌ Derrota', draw: '🤝 Empate' };

  /*
   * Genera el HTML del historial:
   *   .map()    → transforma cada objeto de ronda en un string HTML
   *   .join('') → une los strings sin separadores entre ellos
   *   innerHTML → inserta el HTML generado dentro del div#history-list
   */
  list.innerHTML = state.history.map(h => `
    <div class="history-item ${h.resultado}">
      <span class="round">Ronda ${h.round}</span>
      <span class="match">
        ${EMOJIS[h.jugador]} ${NAMES[h.jugador]}
        &nbsp;vs&nbsp;
        ${EMOJIS[h.pc]} ${NAMES[h.pc]}
      </span>
      <span class="badge">${labels[h.resultado]}</span>
    </div>
  `).join('');
}


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN: resetGame()
  ════════════════════════════════════════════════════════════════════════
  Reinicia el juego completamente al estado inicial:
    - Borra todos los puntajes y el historial
    - Vuelve la arena a su apariencia de inicio
    - Oculta la sección del historial
*/
function resetGame() {

  /* Reemplaza el estado con un objeto nuevo en cero                     */
  state = { wins: 0, draws: 0, loses: 0, round: 0, history: [] };

  /* Pone los tres contadores del marcador en "0"                        */
  ['wins', 'draws', 'loses'].forEach(clave =>
    document.getElementById('score-' + clave).textContent = '0'
  );

  /* Restaura la arena al estado inicial                                 */
  const arena = document.getElementById('arena');
  arena.classList.remove('result-win', 'result-lose', 'result-draw');

  document.getElementById('player-emoji').textContent  = '🤜';
  document.getElementById('pc-emoji').textContent      = '🤛';
  document.getElementById('player-label').textContent  = '—';
  document.getElementById('pc-label').textContent      = '—';
  document.getElementById('result-text').textContent   = '¡Elegí tu jugada!';
  document.getElementById('result-text').className     = 'result-text'; /* Sin color */
  document.getElementById('result-detail').textContent = '¡La batalla comienza ahora! 🎮';

  /* Oculta y vacía el historial                                         */
  document.getElementById('history-section').style.display = 'none';
  document.getElementById('history-list').innerHTML = '';
}


/* ════════════════════════════════════════════════════════════════════════
  FUNCIÓN: launchConfetti()
  ════════════════════════════════════════════════════════════════════════
  Crea 30 piezas de confeti animadas que caen desde arriba al ganar.
  Cada pieza es un div creado con JS y eliminado automáticamente
  después de su animación (para no acumular elementos en el DOM).
*/
function launchConfetti() {

  /* Colores vivos y divertidos para el confeti                          */
  const colors = ['#E17055','#0984E3','#00B894','#F39C12','#6C5CE7','#fd79a8','#fdcb6e'];

  /* Crea 30 piezas con retraso escalonado de 30ms entre cada una        */
  for (let i = 0; i < 30; i++) {

    /*
     * setTimeout(función, ms) ejecuta la función después de X milisegundos.
     * i * 30 ms → efecto de "lluvia" escalonada: no caen todas juntas.
     */
    setTimeout(() => {

      /* Crea un nuevo div en memoria                                     */
      const pieza = document.createElement('div');
      pieza.className = 'confetti-piece';

      /* Posición y estilo aleatorio para cada pieza                      */
      pieza.style.cssText = `
        left: ${15 + Math.random() * 70}%;
        top: 20%;
        background: ${colors[i % colors.length]};
        transform: rotate(${Math.random() * 360}deg);
        animation-delay:    ${Math.random() * 0.4}s;
        animation-duration: ${0.8 + Math.random() * 0.8}s;
      `;

      /* Agrega la pieza al body para que sea visible en pantalla         */
      document.body.appendChild(pieza);

      /* La elimina 1700ms después, cuando ya cayó y desapareció          */
      setTimeout(() => pieza.remove(), 1700);

    }, i * 30); /* Retraso escalonado de 30ms por pieza                  */
  }
}
