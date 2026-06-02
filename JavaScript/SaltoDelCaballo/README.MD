# 🐴 Problema del Salto del Caballo

## 📌 Consigna

El algoritmo de salto del caballo, también conocido como *tour del caballo*, busca encontrar una secuencia de movimientos de un caballo de ajedrez que visite cada casilla de un tablero exactamente una vez.

Este algoritmo utiliza la técnica de **Backtracking (vuelta atrás)**, lo que significa que si un camino no conduce a una solución válida, el algoritmo retrocede y prueba otro camino posible.

---

## 🎯 Objetivo

En un tablero de ajedrez de `8 x 8`, el caballo comienza en la posición inicial:

```text
(x = 0, y = 0)
```

El objetivo consiste en encontrar un recorrido válido para que el caballo pase exactamente una vez por cada una de las 64 casillas del tablero.

---

## ♞ Movimientos del Caballo

El caballo puede realizar hasta 8 movimientos posibles desde una casilla determinada.

Los desplazamientos válidos son:

```text
(2,1)
(1,2)
(-1,2)
(-2,1)
(-2,-1)
(-1,-2)
(1,-2)
(2,-1)
```

Por ejemplo:

Si el caballo está en la posición:

```text
(0,0)
```

Los posibles movimientos válidos serán aquellos que permanezcan dentro del tablero.

Otro ejemplo:

Si el caballo está en la posición:

```text
(3,5)
```

Los movimientos posibles serían:

```text
(5,6)
(4,7)
(2,7)
(1,6)
(1,4)
(2,3)
(4,3)
(5,4)
```

---

## ⚠️ Restricciones

Antes de realizar un movimiento se debe verificar que:

* La casilla de destino esté dentro del tablero.
* El caballo no haya pasado previamente por esa casilla.

Cada movimiento válido se registra guardando el número del salto realizado.

---

## 🔄 Backtracking

Si el caballo agota todos los movimientos posibles sin encontrar una solución:

1. El algoritmo vuelve al movimiento anterior.
2. Se elimina el movimiento realizado.
3. Se prueba otro camino diferente.

Este proceso se conoce como **vuelta atrás** o **Backtracking**.

---

## ✅ Condición de Éxito

El problema se considera resuelto cuando el caballo logra recorrer todas las casillas del tablero exactamente una vez.

En un tablero de `8 x 8`:

```text
8 x 8 = 64 casillas
```

Por lo tanto, el caballo debe realizar:

```text
63 saltos
```

para completar el recorrido total.
