# Bloques de Inicialización en Java

> **Consigna:** ¿Cómo reemplazarías un bloque `static` o no `static` de inicialización? Investigar.

---

## El problema: bloques de inicialización (patrón viejo)

```java
// BLOQUE ESTÁTICO (se ejecuta 1 sola vez al cargar la clase)
static {
    System.out.println("Ejecución del bloque estático");
    ++Persona.contadorPersonas;
}

// BLOQUE NO ESTÁTICO (se copia en cada constructor antes de su cuerpo)
{
    System.out.println("Ejecución del bloque NO estático");
    this.idPersona = Persona.contadorPersonas++;
}
```

---

## Por qué son "viejos"

- **Son difíciles de leer:** la lógica está dispersa, no en el constructor ni en la declaración.
- **El bloque no estático es especialmente confuso** porque el compilador lo copia dentro de cada constructor antes de su cuerpo, lo cual no es evidente.
- **El bloque estático casi siempre puede reemplazarse** con inicialización directa en la declaración.

---

## Cómo reemplazarlos (forma moderna)

### Bloque `static` → inicialización directa del campo

```java
// ANTES (bloque estático)
private static int contadorPersonas;
static {
    ++Persona.contadorPersonas; // queda en 1
}

// AHORA (moderno)
private static int contadorPersonas = 1; // directo en la declaración
```

### Bloque no `static` → lógica en el constructor

```java
// ANTES (bloque no estático)
{
    this.idPersona = Persona.contadorPersonas++;
}
public Persona() {
    System.out.println("Ejecución del constructor");
}

// AHORA (moderno)
public Persona() {
    this.idPersona = Persona.contadorPersonas++; // va directo acá
    System.out.println("Ejecución del constructor");
}
```

---

## Clase reemplazada completa

```java
package domain;

public class Persona {

    private final int idPersona;
    private static int contadorPersonas = 1; // reemplaza el bloque static

    public Persona() {
        this.idPersona = Persona.contadorPersonas++; // reemplaza el bloque no static
        System.out.println("Ejecución del constructor");
    }

    public int getIdPersona() {
        return this.idPersona;
    }

    @Override
    public String toString() {
        return "Persona{" + "idPersona=" + idPersona + '}';
    }
}
```

---

## Resumen de la regla

| Tipo de bloque | Reemplazar con |
|---|---|
| `static { }` | Inicialización directa: `private static int x = valor;` |
| `{ }` (no static) | Lógica dentro del constructor |

> **Excepción:** el bloque `static` sigue siendo necesario cuando la inicialización requiere manejo de excepciones checked (por ejemplo, cargar un driver de base de datos), porque una declaración directa no puede usar `try/catch`. Pero para casos simples como este, es innecesario.
