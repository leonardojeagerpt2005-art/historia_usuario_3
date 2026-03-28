"""
app.py — Punto de entrada del sistema de inventario.
Ejecutar: python app.py
"""

import os
from servicios import (
    agregar_producto, mostrar_inventario, buscar_producto,
    actualizar_producto, eliminar_producto, mostrar_estadisticas,
)
from archivos import guardar_csv, cargar_csv, fusionar

# ─── Utilidades ───────────────────────────────────────────────────────────────

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    input("\n  Presiona ENTER para continuar...")

def titulo(texto):
    borde = "═" * 44
    print(f"\n{borde}\n  {texto}\n{borde}")

def pedir_float(msg, minimo=0.0):
    """Pide un float >= minimo; se llama recursivamente si el dato es invalido."""
    try:
        v = float(input(msg))
        if v >= minimo:
            return v
        print(f"  ⚠️  Debe ser >= {minimo}.")
    except ValueError:
        print("  ⚠️  Ingresa un numero valido (ej. 12.50).")
    return pedir_float(msg, minimo)

def pedir_int(msg, minimo=0):
    """Pide un int >= minimo; se llama recursivamente si el dato es invalido."""
    try:
        v = int(input(msg))
        if v >= minimo:
            return v
        print(f"  ⚠️  Debe ser >= {minimo}.")
    except ValueError:
        print("  ⚠️  Ingresa un numero entero valido.")
    return pedir_int(msg, minimo)

def pedir_ruta(msg):
    """Pide una ruta CSV; usa 'inventario.csv' si se deja en blanco."""
    ruta = input(msg).strip() or "inventario.csv"
    return ruta if ruta.endswith(".csv") else ruta + ".csv"

# ─── Acciones del menu ────────────────────────────────────────────────────────

def op_agregar(inv):
    titulo("AGREGAR PRODUCTO")
    nombre = input("  Nombre : ").strip()
    if not nombre:
        print("  ⚠️  El nombre no puede estar vacio.")
    else:
        print(agregar_producto(inv, nombre,
                               pedir_float("  Precio   : $"),
                               pedir_int  ("  Cantidad : ")))
    pausar()

def op_mostrar(inv):
    titulo("INVENTARIO ACTUAL")
    mostrar_inventario(inv)
    pausar()

def op_buscar(inv):
    titulo("BUSCAR PRODUCTO")
    p = buscar_producto(inv, input("  Nombre a buscar : ").strip())
    if p:
        print(f"\n  Nombre   : {p['nombre']}")
        print(f"  Precio   : ${p['precio']:.2f}")
        print(f"  Cantidad : {p['cantidad']} uds")
        print(f"  Subtotal : ${p['precio'] * p['cantidad']:.2f}")
    else:
        print("  ⚠️  Producto no encontrado.")
    pausar()

def op_actualizar(inv):
    titulo("ACTUALIZAR PRODUCTO")
    nombre = input("  Nombre : ").strip()
    if not buscar_producto(inv, nombre):
        print("  ⚠️  Producto no encontrado.")
        pausar()
        return
    print("  [1] Precio  [2] Cantidad  [3] Ambos")
    op = input("  Opcion : ").strip()
    precio   = pedir_float("  Nuevo precio    : $") if op in ("1","3") else None
    cantidad = pedir_int  ("  Nueva cantidad  : ")  if op in ("2","3") else None
    if op not in ("1","2","3"):
        print("  ⚠️  Opcion invalida.")
    else:
        print(actualizar_producto(inv, nombre, precio, cantidad))
    pausar()

def op_eliminar(inv):
    titulo("ELIMINAR PRODUCTO")
    nombre = input("  Nombre a eliminar : ").strip()
    if not buscar_producto(inv, nombre):
        print("  ⚠️  Producto no encontrado.")
    elif input(f"  Eliminar '{nombre}'? (S/N) : ").strip().upper() == "S":
        print(eliminar_producto(inv, nombre))
    else:
        print("  Cancelado.")
    pausar()

def op_estadisticas(inv):
    titulo("ESTADISTICAS")
    mostrar_estadisticas(inv)
    pausar()

def op_guardar(inv):
    titulo("GUARDAR CSV")
    guardar_csv(inv, pedir_ruta("  Ruta [inventario.csv] : "))
    pausar()

def op_cargar(inv):
    titulo("CARGAR CSV")
    nuevos, invalidas = cargar_csv(pedir_ruta("  Ruta [inventario.csv] : "))
    if nuevos is None or not nuevos:
        print("  ⚠️  No hay datos validos para cargar.")
        pausar()
        return
    print(f"\n  {len(nuevos)} producto(s) leidos | {invalidas} fila(s) invalida(s) omitida(s).")
    if input("  Sobrescribir inventario? (S/N) : ").strip().upper() == "S":
        inv.clear()
        inv.extend(nuevos)
        print(f"  Inventario reemplazado con {len(nuevos)} producto(s).")
    else:
        ag, ac = fusionar(inv, nuevos)
        print(f"  Fusion: {ag} agregado(s), {ac} actualizado(s).")
    pausar()

# ─── Menu principal ───────────────────────────────────────────────────────────

MENU = """
  +--------------------------------------+
  |      GESTION DE INVENTARIO           |
  +------------------+-------------------+
  |  [1] Agregar     |  [2] Mostrar      |
  |  [3] Buscar      |  [4] Actualizar   |
  |  [5] Eliminar    |  [6] Estadisticas |
  |  [7] Guardar CSV |  [8] Cargar CSV   |
  +------------------+-------------------+
  |            [9] Salir                 |
  +--------------------------------------+"""

OPCIONES = {
    "1": op_agregar,    "2": op_mostrar,
    "3": op_buscar,     "4": op_actualizar,
    "5": op_eliminar,   "6": op_estadisticas,
    "7": op_guardar,    "8": op_cargar,
}

def ciclo_menu(inv, activo):
    """Ejecuta el menu recursivamente mientras activo[0] sea True."""
    if not activo[0]:
        return
    limpiar()
    print(MENU)
    print(f"\n  Productos en inventario: {len(inv)}")
    print("-" * 44)
    opcion = input("  Elige una opcion (1-9) : ").strip()
    if opcion == "9":
        limpiar()
        print("\n  Hasta pronto!\n")
        activo[0] = False
    elif opcion in OPCIONES:
        limpiar()
        try:
            OPCIONES[opcion](inv)
        except Exception as e:
            print(f"\n  Error inesperado: {e}")
            pausar()
    else:
        print("  ⚠️  Opcion invalida. Elige entre 1 y 9.")
        pausar()
    ciclo_menu(inv, activo)

def main():
    """Inicializa el inventario y arranca el ciclo de menu."""
    ciclo_menu([], [True])

if __name__ == "__main__":
    main()
