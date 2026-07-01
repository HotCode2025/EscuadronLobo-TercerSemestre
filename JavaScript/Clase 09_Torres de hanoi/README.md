# 🗼 Torres de Hanoi

## 📌 Consigna

El algoritmo de las Torres de Hanoi tiene sus orígenes en la cultura oriental y en una leyenda sobre el templo de Brahma, cuya estructura simulaba una plataforma metálica con tres varillas y discos en su interior.

Este algoritmo utiliza la técnica de **Recursividad**, donde la solución del problema depende de resolver versiones más pequeñas del mismo problema.

---

## 🎯 Objetivo

Dados `n` discos ubicados en la varilla inicial **A**, el objetivo es trasladar todos los discos a la varilla destino **C**, respetando el orden original:

```text
Disco más grande → abajo
Disco más pequeño → arriba
```

La varilla **B** se utiliza como auxiliar durante el proceso.

---

## 📋 Condiciones del Juego

* Solo se puede mover **un disco a la vez**.
* Solo se puede mover el disco que está en la **parte superior** de una varilla.
* **No se puede colocar un disco más grande sobre uno más pequeño**.

---

## 🔄 Algoritmo Recursivo

El problema se resuelve en tres pasos:

1. Mover los `n-1` discos superiores de **A** → **B** (usando C como auxiliar).
2. Mover el disco más grande de **A** → **C**.
3. Mover los `n-1` discos de **B** → **C** (usando A como auxiliar).

```text
hanoi(n, origen, destino, auxiliar)
```

---

## ✅ Condición de Éxito

El problema se considera resuelto cuando los `n` discos se encuentran en la varilla **C** en el mismo orden que estaban en **A**.

La cantidad mínima de movimientos necesarios para `n` discos es:

```text
2ⁿ - 1
```

Por ejemplo, con 3 discos:

```text
2³ - 1 = 7 movimientos
```
