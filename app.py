"""
app.py — Punto de entrada del sistema de inventario.

Ejecutar: python app.py
"""

import os
from historia_usuario_3.servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    mostrar_estadisticas,
)
from historia_usuario_3.archivos import guardar_csv, cargar_csv, fusionar

# ─────────────────────────────────────────────
#  UTILIDADES DE INTERFAZ
# ─────────────────────────────────────────────

def limpiar():
    """Limpia la terminal (compatible con Windows y Unix)."""
    os.system("cls" if os.name == "nt" else "clear")


def separador(caracter="─", ancho=44):
    print(caracter * ancho)


def titulo(texto):
    separador("═")
    print(f"  {texto}")
    separador("═")


def pausar():
    input("\n  Presiona ENTER para continuar...")


def pedir_float(mensaje, minimo=0.0):
    """
    Solicita un número decimal al usuario con validación.

    Parámetros:
        mensaje (str):   Texto a mostrar.
        minimo  (float): Valor mínimo aceptado.

    Retorna:
        float: Valor ingresado y válido.
    """
    try:
        valor = float(input(mensaje))
        if valor < minimo:
            print(f"  ⚠️  El valor debe ser ≥ {minimo}.")
            return pedir_float(mensaje, minimo)   # reintento recursivo
        return valor
    except ValueError:
        print("  ⚠️  Ingresa un número válido (ej. 12.50).")
        return pedir_float(mensaje, minimo)       # reintento recursivo


def pedir_int(mensaje, minimo=0):
    """
    Solicita un número entero al usuario con validación.

    Parámetros:
        mensaje (str): Texto a mostrar.
        minimo  (int): Valor mínimo aceptado.

    Retorna:
        int: Valor ingresado y válido.
    """
    try:
        valor = int(input(mensaje))
        if valor < minimo:
            print(f"  ⚠️  El valor debe ser ≥ {minimo}.")
            return pedir_int(mensaje, minimo)     # reintento recursivo
        return valor
    except ValueError:
        print("  ⚠️  Ingresa un número entero válido.")
        return pedir_int(mensaje, minimo)         # reintento recursivo


def pedir_ruta(mensaje, extension=".csv"):
    """
    Solicita una ruta de archivo al usuario.

    Parámetros:
        mensaje   (str): Texto a mostrar.
        extension (str): Extensión esperada.

    Retorna:
        str: Ruta ingresada (con extensión corregida si falta).
    """
    ruta = input(mensaje).strip()
    if not ruta:
        ruta = "inventario.csv"
    if not ruta.endswith(extension):
        ruta += extension
    return ruta


# ─────────────────────────────────────────────
#  OPCIONES DEL MENÚ
# ─────────────────────────────────────────────

def menu_agregar(inventario):
    titulo("➕  AGREGAR PRODUCTO")
    nombre = input("  Nombre del producto : ").strip()
    if not nombre:
        print("  ⚠️  El nombre no puede estar vacío.")
        pausar()
        return
    precio   = pedir_float("  Precio unitario    : $")
    cantidad = pedir_int("  Cantidad en stock  : ")
    mensaje  = agregar_producto(inventario, nombre, precio, cantidad)
    print(f"\n  {mensaje}")
    pausar()


def menu_mostrar(inventario):
    titulo("📦  INVENTARIO ACTUAL")
    mostrar_inventario(inventario)
    pausar()


def menu_buscar(inventario):
    titulo("🔍  BUSCAR PRODUCTO")
    nombre   = input("  Nombre a buscar : ").strip()
    producto = buscar_producto(inventario, nombre)
    if producto:
        print(f"\n  ✅  Encontrado:")
        print(f"     • Nombre   : {producto['nombre']}")
        print(f"     • Precio   : ${producto['precio']:.2f}")
        print(f"     • Cantidad : {producto['cantidad']} uds")
        print(f"     • Subtotal : ${producto['precio'] * producto['cantidad']:.2f}")
    else:
        print(f"\n  ⚠️  '{nombre}' no está en el inventario.")
    pausar()


def menu_actualizar(inventario):
    titulo("✏️   ACTUALIZAR PRODUCTO")
    nombre = input("  Nombre del producto : ").strip()
    if not buscar_producto(inventario, nombre):
        print(f"\n  ⚠️  '{nombre}' no encontrado.")
        pausar()
        return

    print("\n  ¿Qué deseas actualizar?")
    print("  [1] Solo precio")
    print("  [2] Solo cantidad")
    print("  [3] Ambos")
    opcion = input("  Opción : ").strip()

    nuevo_precio    = None
    nueva_cantidad  = None

    if opcion in ("1", "3"):
        nuevo_precio = pedir_float("  Nuevo precio    : $")
    if opcion in ("2", "3"):
        nueva_cantidad = pedir_int("  Nueva cantidad  : ")
    if opcion not in ("1", "2", "3"):
        print("  ⚠️  Opción no válida.")
        pausar()
        return

    mensaje = actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)
    print(f"\n  {mensaje}")
    pausar()


def menu_eliminar(inventario):
    titulo("🗑️   ELIMINAR PRODUCTO")
    nombre = input("  Nombre a eliminar : ").strip()
    producto = buscar_producto(inventario, nombre)
    if not producto:
        print(f"\n  ⚠️  '{nombre}' no encontrado.")
        pausar()
        return

    confirma = input(f"\n  ¿Eliminar '{producto['nombre']}'? (S/N) : ").strip().upper()
    if confirma == "S":
        mensaje = eliminar_producto(inventario, nombre)
        print(f"\n  {mensaje}")
    else:
        print("  ↩️  Operación cancelada.")
    pausar()


def menu_estadisticas(inventario):
    titulo("📊  ESTADÍSTICAS")
    mostrar_estadisticas(inventario)
    pausar()


def menu_guardar(inventario):
    titulo("💾  GUARDAR CSV")
    ruta = pedir_ruta("  Ruta del archivo [inventario.csv] : ")
    guardar_csv(inventario, ruta)
    pausar()


def menu_cargar(inventario):
    titulo("📂  CARGAR CSV")
    ruta = pedir_ruta("  Ruta del archivo [inventario.csv] : ")

    nuevos, filas_invalidas = cargar_csv(ruta)

    if nuevos is None:
        # Error irrecuperable (archivo no encontrado, encabezado inválido, etc.)
        pausar()
        return

    print(f"\n  ℹ️  {len(nuevos)} producto(s) válidos leídos.", end="")
    if filas_invalidas:
        print(f"  |  {filas_invalidas} fila(s) inválida(s) omitida(s).")
    else:
        print()

    if not nuevos:
        print("  ⚠️  No hay datos válidos para cargar.")
        pausar()
        return

    accion = input("\n  ¿Sobrescribir inventario actual? (S/N) : ").strip().upper()

    if accion == "S":
        inventario.clear()
        inventario.extend(nuevos)
        print(f"\n  ✅  Inventario reemplazado con {len(nuevos)} producto(s).")
    else:
        agregados, actualizados = fusionar(inventario, nuevos)
        print(f"\n  ✅  Fusión completada:")
        print(f"     • Productos nuevos agregados : {agregados}")
        print(f"     • Productos actualizados     : {actualizados}")

    print(f"\n  📋  Resumen final:")
    print(f"     • Productos cargados del CSV : {len(nuevos)}")
    print(f"     • Filas inválidas omitidas   : {filas_invalidas}")
    print(f"     • Acción realizada           : {'Reemplazo' if accion == 'S' else 'Fusión'}")
    pausar()


# ─────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ─────────────────────────────────────────────

MENU = """
  ┌─────────────────────────────────────┐
  │        🏪  GESTIÓN DE INVENTARIO    │
  ├──────────────────┬──────────────────┤
  │  [1] Agregar     │  [2] Mostrar     │
  │  [3] Buscar      │  [4] Actualizar  │
  │  [5] Eliminar    │  [6] Estadísticas│
  │  [7] Guardar CSV │  [8] Cargar CSV  │
  ├──────────────────┴──────────────────┤
  │          [9] Salir                  │
  └─────────────────────────────────────┘
"""

OPCIONES = {
    "1": menu_agregar,
    "2": menu_mostrar,
    "3": menu_buscar,
    "4": menu_actualizar,
    "5": menu_eliminar,
    "6": menu_estadisticas,
    "7": menu_guardar,
    "8": menu_cargar,
}


def ciclo_menu(inventario, activo):
    """
    Ejecuta un ciclo del menú principal de forma recursiva.

    Parámetros:
        inventario (list[dict]): Lista de productos en memoria.
        activo     (list[bool]): Lista de un elemento que actúa como flag
                                 mutable; activo[0] = False detiene la recursión.

    Retorna:
        None
    """
    if not activo[0]:
        # Flag apagado → detener la recursión (condición de salida)
        return

    limpiar()
    print(MENU)
    print(f"  Productos en inventario: {len(inventario)}")
    separador()
    opcion = input("  Elige una opción (1-9) : ").strip()

    if opcion == "9":
        limpiar()
        print("\n  👋  ¡Hasta pronto! Recuerda guardar antes de salir.\n")
        activo[0] = False          # apaga el flag → próxima llamada no se ejecuta
    elif opcion in OPCIONES:
        limpiar()
        try:
            OPCIONES[opcion](inventario)
        except Exception as e:
            # Captura cualquier error inesperado sin cerrar el programa
            print(f"\n  ❌  Error inesperado: {e}")
            pausar()
    else:
        print("  ⚠️  Opción inválida. Elige un número del 1 al 9.")
        pausar()

    # Llamada recursiva: continúa el ciclo mientras activo[0] sea True
    ciclo_menu(inventario, activo)


def main():
    """Punto de entrada: inicializa el inventario y arranca el ciclo de menú."""
    inventario = []        # Estado en memoria: lista de diccionarios
    activo     = [True]    # Flag mutable en lista para compartir entre llamadas

    ciclo_menu(inventario, activo)


if __name__ == "__main__":
    main()
