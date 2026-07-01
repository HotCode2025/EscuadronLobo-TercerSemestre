// Tamaño tablero
const N = 8;

// Movimientos del caballo
const movX = [2, 1, -1, -2, -2, -1, 1, 2];
const movY = [1, 2, 2, 1, -1, -2, -2, -1];

// Matriz tablero
let tablero;

// Guardar recorrido
let recorrido = [];

// Crear tablero vacío
function crearTablero() {
    tablero = Array.from({ length: N }, () => Array(N).fill(-1));
}

// Iniciar algoritmo
function iniciar() {
    reiniciar();
    tablero[0][0] = 0;
    recorrido = [];
    resolver(0, 0, 1);
    // Guardar posición inicial
    recorrido.unshift([0, 0]);
    // Animar recorrido
    animarRecorrido();
}

// Validar movimiento
function esValido(x, y) {
    return x >= 0 && y >= 0 && x < N && y < N && tablero[x][y] === -1;
}

// Backtracking
function resolver(x, y, salto) {
    // Caso base
    if (salto === N * N) {
      return true;
    }

    for (let i = 0; i < 8; i++) {
        let nuevoX = x + movX[i];
        let nuevoY = y + movY[i];
        if (esValido(nuevoX, nuevoY)) {
            tablero[nuevoX][nuevoY] = salto;
            recorrido.push([nuevoX, nuevoY]);
            if (resolver(nuevoX, nuevoY, salto + 1)) {
                return true;
            }
            // Backtracking
            tablero[nuevoX][nuevoY] = -1;
            recorrido.pop();
        }
    }
    return false;
}

// Dibujar tablero vacío
function dibujarTablero() {
    const tableroHTML = document.getElementById("tablero");
    tableroHTML.innerHTML = "";
    for (let fila = 0; fila < N; fila++) {
        for (let col = 0; col < N; col++) {
            const casilla = document.createElement("div");
            casilla.classList.add("casilla");
            casilla.id = `casilla-${fila}-${col}`;
            if ((fila + col) % 2 === 0) {
                casilla.classList.add("blanca");
            } else {
                casilla.classList.add("negra");
            }
            tableroHTML.appendChild(casilla);
        }
    }
}

// Animación recorrido
async function animarRecorrido() {
    for (let i = 0; i < recorrido.length; i++) {
        let [x, y] = recorrido[i];
        // Limpiar caballo anterior
        document.querySelectorAll(".caballo").forEach((c) => c.remove());
        // Casilla actual
        const casilla = document.getElementById(`casilla-${x}-${y}`);
        // Dejar número anterior
        if (i > 0) {
            let [prevX, prevY] = recorrido[i - 1];
            const anterior = document.getElementById(`casilla-${prevX}-${prevY}`);
            anterior.innerHTML = i - 1;
        }
        // Crear caballo
        const caballo = document.createElement("div");
        caballo.classList.add("caballo");
        caballo.innerHTML = "🐎";
        casilla.appendChild(caballo);
        // Mostrar movimiento
        mostrarMovimiento(i, x, y);
        // Espera animación
        await esperar(500);
    }
    // Último número
    let [ultimoX, ultimoY] = recorrido[recorrido.length - 1];
    const ultima = document.getElementById(`casilla-${ultimoX}-${ultimoY}`);
    ultima.innerHTML = recorrido.length - 1;
}

// Delay
function esperar(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}

// Reiniciar tablero
function reiniciar() {
    crearTablero();
    recorrido = [];
    dibujarTablero();
    document.getElementById("movimientos").innerHTML = "";
}

// Mostrar movimientos
function mostrarMovimiento(numero, x, y){
    const contenedor =
    document.getElementById("movimientos");
    const item =
    document.createElement("div");
    item.classList.add("movimiento");
    item.innerHTML =
    `<strong>${numero}</strong> → (${x}, ${y})`;
    contenedor.appendChild(item);
    
    // Auto scroll
    contenedor.scrollTop =
    contenedor.scrollHeight;
}

// Crear tablero al inicio
reiniciar();