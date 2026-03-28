"""
app.py — Entry point of the inventory system.
Run with: python app.py
"""

import os
# Import core inventory services (business logic)
from servicios import (
    agregar_producto, mostrar_inventario, buscar_producto,
    actualizar_producto, eliminar_producto, mostrar_estadisticas,
)
# Import file handling utilities (CSV persistence)
from archivos import guardar_csv, cargar_csv, fusionar

# ─── Utility Functions ────────────────────────────────────────────────────────

def limpiar():
    """Clears the console screen depending on the OS."""
    os.system("cls" if os.name == "nt" else "clear")

def pausar():
    """Pauses execution until the user presses ENTER."""
    input("\n  Press ENTER to continue...")

def titulo(texto):
    """Prints a formatted title with a decorative border."""
    borde = "═" * 44
    print(f"\n{borde}\n  {texto}\n{borde}")

def pedir_float(msg, minimo=0.0):
    """
    Prompts the user for a float value >= minimum.
    Uses recursion if the input is invalid.
    """
    try:
        v = float(input(msg))
        if v >= minimo:
            return v
        print(f"  ⚠️  Must be >= {minimo}.")
    except ValueError:
        print("  ⚠️  Enter a valid number (e.g. 12.50).")
    return pedir_float(msg, minimo)

def pedir_int(msg, minimo=0):
    """
    Prompts the user for an integer >= minimum.
    Uses recursion if the input is invalid.
    """
    try:
        v = int(input(msg))
        if v >= minimo:
            return v
        print(f"  ⚠️  Must be >= {minimo}.")
    except ValueError:
        print("  ⚠️  Enter a valid integer.")
    return pedir_int(msg, minimo)

def pedir_ruta(msg):
    """
    Prompts for a CSV file path.
    Defaults to 'inventario.csv' if empty input is given.
    Ensures the file has a .csv extension.
    """
    ruta = input(msg).strip() or "inventario.csv"
    return ruta if ruta.endswith(".csv") else ruta + ".csv"

# ─── Menu Actions ─────────────────────────────────────────────────────────────

def op_agregar(inv):
    """Handles adding a new product to the inventory."""
    titulo("ADD PRODUCT")
    nombre = input("  Name : ").strip()
    if not nombre:
        print("  ⚠️  Name cannot be empty.")
    else:
        print(agregar_producto(inv, nombre,
                               pedir_float("  Price   : $"),
                               pedir_int  ("  Quantity: ")))
    pausar()

def op_mostrar(inv):
    """Displays all products in the inventory."""
    titulo("CURRENT INVENTORY")
    mostrar_inventario(inv)
    pausar()

def op_buscar(inv):
    """Searches for a product by name."""
    titulo("SEARCH PRODUCT")
    p = buscar_producto(inv, input("  Name to search : ").strip())
    if p:
        # Display product details
        print(f"\n  Name     : {p['nombre']}")
        print(f"  Price    : ${p['precio']:.2f}")
        print(f"  Quantity : {p['cantidad']} units")
        print(f"  Subtotal : ${p['precio'] * p['cantidad']:.2f}")
    else:
        print("  ⚠️  Product not found.")
    pausar()

def op_actualizar(inv):
    """Updates price and/or quantity of an existing product."""
    titulo("UPDATE PRODUCT")
    nombre = input("  Name : ").strip()
    
    # Check if product exists
    if not buscar_producto(inv, nombre):
        print("  ⚠️  Product not found.")
        pausar()
        return

    print("  [1] Price  [2] Quantity  [3] Both")
    op = input("  Option : ").strip()

    # Conditional updates based on user choice
    precio   = pedir_float("  New price    : $") if op in ("1","3") else None
    cantidad = pedir_int  ("  New quantity : ")  if op in ("2","3") else None

    if op not in ("1","2","3"):
        print("  ⚠️  Invalid option.")
    else:
        print(actualizar_producto(inv, nombre, precio, cantidad))
    pausar()

def op_eliminar(inv):
    """Deletes a product from the inventory."""
    titulo("DELETE PRODUCT")
    nombre = input("  Name to delete : ").strip()

    if not buscar_producto(inv, nombre):
        print("  ⚠️  Product not found.")
    elif input(f"  Delete '{nombre}'? (Y/N) : ").strip().upper() == "S":
        print(eliminar_producto(inv, nombre))
    else:
        print("  Cancelled.")
    pausar()

def op_estadisticas(inv):
    """Displays inventory statistics (totals, etc.)."""
    titulo("STATISTICS")
    mostrar_estadisticas(inv)
    pausar()

def op_guardar(inv):
    """Saves the inventory to a CSV file."""
    titulo("SAVE CSV")
    guardar_csv(inv, pedir_ruta("  Path [inventario.csv] : "))
    pausar()

def op_cargar(inv):
    """Loads inventory data from a CSV file."""
    titulo("LOAD CSV")
    nuevos, invalidas = cargar_csv(pedir_ruta("  Path [inventario.csv] : "))

    if nuevos is None or not nuevos:
        print("  ⚠️  No valid data to load.")
        pausar()
        return

    print(f"\n  {len(nuevos)} product(s) read | {invalidas} invalid row(s) skipped.")

    # Ask user whether to overwrite or merge data
    if input("  Overwrite inventory? (Y/N) : ").strip().upper() == "S":
        inv.clear()
        inv.extend(nuevos)
        print(f"  Inventory replaced with {len(nuevos)} product(s).")
    else:
        ag, ac = fusionar(inv, nuevos)
        print(f"  Merge: {ag} added, {ac} updated.")
    pausar()

# ─── Main Menu ────────────────────────────────────────────────────────────────

MENU = """
  +--------------------------------------+
  |         INVENTORY MANAGEMENT         |
  +------------------+-------------------+
  |  [1] Add         |  [2] Show         |
  |  [3] Search      |  [4] Update       |
  |  [5] Delete      |  [6] Statistics   |
  |  [7] Save CSV    |  [8] Load CSV     |
  +------------------+-------------------+
  |            [9] Exit                  |
  +--------------------------------------+"""

# Map menu options to their corresponding functions
OPCIONES = {
    "1": op_agregar,    "2": op_mostrar,
    "3": op_buscar,     "4": op_actualizar,
    "5": op_eliminar,   "6": op_estadisticas,
    "7": op_guardar,    "8": op_cargar,
}

def ciclo_menu(inv, activo):
    """
    Recursively runs the menu while 'activo[0]' is True.
    Uses a list to allow mutability (pass-by-reference behavior).
    """
    if not activo[0]:
        return

    limpiar()
    print(MENU)
    print(f"\n  Products in inventory: {len(inv)}")
    print("-" * 44)

    opcion = input("  Choose an option (1-9) : ").strip()

    if opcion == "9":
        limpiar()
        print("\n  Goodbye!\n")
        activo[0] = False

    elif opcion in OPCIONES:
        limpiar()
        try:
            # Execute selected option
            OPCIONES[opcion](inv)
        except Exception as e:
            print(f"\n  Unexpected error: {e}")
            pausar()
    else:
        print("  ⚠️  Invalid option. Choose between 1 and 9.")
        pausar()

    # Recursive call to keep menu running
    ciclo_menu(inv, activo)

def main():
    """Initializes the inventory and starts the menu loop."""
    ciclo_menu([], [True])

# Entry point check
if __name__ == "__main__":
    main()
