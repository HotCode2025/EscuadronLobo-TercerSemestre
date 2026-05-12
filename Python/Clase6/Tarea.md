# Trabajo en VSC con Entornos Virtuales

## 1. Crear el entorno virtual

### Windows
```bash
python -m venv venv
```

### Linux
```bash
python3 -m venv venv
```

---

## 2. Activar el entorno virtual desde la terminal

### Linux
```bash
source venv/bin/activate
```

### Windows
```bash
venv/scripts/activate
```

---

## 3. Desactivar el entorno virtual

Para desactivar el entorno virtual desde la terminal se utiliza el siguiente comando:

```bash
deactivate
```

Este comando funciona tanto en Windows como en Linux una vez que el entorno virtual está activado.

---

# 4. ¿Qué es el DOM?

El **DOM (Document Object Model)** es una representación en forma de árbol de una página web creada por el navegador.

Gracias al DOM, JavaScript puede:

- acceder a los elementos HTML,
- modificarlos,
- agregar o eliminar contenido,
- cambiar estilos,
- responder a eventos del usuario.

## Ejemplo

Si una página tiene un botón o un título, JavaScript puede encontrarlos mediante el DOM y cambiar su contenido o comportamiento dinámicamente.