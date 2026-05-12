# 🕐 Reloj Digital Interactivo

**Versión:** 1.0  
**Tecnologías:** HTML5 · CSS3 · JavaScript (Vanilla)  
**Autor:** Generado con asistencia de Claude (Anthropic)

---

## 📋 Descripción

Reloj digital en tiempo real desarrollado con HTML, CSS y JavaScript puro, sin dependencias externas ni frameworks. Muestra la hora actual con actualización cada segundo, soporte para múltiples zonas horarias internacionales y una estética profesional de panel de control.

---

## 📁 Estructura del proyecto

```
proyecto/
├── reloj.html     ← Estructura HTML e interactividad (JavaScript)
└── reloj.css      ← Estilos, animaciones y paleta de colores
```

> ⚠️ Ambos archivos deben estar en la **misma carpeta** para que el enlace de la hoja de estilos funcione correctamente.

---

## ✨ Funcionalidades

| Función | Descripción |
|---|---|
| ⏱️ Hora en tiempo real | Actualización automática cada 1 segundo |
| 📅 Fecha completa | Muestra día, número, mes y año en español |
| 🌍 Zonas horarias | Soporte para 5 ciudades internacionales |
| 🔄 Formato 12h / 24h | Alterna entre ambos formatos con AM/PM |
| ⏸️ Pausar / Reanudar | Detiene la actualización del reloj |
| 👁️ Ocultar segundos | Muestra u oculta el contador de segundos |
| 💡 Indicador de estado | Punto pulsante que refleja el estado actual |

---

## 🌍 Zonas horarias disponibles

- 🇦🇷 Buenos Aires — `America/Argentina/Buenos_Aires`
- 🇪🇸 Madrid — `Europe/Madrid`
- 🇺🇸 Nueva York — `America/New_York`
- 🇬🇧 Londres — `Europe/London`
- 🇯🇵 Tokio — `Asia/Tokyo`

---

## 🚀 Cómo usar

1. Descargar ambos archivos (`reloj.html` y `reloj.css`)
2. Colocarlos en la misma carpeta
3. Abrir `reloj.html` en cualquier navegador moderno
4. No requiere servidor, instalación ni conexión a internet (excepto para cargar las fuentes de Google Fonts)

---

## 🎨 Tecnologías y APIs utilizadas

- **HTML5** — estructura semántica del documento
- **CSS3** — animaciones (`@keyframes`), `clamp()` responsivo, pseudo-elementos
- **JavaScript (ES6+)** — lógica de actualización e interactividad
- **`Intl.DateTimeFormat`** — API nativa del navegador para internacionalización de fechas y zonas horarias
- **`setInterval`** — actualización periódica del display cada 1000 ms
- **Google Fonts** — tipografías *Share Tech Mono* y *Rajdhani*

---

## 🎨 Paleta de colores

| Uso | Color | Hex |
|---|---|---|
| Fondo de página | Negro azulado | `#060910` |
| Fondo tarjeta | Azul oscuro | `#0a0e1a` |
| Dígitos activos | Cian luminoso | `#00e5ff` |
| Estado pausado | Violeta | `#7c3aed` |
| Texto secundario | Gris azulado | `#5a7090` |
| Borde tarjeta | Azul grisáceo | `#1e2a45` |

---

## 💬 Prompts utilizados para generar este proyecto

A continuación se detallan las instrucciones enviadas al asistente para construir este proyecto de forma incremental:

---

### Prompt 1 — Creación inicial del reloj

> *"Quiero que me ayudes a realizar este reloj digital actualizado en HTML y CSS, con un diseño formal, profesional y llamativo, también puede ser interactivo"*

**Resultado:** Se generó un widget interactivo con dígitos en fuente monoespaciada, fondo oscuro, animación de línea de luz en la parte superior, botones de control (12h/24h, pausar, ocultar segundos) y selector de zonas horarias. El reloj usa la API `Intl.DateTimeFormat` para mostrar la hora en tiempo real.

---

### Prompt 2 — Corrección visual de los botones

> *"Sí quiero los dos archivos en HTML y en CSS, modificale los botones que quedan muy oscuros"*

**Resultado:** Se ajustó el estilo de los botones aumentando el contraste: fondo cambiado de `#0f1828` a `#152030`, borde de `#1e2a45` a `#2e4060` y color de texto de `#3a5070` a `#7ab0d8`. Se generaron los archivos separados `reloj.html` y `reloj.css`.

---

### Prompt 3 — Corrección del espaciado entre dígitos

> *"¿Cómo hago para que los números no estén tan separados? Que queden con el original que me pasaste"*

**Resultado:** Se redujo `letter-spacing` de `4px` a `0px` en `.clock-digits` y se ajustó el `font-size` con `clamp(56px, 13vw, 82px)` para que los dígitos queden compactos y en una sola línea sin desbordarse en el navegador.

---

### Prompt 4 — Comentarios profesionales

> *"Dame los dos códigos comentados sin modificaciones, listos para presentar, que queden formal y profesional"*

**Resultado:** Se documentaron ambos archivos con:
- Encabezado de archivo con versión, descripción y tabla de contenidos
- Comentarios de bloque en cada sección HTML y CSS
- Comentarios inline en el JavaScript explicando variables, funciones y flujo de ejecución

---

### Prompt 5 — Generación de este README

> *"Generame también un README con los prompts que te indiqué y el formato HTML y CSS"*

**Resultado:** Este archivo de documentación que describe el proyecto, su estructura, funcionalidades, tecnologías utilizadas y el historial completo de prompts.

---

## 🧠 Estructura del JavaScript (resumen)

```
tzOptions[]          → Array con las 5 zonas horarias disponibles
paused / use12h      → Variables de estado de la configuración
showSeconds / currentTZ

pad(n)               → Formatea números a 2 dígitos: 7 → "07"
tick()               → Función principal: obtiene la hora actual,
                       formatea con Intl.DateTimeFormat y actualiza el DOM

setInterval(tick, 1000) → Llama a tick() cada segundo
```

---

## 📐 Estructura del CSS (resumen)

```
body                 → Fondo negro azulado, centrado con Flexbox
.clock-card          → Panel principal con bordes redondeados
.clock-card::before  → Línea de luz animada en la parte superior
.clock-digits        → Dígitos en fuente monoespaciada, cian brillante
.colon-blink         → Parpadeo de los dos puntos separadores
.btn / .tz-btn       → Botones de control y zona horaria
.dot                 → Punto pulsante del indicador de estado

@keyframes scanline  → Pulso de opacidad de la línea superior
@keyframes blink     → Parpadeo on/off de los separadores ":"
@keyframes pulse     → Latido del punto indicador de estado
```

---

## 🌐 Compatibilidad

| Navegador | Soporte |
|---|---|
| Google Chrome 80+ | ✅ Completo |
| Mozilla Firefox 75+ | ✅ Completo |
| Microsoft Edge 80+ | ✅ Completo |
| Safari 14+ | ✅ Completo |
| Opera 67+ | ✅ Completo |

> Requiere soporte para `Intl.DateTimeFormat` con `formatToParts()` y `clamp()` en CSS. Todos los navegadores modernos lo soportan.

---

*Documentación generada con Claude — Anthropic*
