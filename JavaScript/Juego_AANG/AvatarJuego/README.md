# ⚔️ LOS ELEMENTOS — La Leyenda de Aang

**Escuadrón Lobo · JavaScript + HTML + CSS**

---

## Descripción del juego

**LOS ELEMENTOS** es un juego de batalla por turnos basado en *La Leyenda de Aang*.
El jugador elige a uno de los cuatro guerreros elementales y se enfrenta a un oponente
controlado por la CPU. Cada turno se elige un ataque; el de mayor poder gana el turno
y el rival pierde una vida. Gana quien deje al otro sin vidas.

---

## Personajes jugables

| Personaje | Elemento | Poder | Velocidad | Imagen |
|-----------|----------|-------|-----------|--------|
| **Aang**  | 🌪️ Aire  | 3 | 5 | `AANG.png` |
| **Katara**| 💧 Agua  | 3 | 4 | `KATARA.png` |
| **Zuko**  | 🔥 Fuego | 4 | 3 | `ZUKO.png` |
| **Toph**  | 🌱 Tierra| 2 | 5 | `TOPH.png` |

Cada personaje tiene **3 expresiones** únicas que aparecen en el bocadillo según el resultado del turno:
- `gana` → cuando el jugador vence el turno
- `pierde` → cuando el jugador pierde el turno
- `empata` → cuando hay empate de poder

---

## Estructura del proyecto

```
LosElementos/
├── index.html            → Estructura HTML completa (5 secciones)
├── styles.css            → Estilos: tema videojuego anime oscuro + VR
├── js/
│   └── avatar.js         → Lógica del juego en JavaScript
├── AANG.png              → Imagen individual de Aang
├── KATARA.png            → Imagen individual de Katara
├── ZUKO.png              → Imagen individual de Zuko
├── TOPH.png              → Imagen individual de Toph
├── Logo_del_AVATAR.png   → Arte del grupo (banner y fondo)
└── logo_lobo.png         → Logo del Escuadrón Lobo
```

---

## Cómo ejecutar

1. Descomprimir `LosElementos.zip`
2. Abrir la carpeta `LosElementos/`
3. Doble clic en `index.html`
4. Se abre en el navegador — no requiere instalación

---

## Flujo del juego

```
Inicio → Elegir personaje (radio buttons)
  ↓
Pulsar "¡ENTRAR AL COMBATE!"
  ↓
CPU elige oponente al azar
  ↓
Elegir ataque (Fuego / Agua / Tierra / Aire)
  ↓
Comparar poderes → descontar vida al perdedor
  ↓
Mostrar expresión del personaje en el bocadillo
  ↓
¿Alguien llegó a 0 vidas?
  ├─ No → siguiente turno (ronda++)
  └─ Sí → mostrar resultado final + botón Reiniciar
```

---

## Ataques y poderes

| Ataque | Emoji | Poder |
|--------|-------|-------|
| Fuego  | 🔥    | 4     |
| Agua   | 💧    | 3     |
| Aire   | 🌪️   | 3     |
| Tierra | 🌱    | 2     |

La CPU elige su ataque con `Math.random()` cada turno.
Si los poderes son iguales → empate (nadie pierde vida).

---

## Diseño Visual

- **Fondo**: grilla de videojuego + imagen del grupo difuminada como fondo ambiental
- **Tarjetas de personaje**: imágenes PNG reales con `mix-blend-mode: multiply` para eliminar el fondo blanco
- **HUD de batalla**: barras de vida (verde/rojo), nombres, imágenes reales de los personajes
- **Bocadillo de mensajes**: texto dinámico con expresiones únicas por personaje y resultado
- **Efectos VR**: scanlines, marco neón, brillo por elemento, animaciones CSS

---

## Conceptos JavaScript utilizados

| Concepto | Uso |
|---|---|
| Objetos con propiedades anidadas | `PERSONAJES` con `expresiones: { gana, pierde, empata }` |
| Array con `find()` | Buscar ataque por id |
| `querySelectorAll` + `forEach` | Leer radio buttons |
| `Math.random()` + `Math.floor()` | Oponente y ataque aleatorios |
| `classList.add/remove` | Mostrar/ocultar secciones |
| `innerHTML` | Mensajes dinámicos con HTML |
| `style.width` | Actualizar barras de HP |
| `addEventListener` | Eventos de clic en botones |
| Estado global (`estado`) | Centralizar variables del juego |

---

## Requisitos

- Navegador moderno (Chrome 80+, Firefox 75+, Edge 80+)
- JavaScript habilitado — sin dependencias externas
