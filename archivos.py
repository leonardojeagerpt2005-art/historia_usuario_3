"""
archivos.py — CSV persistence module for the inventory system.
"""

import csv
import os

# CSV header structure (expected column names)
ENCABEZADO = ["nombre", "precio", "cantidad"]


# ─────────────────────────────────────────────
#  SAVE CSV
# ─────────────────────────────────────────────

def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Saves the inventory to a CSV file.

    Parameters:
        inventario     (list[dict]): List of products to save.
        ruta           (str):        Destination file path.
        incluir_header (bool):       If True, writes the header row.

    Returns:
        bool: True if saved successfully, False otherwise.
    """
    # Check if inventory is empty
    if not inventario:
        print("  ⚠️  Inventory is empty. Nothing to save.")
        return False

    try:
        # Create directory if it does not exist
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        # Open file in write mode with UTF-8 encoding
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=ENCABEZADO)

            # Write header if required
            if incluir_header:
                escritor.writeheader()

            # Write all product rows
            escritor.writerows(inventario)

        print(f"  💾  Inventory saved at: {os.path.abspath(ruta)}")
        return True

    except PermissionError:
        # Error if the program lacks write permissions
        print(f"  ❌  No write permission for: {ruta}")
    except OSError as e:
        # General OS-related error
        print(f"  ❌  Error saving file: {e}")
    except Exception as e:
        # Catch any unexpected error
        print(f"  ❌  Unexpected error while saving: {e}")

    return False


# ─────────────────────────────────────────────
#  LOAD CSV
# ─────────────────────────────────────────────

def cargar_csv(ruta):
    """
    Loads products from a CSV file with row-level validation.

    Parameters:
        ruta (str): Path to the CSV file.

    Returns:
        tuple(list[dict], int):
            - List of valid products loaded.
            - Number of invalid rows skipped.
        Returns (None, 0) if the file cannot be read or header is invalid.
    """
    productos = []
    filas_invalidas = 0

    try:
        # Open file in read mode
        with open(ruta, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            # Validate header structure
            if lector.fieldnames != ENCABEZADO:
                print(f"  ❌  Invalid header. Expected: {','.join(ENCABEZADO)}")
                print(f"       Found: {','.join(lector.fieldnames or [])}")
                return None, 0

            # Iterate through each row (starting from line 2)
            for numero, fila in enumerate(lector, start=2):

                # Validate number of columns
                if len(fila) != 3:
                    print(f"  ⚠️  Row {numero}: incorrect columns — skipped.")
                    filas_invalidas += 1
                    continue

                try:
                    # Extract and convert values
                    nombre   = fila["nombre"].strip()
                    precio   = float(fila["precio"])
                    cantidad = int(fila["cantidad"])

                    # Validate data rules
                    if not nombre:
                        raise ValueError("Empty name")
                    if precio < 0:
                        raise ValueError("Negative price")
                    if cantidad < 0:
                        raise ValueError("Negative quantity")

                    # Add valid product to list
                    productos.append({
                        "nombre": nombre,
                        "precio": precio,
                        "cantidad": cantidad
                    })

                except ValueError as e:
                    # Handle invalid data in row
                    print(f"  ⚠️  Row {numero}: invalid data ({e}) — skipped.")
                    filas_invalidas += 1

        return productos, filas_invalidas

    except FileNotFoundError:
        # File does not exist
        print(f"  ❌  File not found: {ruta}")
    except UnicodeDecodeError:
        # Encoding error (not UTF-8)
        print("  ❌  Encoding error. Make sure the file is UTF-8.")
    except Exception as e:
        # Catch any unexpected error
        print(f"  ❌  Unexpected error while loading: {e}")

    return None, 0


# ─────────────────────────────────────────────
#  INVENTORY MERGE
# ─────────────────────────────────────────────

def fusionar(inventario_actual, nuevos):
    """
    Merges 'nuevos' products into 'inventario_actual'.

    Merge policy:
      - If product exists → add quantities and update price to the new value.
      - If product does not exist → add it.

    Parameters:
        inventario_actual (list[dict]): Current in-memory inventory.
        nuevos            (list[dict]): Products loaded from CSV.

    Returns:
        tuple(int, int): (added, updated)
    """
    print("\n  📋  Merge policy:")
    print("      • Existing product → add quantity + update price.")
    print("      • New product      → added directly.\n")

    agregados    = 0
    actualizados = 0

    # Create a dictionary for fast lookup (case-insensitive)
    nombres_actuales = {
        p["nombre"].lower(): p for p in inventario_actual
    }

    # Iterate through new products
    for nuevo in nuevos:
        clave = nuevo["nombre"].lower()

        if clave in nombres_actuales:
            # Update existing product
            existente = nombres_actuales[clave]
            existente["cantidad"] += nuevo["cantidad"]
            existente["precio"]    = nuevo["precio"]
            actualizados += 1
        else:
            # Add new product
            inventario_actual.append(nuevo)
            nombres_actuales[clave] = nuevo
            agregados += 1

    return agregados, actualizados
