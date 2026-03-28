"""
archivos.py — Módulo de persistencia CSV para el inventario.
"""

import csv
import os

ENCABEZADO = ["nombre", "precio", "cantidad"]


# ─────────────────────────────────────────────
#  GUARDAR CSV
# ─────────────────────────────────────────────

def guardar_csv(inventario, ruta, incluir_header=True):
    """
    Guarda el inventario en un archivo CSV.

    Parámetros:
        inventario     (list[dict]): Lista de productos a guardar.
        ruta           (str):        Ruta destino del archivo CSV.
        incluir_header (bool):       Si True, escribe la fila de encabezado.

    Retorna:
        bool: True si se guardó con éxito, False si hubo error.
    """
    if not inventario:
        print("  ⚠️  El inventario está vacío. No hay nada que guardar.")
        return False

    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ruta)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)

        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=ENCABEZADO)
            if incluir_header:
                escritor.writeheader()
            escritor.writerows(inventario)

        print(f"  💾  Inventario guardado en: {os.path.abspath(ruta)}")
        return True

    except PermissionError:
        print(f"  ❌  Sin permisos de escritura en: {ruta}")
    except OSError as e:
        print(f"  ❌  Error al guardar el archivo: {e}")
    except Exception as e:
        print(f"  ❌  Error inesperado al guardar: {e}")

    return False


# ─────────────────────────────────────────────
#  CARGAR CSV
# ─────────────────────────────────────────────

def cargar_csv(ruta):
    """
    Carga productos desde un archivo CSV con validaciones por fila.

    Parámetros:
        ruta (str): Ruta del archivo CSV a leer.

    Retorna:
        tuple(list[dict], int):
            - Lista de productos válidos cargados.
            - Cantidad de filas inválidas omitidas.
        Retorna (None, 0) si el archivo no pudo leerse o el encabezado es inválido.
    """
    productos = []
    filas_invalidas = 0

    try:
        with open(ruta, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            # Validar encabezado
            if lector.fieldnames != ENCABEZADO:
                print(f"  ❌  Encabezado inválido. Se esperaba: {','.join(ENCABEZADO)}")
                print(f"       Encontrado: {','.join(lector.fieldnames or [])}")
                return None, 0

            for numero, fila in enumerate(lector, start=2):  # fila 1 = encabezado
                # Verificar cantidad de columnas
                if len(fila) != 3:
                    print(f"  ⚠️  Fila {numero}: columnas incorrectas — omitida.")
                    filas_invalidas += 1
                    continue

                try:
                    nombre   = fila["nombre"].strip()
                    precio   = float(fila["precio"])
                    cantidad = int(fila["cantidad"])

                    if not nombre:
                        raise ValueError("Nombre vacío")
                    if precio < 0:
                        raise ValueError("Precio negativo")
                    if cantidad < 0:
                        raise ValueError("Cantidad negativa")

                    productos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})

                except ValueError as e:
                    print(f"  ⚠️  Fila {numero}: dato inválido ({e}) — omitida.")
                    filas_invalidas += 1

        return productos, filas_invalidas

    except FileNotFoundError:
        print(f"  ❌  Archivo no encontrado: {ruta}")
    except UnicodeDecodeError:
        print("  ❌  Error de codificación. Asegúrate de que el archivo esté en UTF-8.")
    except Exception as e:
        print(f"  ❌  Error inesperado al cargar: {e}")

    return None, 0


# ─────────────────────────────────────────────
#  FUSIÓN DE INVENTARIOS
# ─────────────────────────────────────────────

def fusionar(inventario_actual, nuevos):
    """
    Fusiona la lista 'nuevos' en 'inventario_actual'.

    Política de fusión:
      - Si el producto ya existe → suma cantidades y actualiza precio al nuevo.
      - Si no existe → lo agrega.

    Parámetros:
        inventario_actual (list[dict]): Inventario en memoria.
        nuevos            (list[dict]): Productos cargados del CSV.

    Retorna:
        tuple(int, int): (agregados, actualizados)
    """
    print("\n  📋  Política de fusión:")
    print("      • Producto existente → suma cantidad + precio actualizado al nuevo valor.")
    print("      • Producto nuevo     → se agrega directamente.\n")

    agregados    = 0
    actualizados = 0

    nombres_actuales = {p["nombre"].lower(): p for p in inventario_actual}

    for nuevo in nuevos:
        clave = nuevo["nombre"].lower()
        if clave in nombres_actuales:
            existente = nombres_actuales[clave]
            existente["cantidad"] += nuevo["cantidad"]
            existente["precio"]    = nuevo["precio"]
            actualizados += 1
        else:
            inventario_actual.append(nuevo)
            nombres_actuales[clave] = nuevo
            agregados += 1

    return agregados, actualizados
