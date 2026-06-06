# Restaurante Escuadrón Lobo

Sistema de gestión para un restaurante de comida rápida, desarrollado en Python con PostgreSQL como base de datos. Permite administrar usuarios, menú, stock, pedidos y ventas con un flujo de trabajo diferenciado por rol: administrador, mozo, cocinero y cliente.

---

## Tecnologías

| Tecnología | Versión | Uso |
|------------|---------|-----|
| Python | 3.10+ | Lenguaje principal |
| PostgreSQL | 17 | Motor de base de datos |
| psycopg | 3.x | Driver Python para PostgreSQL |
| pgAdmin 4 | — | Administración visual de la base de datos |

---

## Roles del sistema

| Rol | Descripción |
|-----|-------------|
| **Admin** | Gestión de usuarios, menú, stock e inventario, reportes de ventas |
| **Mozo** | Ver mesas, tomar pedidos, entregar y cancelar órdenes |
| **Cocinero** | Ver pedidos activos, marcar como preparando/listo, ver stock |
| **Cliente** | Ver menú, hacer pedidos, ver estado de sus pedidos |

---

## Instalación

### 1. Requisitos previos

- Python 3.10+ con **"Add Python to PATH"** tildado durante la instalación
- PostgreSQL 17 + pgAdmin 4

### 2. Crear la base de datos

Abrí pgAdmin 4 y ejecutá:

```sql
CREATE DATABASE restaurante_escuadronlobo;
```

### 3. Clonar el repositorio

```
git clone https://github.com/HotCode2025/EscuadronLobo-TercerSemestre.git
cd RestauranteComidaRapida-EscuadronLobo
```

### 4. Instalar dependencias

```
pip install "psycopg[binary]"
```

### 5. Configurar la contraseña

En `database.py` línea 10, cambiá la contraseña por la que pusiste al instalar PostgreSQL:

```python
"password": os.environ.get("PGPASSWORD", "tu_contraseña"),
```

### 6. Correr el proyecto

```
python main.py
```

Las tablas y los datos de prueba se crean automáticamente en el primer arranque.

---

## Credenciales de prueba

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| admin | admin123 | Admin |
| mozo1 | mozo123 | Mozo |
| cocina1 | cocina123 | Cocinero |
| cliente1 | cliente123 | Cliente |
| cliente2 | cliente123 | Cliente |

---

## Estructura del proyecto

```
├── main.py                      # Entrada, login y enrutamiento por rol
├── database.py                  # Conexión a PostgreSQL, helper execute(), init_db()
├── seed.py                      # Carga de datos iniciales
├── requirements.txt
├── gestion/
│   ├── gestion_usuarios.py      # CRUD de usuarios, hash SHA-256
│   ├── gestion_pedidos.py       # Motor de pedidos, verificación de stock
│   ├── gestion_stock.py         # Control de inventario
│   └── gestion_ventas.py        # Reportes de ventas
└── menus/
    ├── utils.py                 # Funciones compartidas por todos los menús
    ├── menu_admin.py            # Panel del administrador
    ├── menu_mozo.py             # Interfaz del mozo
    ├── menu_cocinero.py         # Interfaz del cocinero
    └── menu_cliente.py          # Interfaz del cliente
```

---

## Base de datos

El sistema usa 7 tablas relacionales:

```
usuarios
├── id          SERIAL PRIMARY KEY
├── nombre      TEXT
├── usuario     TEXT UNIQUE
├── contrasena  TEXT
└── rol         TEXT  →  admin / mozo / cocinero / cliente

ingredientes
├── id          SERIAL PRIMARY KEY
├── nombre      TEXT UNIQUE
├── cantidad    INTEGER
└── minimo      INTEGER  →  nivel mínimo de alerta

productos
├── id          SERIAL PRIMARY KEY
├── nombre      TEXT
├── categoria   TEXT  →  hamburguesa / pizza / acompanamiento / bebida
├── variante    TEXT
├── precio      NUMERIC(10,2)
└── disponible  BOOLEAN

producto_ingredientes       →  receta de cada producto
├── producto_id    INTEGER  FK → productos
├── ingrediente_id INTEGER  FK → ingredientes
└── cantidad       INTEGER  →  cantidad necesaria por receta

ordenes
├── id          SERIAL PRIMARY KEY
├── cliente_id  INTEGER  FK → usuarios
├── mozo_id     INTEGER  FK → usuarios
├── mesa        INTEGER
├── estado      TEXT  →  pendiente / preparando / listo / entregado
├── total       NUMERIC(10,2)
└── creado_en   TIMESTAMP DEFAULT NOW()

orden_items
├── id          SERIAL PRIMARY KEY
├── orden_id    INTEGER  FK → ordenes
├── producto_id INTEGER  FK → productos
├── cantidad    INTEGER
└── subtotal    NUMERIC(10,2)

ventas
├── id          SERIAL PRIMARY KEY
├── orden_id    INTEGER  FK → ordenes
├── total       NUMERIC(10,2)
└── fecha       TIMESTAMP DEFAULT NOW()
```

---

## Características técnicas

- Autenticación con hash **SHA-256** — las contraseñas nunca se guardan en texto plano
- Verificación de stock antes de confirmar cualquier pedido
- Descuento automático de ingredientes al marcar una orden como lista usando `GREATEST(0, x)` para nunca bajar de cero
- Resultados de queries como diccionarios con `row_factory=dict_row`
- `INSERT ... RETURNING id` para obtener IDs generados por PostgreSQL
- Transacciones con `commit()` y `rollback()` en operaciones críticas

---

## Equipo

**Escuadrón Lobo — Programación III**

| Integrante | Módulo |
|------------|--------|
| Lucas | `main.py` y `menus/utils.py` |
| Cecilia | `database.py`, `seed.py` y `gestion/gestion_usuarios.py` |
| Valeria | `menus/menu_admin.py` |
| Valentín | `gestion/gestion_pedidos.py` |
| Darío | `menus/menu_mozo.py` |
| Orlando | `gestion/gestion_stock.py` y `menus/menu_cocinero.py` |
| Juan | `menus/menu_cliente.py` y `gestion/gestion_ventas.py` |
