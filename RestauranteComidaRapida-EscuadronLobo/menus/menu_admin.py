"""
menu_admin.py
=============
Módulo que implementa la interfaz de administración del sistema de gestión
de un restaurante. Define la clase MenuAdmin, responsable de orquestar las
operaciones de alto nivel accesibles exclusivamente por usuarios con rol
de administrador: gestión de usuarios, control del menú, inventario/stock
y reportes de ventas.

Dependencias internas:
    - gestion.gestion_usuarios  : CRUD de cuentas de usuario.
    - gestion.gestion_stock     : Consulta y ajuste del inventario.
    - gestion.gestion_ventas    : Registro y consulta de ventas.
    - menus.utils               : Utilidades de presentación en consola.

"""

import re

# ---------------------------------------------------------------------------
# Importaciones del dominio de negocio
# ---------------------------------------------------------------------------
from gestion.gestion_usuarios import get_todos, crear_usuario, eliminar_usuario, ROLES
from gestion.gestion_stock import (
    get_todos as get_ingredientes,   # Alias para evitar colisión de nombres
    get_alertas,
    ajustar_stock,
    get_todos_productos,
    toggle_disponible,
)
from gestion.gestion_ventas import (
    get_ventas_hoy,
    get_ventas_por_fecha,
    get_resumen_ventas,
    get_items_venta,
)
from menus.utils import limpiar, separador, icono_stock, cambiar_contrasena_ui

# ---------------------------------------------------------------------------
# Constantes de presentación
# ---------------------------------------------------------------------------
# Mapeo de claves internas de categoría al texto visible en pantalla.
# Centralizar el mapeo aquí evita repetir strings en múltiples lugares
# y facilita la internacionalización futura.
CATEGORIAS_LABEL = {
    "hamburguesa":    "Hamburguesa",
    "pizza":          "Pizza",
    "acompanamiento": "Acompañamiento",
    "bebida":         "Bebida",
}


# ===========================================================================
class MenuAdmin:
    """
    Controlador de la interfaz de administración del sistema.

    Esta clase sigue el patrón de diseño *Command / Controller*: centraliza
    la lógica de navegación y delega las operaciones reales a los módulos de
    gestión correspondientes.  Cada método público representa una sección del
    menú; cada método privado (prefijo ``_``) implementa una acción atómica.

    Atributos:
        user (dict): Diccionario con los datos del administrador autenticado.
                     Se espera que contenga al menos las claves
                     ``'id'``, ``'nombre'`` y ``'usuario'``.
    """

    def __init__(self, user: dict) -> None:
        """
        Inicializa el controlador con el usuario que inició sesión.

        Args:
            user (dict): Datos del administrador obtenidos tras la autenticación.
        """
        self.user = user

    # -----------------------------------------------------------------------
    # Menú principal
    # -----------------------------------------------------------------------
    def ejecutar(self) -> None:
        """
        Punto de entrada principal del panel de administración.

        Implementa un bucle de evento simple (REPL) que presenta el menú
        principal y despacha la opción seleccionada al método correspondiente.
        El bucle finaliza cuando el usuario elige la opción ``0`` (cerrar sesión).
        """
        while True:
            limpiar()
            print("=" * 48)
            print(f"  ADMIN — {self.user['nombre']}")
            print("=" * 48)
            print("  1. Gestión de usuarios")
            print("  2. Gestión del menú")
            print("  3. Inventario / Stock")
            print("  4. Reportes de ventas")
            print("  5. Cambiar contraseña")
            print("  0. Cerrar sesión")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self.gestion_usuarios()
            elif op == "2":
                self.gestion_menu()
            elif op == "3":
                self.gestion_stock()
            elif op == "4":
                self.reportes_ventas()
            elif op == "5":
                self._cambiar_contrasena()
            elif op == "0":
                break   # Termina el bucle y cierra la sesión

    # =======================================================================
    # SECCIÓN: GESTIÓN DE USUARIOS
    # =======================================================================
    def gestion_usuarios(self) -> None:
        """
        Submenú de administración de cuentas de usuario.

        Presenta las opciones de: listar, crear y eliminar usuarios,
        y retorna al menú principal cuando el usuario elige ``0``.
        """
        while True:
            limpiar()
            print("=" * 48)
            print("  GESTIÓN DE USUARIOS")
            print("=" * 48)
            print("  1. Ver todos los usuarios")
            print("  2. Crear usuario")
            print("  3. Eliminar usuario")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ver_usuarios()
            elif op == "2":
                self._crear_usuario()
            elif op == "3":
                self._eliminar_usuario()
            elif op == "0":
                break

    def _ver_usuarios(self) -> None:
        """
        Muestra el listado completo de usuarios registrados en el sistema.

        Recupera todos los usuarios mediante ``get_todos()`` y los presenta
        en formato tabular con columnas alineadas para mejorar la legibilidad.
        """
        limpiar()
        usuarios = get_todos()
        print("=" * 48)
        print("  USUARIOS")
        separador(48)
        # Encabezado de columnas con ancho fijo para alineación tabular
        print(f"  {'ID':<4} {'Nombre':<20} {'Usuario':<14} {'Rol'}")
        separador(48)
        for u in usuarios:
            print(f"  {u['id']:<4} {u['nombre']:<20} {u['usuario']:<14} {u['rol']}")
        separador(48)
        print(f"  Total: {len(usuarios)} usuarios")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _crear_usuario(self) -> None:
        """
        Guía al administrador por el flujo de creación de un nuevo usuario.

        Valida que:
            - Ningún campo obligatorio esté vacío.
            - El rol ingresado exista en la lista ``ROLES`` definida en
              ``gestion_usuarios``.

        Si la validación es exitosa, delega la creación a ``crear_usuario()``,
        que retorna una tupla ``(ok: bool, mensaje: str)``.
        """
        limpiar()
        print("=" * 48)
        print("  CREAR USUARIO")
        print("=" * 48)

        nombre    = input("  Nombre completo : ").strip()
        usuario   = input("  Usuario         : ").strip()
        contrasena = input("  Contraseña      : ").strip()

        print(f"  Roles disponibles: {', '.join(ROLES)}")
        rol = input("  Rol             : ").strip().lower()

        # --- Validación de campos obligatorios ---
        if not nombre or not usuario or not contrasena:
            print("\n  Todos los campos son obligatorios.")
            input("  Presiona Enter para volver...")
            return

        # --- Validación del rol ---
        if rol not in ROLES:
            print(f"\n  Rol inválido. Debe ser uno de: {', '.join(ROLES)}")
            input("  Presiona Enter para volver...")
            return

        # Delegar la creación al módulo de negocio
        ok, msg = crear_usuario(nombre, usuario, contrasena, rol)
        print(f"\n  {msg}")
        input("  Presiona Enter para continuar...")

    def _eliminar_usuario(self) -> None:
        """
        Permite al administrador eliminar una cuenta de usuario existente.

        Presenta la lista numerada de usuarios y solicita la selección por
        número de posición.  Incluye dos salvaguardas:
            1. Impide que el administrador se elimine a sí mismo.
            2. Requiere confirmación explícita (``s/n``) antes de proceder.
        """
        limpiar()
        usuarios = get_todos()
        print("=" * 48)
        print("  ELIMINAR USUARIO")
        separador(48)
        for i, u in enumerate(usuarios, 1):
            print(f"  {i:>2}. [{u['rol']:<8}] {u['nombre']}  (@{u['usuario']})")
        separador(48)
        print("   0. Volver")
        print("=" * 48)

        op = input("  ¿Cuál eliminás? (número): ").strip()

        # Validar que la entrada sea un número dentro del rango válido
        if op == "0" or not op.isdigit() or not (1 <= int(op) <= len(usuarios)):
            return

        target = usuarios[int(op) - 1]

        # --- Salvaguarda: no permitir la auto-eliminación ---
        if target["id"] == self.user["id"]:
            print("\n  No podés eliminarte a vos mismo.")
            input("  Presiona Enter para volver...")
            return

        # --- Confirmación explícita antes de eliminar ---
        confirmar = input(f"  ¿Eliminar a {target['nombre']}? (s/n): ").strip().lower()
        if confirmar == "s":
            eliminar_usuario(target["id"])
            print(f"\n  Usuario '{target['nombre']}' eliminado.")
        else:
            print("\n  Cancelado.")
        input("  Presiona Enter para continuar...")

    # =======================================================================
    # SECCIÓN: GESTIÓN DEL MENÚ
    # =======================================================================
    def gestion_menu(self) -> None:
        """
        Submenú de administración de productos del menú del restaurante.

        Permite visualizar los productos disponibles y alternar su estado
        (habilitado / deshabilitado) sin necesidad de eliminarlos.
        """
        while True:
            limpiar()
            print("=" * 48)
            print("  GESTIÓN DEL MENÚ")
            print("=" * 48)
            print("  1. Ver todos los productos")
            print("  2. Habilitar / deshabilitar producto")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ver_productos()
            elif op == "2":
                self._toggle_producto()
            elif op == "0":
                break

    def _ver_productos(self) -> None:
        """
        Muestra el catálogo completo de productos agrupados por categoría.

        Itera la lista de productos y detecta cambios de categoría para
        imprimir un encabezado de sección en cada transición.
        El estado de disponibilidad se indica con ``OK`` o ``OFF``.
        """
        limpiar()
        productos = get_todos_productos()
        print("=" * 48)
        print("  PRODUCTOS")
        separador(48)

        cat_actual = None
        for p in productos:
            # Obtener la etiqueta legible de la categoría; si no existe en el
            # mapeo, se usa el valor crudo como fallback
            cat = CATEGORIAS_LABEL.get(p["categoria"], p["categoria"])

            # Imprimir encabezado de categoría cuando hay un cambio de sección
            if cat != cat_actual:
                if cat_actual:
                    separador(48)   # Separador entre categorías
                print(f"  {cat.upper()}")
                cat_actual = cat

            # Componer el nombre del producto con variante opcional
            nombre = p["nombre"]
            if p["variante"]:
                nombre += f" ({p['variante']})"

            estado = "OK" if p["disponible"] else "OFF"
            print(f"  {p['id']:>3}. {nombre:<32} ${p['precio']:.2f}  [{estado}]")

        separador(48)
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _toggle_producto(self) -> None:
        """
        Alterna el estado de disponibilidad de un producto (ON ↔ OFF).

        Solicita al administrador el ID del producto y llama a
        ``toggle_disponible()``, que invierte el valor booleano en la
        base de datos sin requerir que el administrador conozca el estado
        actual.  El ID se valida contra la lista actual de productos para
        prevenir errores de integridad.
        """
        limpiar()
        productos = get_todos_productos()
        print("=" * 48)
        print("  HABILITAR / DESHABILITAR PRODUCTO")
        separador(48)
        for p in productos:
            nombre = p["nombre"]
            if p["variante"]:
                nombre += f" ({p['variante']})"
            estado = "ON" if p["disponible"] else "OFF"
            print(f"  {p['id']:>3}. [{estado}] {nombre}")
        separador(48)
        print("   0. Volver")
        print("=" * 48)

        op = input("  ID del producto: ").strip()
        if op == "0":
            return

        # Validar que el ID ingresado corresponda a un producto existente
        ids = [p["id"] for p in productos]
        if not op.isdigit() or int(op) not in ids:
            print("  ID inválido.")
            input("  Presiona Enter para volver...")
            return

        toggle_disponible(int(op))
        print(f"\n  Producto actualizado.")
        input("  Presiona Enter para continuar...")

    # =======================================================================
    # SECCIÓN: INVENTARIO / STOCK
    # =======================================================================
    def gestion_stock(self) -> None:
        """
        Submenú de control de inventario de ingredientes.

        Centraliza la visualización del stock, la consulta de alertas por
        niveles bajos y el ajuste manual de cantidades (reposición o descuento).
        """
        while True:
            limpiar()
            print("=" * 48)
            print("  INVENTARIO / STOCK")
            print("=" * 48)
            print("  1. Ver stock completo")
            print("  2. Ver alertas de stock bajo")
            print("  3. Reponer ingrediente")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ver_stock_completo()
            elif op == "2":
                self._ver_alertas()
            elif op == "3":
                self._reponer()
            elif op == "0":
                break

    def _ver_stock_completo(self) -> None:
        """
        Muestra el inventario completo de ingredientes con indicadores visuales.

        Cada fila incluye el icono retornado por ``icono_stock()``, que
        permite identificar visualmente los ingredientes cuya cantidad actual
        ha alcanzado o caído por debajo del mínimo configurado.

        Al pie del listado se informa cuántos ingredientes presentan alertas.
        """
        limpiar()
        ingredientes = get_ingredientes()
        print("=" * 48)
        print("  STOCK COMPLETO")
        separador(48)
        print(f"  {'ID':<4} {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
        separador(48)
        for ing in ingredientes:
            icono = icono_stock(ing["cantidad"], ing["minimo"])
            print(
                f"  {ing['id']:<4} {ing['nombre']:<25} "
                f"{ing['cantidad']:>6}  {ing['minimo']:>5}  {icono}"
            )
        separador(48)
        # Conteo inline de alertas sin llamada adicional a la base de datos
        alertas = [i for i in ingredientes if i["cantidad"] <= i["minimo"]]
        if alertas:
            print(f"  {len(alertas)} ingrediente(s) con stock bajo.")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _ver_alertas(self) -> None:
        """
        Muestra únicamente los ingredientes cuyo stock está en nivel crítico.

        Llama a ``get_alertas()``, que ya filtra en la capa de datos, por lo
        que este método solo es responsable de la presentación. Si no hay
        alertas activas, informa al usuario que el inventario está en orden.
        """
        limpiar()
        alertas = get_alertas()
        print("=" * 48)
        print("  ALERTAS DE STOCK BAJO")
        separador(48)
        if not alertas:
            print("  Sin alertas. Todo el stock está OK.")
        else:
            print(f"  {'ID':<4} {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
            separador(48)
            for a in alertas:
                # El símbolo ⚠ refuerza visualmente el estado de alerta
                print(
                    f"  {a['id']:<4} {a['nombre']:<25} "
                    f"{a['cantidad']:>6}  {a['minimo']:>5}  ⚠"
                )
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _reponer(self) -> None:
        """
        Permite al administrador agregar o quitar unidades de un ingrediente.

        Flujo de interacción:
            1. Muestra el listado de ingredientes con su stock actual.
            2. Solicita el ID del ingrediente a ajustar.
            3. Pregunta si se desea agregar (``1``) o quitar (``2``) unidades.
            4. Solicita la cantidad y aplica el signo correspondiente.
            5. Llama a ``ajustar_stock(id, delta)`` donde ``delta`` puede
               ser positivo (reposición) o negativo (descuento).

        La función ``ajustar_stock`` es responsable de validar que el
        resultado no sea negativo; este método solo prepara los parámetros.
        """
        limpiar()
        ingredientes = get_ingredientes()
        print("=" * 48)
        print("  AJUSTAR STOCK")
        separador(48)
        print(f"  {'ID':<4} {'Ingrediente':<25} {'Stock':>6}  {'Mín':>5}")
        separador(48)
        for ing in ingredientes:
            icono = icono_stock(ing["cantidad"], ing["minimo"])
            print(
                f"  {ing['id']:<4} {ing['nombre']:<25} "
                f"{ing['cantidad']:>6}  {ing['minimo']:>5}  {icono}"
            )
        separador(48)
        print("   0. Volver")
        print("=" * 48)

        op = input("  ID del ingrediente: ").strip()
        if op == "0":
            return

        # Validar que el ID exista en la lista actual de ingredientes
        ids = [i["id"] for i in ingredientes]
        if not op.isdigit() or int(op) not in ids:
            print("  ID inválido.")
            input("  Presiona Enter para volver...")
            return

        # Recuperar el objeto completo del ingrediente seleccionado
        ing = next(i for i in ingredientes if i["id"] == int(op))
        print(f"\n  {ing['nombre']} — Stock actual: {ing['cantidad']}")
        print("  1. Agregar")
        print("  2. Quitar")
        accion = input("  Opción: ").strip()

        if accion not in ("1", "2"):
            return

        cant = input("  Cantidad: ").strip()
        if not cant.isdigit() or int(cant) < 1:
            print("  Cantidad inválida.")
            input("  Presiona Enter para volver...")
            return

        # Convertir cantidad a delta: positivo para agregar, negativo para quitar
        cantidad = int(cant) if accion == "1" else -int(cant)
        ajustar_stock(ing["id"], cantidad)
        signo = "+" if cantidad > 0 else ""
        print(f"\n  {ing['nombre']}: {signo}{cantidad} unidades.")
        input("  Presiona Enter para continuar...")

    # =======================================================================
    # SECCIÓN: REPORTES DE VENTAS
    # =======================================================================
    def reportes_ventas(self) -> None:
        """
        Submenú de reportes de ventas.

        Muestra un resumen ejecutivo en el encabezado (total de ventas,
        recaudación acumulada y recaudación del día) antes de presentar
        las opciones de detalle.  El resumen se refresca en cada iteración
        del bucle para reflejar datos actualizados.
        """
        while True:
            limpiar()
            resumen = get_resumen_ventas()
            print("=" * 48)
            print("  REPORTES DE VENTAS")
            separador(48)
            print(f"  Total de ventas:     {resumen['total_ventas']}")
            print(f"  Recaudado total:     ${resumen['total_recaudado']:.2f}")
            print(f"  Recaudado hoy:       ${resumen['hoy']:.2f}")
            separador(48)
            print("  1. Ver ventas de hoy")
            print("  2. Ver ventas por fecha")
            print("  0. Volver")
            print("=" * 48)

            op = input("  Opción: ").strip()

            if op == "1":
                self._ventas_hoy()
            elif op == "2":
                self._ventas_por_fecha()
            elif op == "0":
                break

    def _mostrar_ventas(self, ventas: list, titulo: str) -> None:
        """
        Renderiza un listado de ventas con su detalle de ítems.

        Método auxiliar reutilizado por ``_ventas_hoy`` y ``_ventas_por_fecha``
        para evitar duplicación de código (principio DRY).

        Por cada venta se muestra: ID de venta, ID de orden, mesa, total y hora.
        Debajo de cada venta se listan los ítems consumidos con sus variantes.

        Args:
            ventas (list): Lista de diccionarios de ventas a mostrar.
            titulo (str) : Título a mostrar en el encabezado del reporte.
        """
        limpiar()
        print("=" * 48)
        print(f"  {titulo}")
        separador(48)
        if not ventas:
            print("  Sin ventas registradas.")
        else:
            for v in ventas:
                # Extraer solo la hora de la marca de tiempo completa
                hora = v["fecha"].strftime("%H:%M")
                print(
                    f"  Venta #{v['id']}  Orden #{v['orden_id']}  "
                    f"Mesa {v['mesa']}  ${v['total']:.2f}  {hora}"
                )
                # Recuperar y listar los ítems de cada venta (detalle)
                items = get_items_venta(v["orden_id"])
                for it in items:
                    nombre = it["nombre"]
                    if it["variante"]:
                        nombre += f" ({it['variante']})"
                    print(f"      {it['cantidad']}x  {nombre}")
                separador(48)

            # Totalizador al pie del reporte
            total = sum(v["total"] for v in ventas)
            print(f"  TOTAL: ${total:.2f}  ({len(ventas)} ventas)")
        print("=" * 48)
        input("  Presiona Enter para volver...")

    def _ventas_hoy(self) -> None:
        """
        Delega la obtención de ventas del día a ``get_ventas_hoy()``
        y las pasa al método genérico de visualización.
        """
        self._mostrar_ventas(get_ventas_hoy(), "VENTAS DE HOY")

    def _ventas_por_fecha(self) -> None:
        """
        Solicita una fecha al administrador y muestra las ventas de ese día.

        Valida el formato de entrada con una expresión regular (``AAAA-MM-DD``)
        antes de consultar la base de datos, evitando queries con fechas
        malformadas que podrían causar errores en la capa de datos.

        Formato esperado: ``AAAA-MM-DD`` (ej: ``2026-04-02``).
        """
        limpiar()
        fecha = input("  Fecha (AAAA-MM-DD): ").strip()

        # Validar formato de fecha con expresión regular
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            print("\n  Formato inválido. Usá AAAA-MM-DD (ej: 2026-04-02).")
            input("  Presiona Enter para volver...")
            return

        ventas = get_ventas_por_fecha(fecha)
        self._mostrar_ventas(ventas, f"VENTAS DEL {fecha}")

    # -----------------------------------------------------------------------
    # Utilidad: cambio de contraseña
    # -----------------------------------------------------------------------
    def _cambiar_contrasena(self) -> None:
        """
        Invoca el flujo estándar de cambio de contraseña definido en
        ``menus.utils``.

        Pasa el usuario actual y el ancho de pantalla como argumentos para
        que la utilidad pueda formatear la salida de forma consistente con
        el resto del panel de administración.
        """
        cambiar_contrasena_ui(self.user, ancho=48)