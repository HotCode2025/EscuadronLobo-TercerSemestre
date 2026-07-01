# ♛ Problema de las N Reinas

## Descripción

El **Problema de las N Reinas** consiste en colocar **N reinas** en un tablero de ajedrez de **N×N** de tal forma que **ninguna reina pueda atacar a otra**.

Una reina en ajedrez puede atacar en cualquier dirección:
- Misma **fila**
- Misma **columna**
- Misma **diagonal**

Este proyecto implementa una solución en **JavaScript puro** usando el algoritmo de **Backtracking** (retroceso), con una interfaz visual interactiva en HTML y CSS.

---

## Estructura del Proyecto

```
NueveReinas/
└── juego/
    ├── index.html       → Estructura HTML de la aplicación
    ├── styles.css       → Estilos y diseño visual
    ├── NueveReinas.js   → Algoritmo de backtracking (lógica pura)
    └── app.js           → Interfaz de usuario y animación
```

---

## ¿Cómo ejecutar?

1. Abrir la carpeta `juego/` en un explorador de archivos.
2. Hacer doble clic en `index.html`.
3. Se abrirá directamente en el navegador (Chrome, Firefox, Edge).
4. No requiere servidor ni instalación adicional.

---

## ¿Cómo usar la aplicación?

| Paso | Acción |
|------|--------|
| 1 | Ingresar un valor de **N** (mínimo 8, máximo 14) |
| 2 | Pulsar **▶ Resolver** |
| 3 | Observar el **proceso** de backtracking en el tablero izquierdo |
| 4 | Ver la **solución final** en el tablero derecho |
| 5 | Usar **Siguiente solución →** para recorrer todas las soluciones |
| 6 | Pulsar **↺ Reiniciar** para empezar de nuevo |

---

## El Algoritmo: Backtracking

### Idea principal

Se intenta colocar una reina en cada fila, de arriba hacia abajo:

```
Fila 0 → intentar columnas 0, 1, 2, ... hasta encontrar una segura
Fila 1 → lo mismo, considerando la reina ya colocada en Fila 0
...
Fila N-1 → si se llega aquí con una reina colocada, ¡solución encontrada!
```

Si en alguna fila **no hay columna válida**, se retrocede (backtrack) a la fila anterior y se prueba la siguiente columna.

### Pseudocódigo

```
función resolver(fila):
  si fila == N:
    guardar solución
    retornar

  para columna desde 0 hasta N-1:
    si isSafe(fila, columna):
      tablero[fila] = columna      // colocar reina
      resolver(fila + 1)           // recursión
      tablero[fila] = -1           // quitar reina (backtrack)
```

### Verificación de seguridad

```
función isSafe(fila, columna):
  para cada filaAnterior de 0 a fila-1:
    si misma columna → NO es seguro
    si misma diagonal → NO es seguro
  retornar ES seguro
```

---

## Cantidad de soluciones por N

| N  | Soluciones |
|----|-----------|
| 8  | 92        |
| 9  | 352       |
| 10 | 724       |
| 12 | 14,200    |
| 14 | 365,596   |

---

## Archivos y su función

### `NueveReinas.js`
- `isSafe(tablero, fila, columna, n)` → verifica si una posición es válida
- `resolver(tablero, fila, n, soluciones, pasos)` → backtracking recursivo
- `encontrarSoluciones(n)` → inicializa y ejecuta el algoritmo

### `app.js`
- `crearTablero(contenedor, n)` → genera el grid HTML del tablero
- `dibujarReinas(prefijo, tableroArray, n)` → coloca los símbolos ♛ en el DOM
- `animarPasos(pasos, n, callback)` → reproduce el proceso paso a paso
- `mostrarIndices(solucion)` → muestra el arreglo [F0:C0, F1:C4, ...]
- `resolverJuego()` → función principal (botón Resolver)
- `siguienteSolucion()` → navega al siguiente resultado
- `resetJuego()` → reinicia la aplicación

### `index.html`
Estructura semántica con:
- Hero / encabezado
- Panel de controles (input + botones)
- Panel de índices
- Dos tableros (Proceso / Solución)
- Sección didáctica

### `styles.css`
- Variables CSS para theming consistente
- Tablero con alternancia clara/oscura
- Animaciones: aparición de reinas, pulso de conflicto
- Diseño responsive para móviles

---

## Requisitos técnicos

- Navegador moderno (Chrome 80+, Firefox 75+, Edge 80+)
- JavaScript habilitado
- Sin dependencias externas

---

## Autores

Actividad grupal — Algoritmos y Estructuras de Datos
