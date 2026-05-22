# 🔥💧🌱🌪️ Avatar — 

**Escuadrón Lobo · Algoritmos & JavaScript**

---

## ¿De qué trata el juego?

Es un juego de batalla por turnos basado en **La Leyenda de Aang: El Avatar**

El jugador elige un personaje (Zuko, Katara, Aang o Toph) y se enfrenta a un oponente elegido automáticamente por la CPU. En cada turno se elige un ataque; el que tenga mayor poder gana el turno y el rival pierde una vida. Gana quien deje al otro sin vidas.

---

## Estructura del proyecto

```
AvatarJuego/
├── index.html       → Estructura HTML completa del juego
├── styles.css       → Estilos visuales (tema /cómic)
├── logo_lobo.png    → Logo del Escuadrón Lobo
└── js/
    └── avatar.js    → Lógica del juego en JavaScript
```

---

## Cómo ejecutar

1. Descomprimir el archivo `AvatarJuego.zip`
2. Abrir la carpeta `AvatarJuego/`
3. Hacer doble clic en `index.html`
4. Se abre directamente en el navegador (Chrome, Firefox, Edge)

> No requiere instalación ni servidor.

---

## Flujo del juego

```
Inicio
  ↓
Seleccionar personaje (radio buttons)
  ↓
Pulsar "Seleccionar"
  ↓
La CPU elige oponente al azar
  ↓
Elegir ataque (Fuego / Agua / Tierra / Aire)
  ↓
Se comparan poderes → se actualiza vidas
  ↓
¿Alguno llegó a 0 vidas?
  ├─ No → volver a elegir ataque
  └─ Sí → mostrar resultado + botón Reiniciar
```

---

## Descripción de archivos

### `index.html`
- `<section id="seleccionar-personaje">` — tarjetas con radio buttons
- `<section id="seleccionar-ataque">` — barra de vidas + botones de ataque
- `<section id="mensajes">` — párrafo dinámico modificado por JS
- `<section id="resultado-final">` — resultado final (oculto al inicio)
- `<section id="reiniciar">` — botón de reinicio (oculto al inicio)

### `styles.css`
- Variables CSS (colores, fuentes, sombras de cómic)
- Diseño tipo cómic con fuente **Bangers** + **Nunito**
- Animaciones CSS: entrada del título, rebote, sacudida
- Responsive para móviles (grid de 2 columnas en pantallas pequeñas)

### `js/avatar.js`
| Función | Qué hace |
|---|---|
| `seleccionarPersonajeJugador()` | Lee el radio checked y guarda el personaje en el estado |
| `seleccionarOponenteAleatorio(excluir)` | Elige un personaje distinto al del jugador usando `Math.random()` |
| `ejecutarAtaque(idAtaque)` | Compara poderes y actualiza vidas y mensajes |
| `ataqueOponenteAleatorio()` | La CPU elige ataque al azar |
| `actualizarVidasDOM()` | Sincroniza los `<span>` de vidas con el estado |
| `generarCorazones(actuales, max)` | Genera el string de ❤️/💔 para las vidas |
| `sacudirElemento(el)` | Aplica animación CSS de sacudida |
| `verificarFinJuego()` | Detecta si alguien llegó a 0 vidas |
| `reiniciarJuego()` | Resetea estado y DOM sin recargar la página |

---

## Conceptos JavaScript utilizados

| Concepto | Dónde se usa |
|---|---|
| `document.getElementById()` | Obtener referencias a elementos del DOM |
| `querySelectorAll()` | Obtener todos los radio buttons |
| `addEventListener('click', fn)` | Escuchar clics en botones |
| `Math.random()` + `Math.floor()` | Selección aleatoria de personaje/ataque |
| `Object.keys()` + `.filter()` | Filtrar personajes disponibles |
| `Array.find()` | Buscar un ataque por su id |
| `classList.add/remove()` | Mostrar y ocultar secciones |
| `innerHTML` | Escribir HTML dinámico en mensajes |
| `forEach()` | Registrar eventos en múltiples botones |
| Objetos y arrays | Almacenar datos de personajes y ataques |

---

## Requisitos

- Navegador moderno con JavaScript habilitado
- Sin dependencias ni librerías externas
