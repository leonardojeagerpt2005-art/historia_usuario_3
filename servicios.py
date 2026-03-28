"""
servicios.py — Module for CRUD operations and inventory statistics.
"""

# ─────────────────────────────────────────────
#  CRUD OPERATIONS
# ─────────────────────────────────────────────

def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Adds a product to the inventory or updates quantity if it already exists.

    Parameters:
        inventario (list[dict]): In-memory list of products.
        nombre     (str):        Product name (case-insensitive).
        precio     (float):      Unit price (≥ 0).
        cantidad   (int):        Quantity to add (≥ 0).

    Returns:
        str: Result message ('added' or 'updated').
    """
    # Clean input (remove leading/trailing spaces)
    nombre = nombre.strip()

    # Check if product already exists
    existente = buscar_producto(inventario, nombre)

    if existente:
        # Update quantity and overwrite price with latest value
        existente["cantidad"] += cantidad
        existente["precio"] = precio
        return f"✅ '{nombre}' already existed — quantity updated and price adjusted."

    # Add new product if it does not exist
    inventario.append({
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad
    })
    return f"✅ Product '{nombre}' added to inventory."


def mostrar_inventario(inventario):
    """
    Displays all products in a formatted table.

    Parameters:
        inventario (list[dict]): List of products.

    Returns:
        None
    """
    # Check if inventory is empty
    if not inventario:
        print("\n  📭  Inventory is empty.\n")
        return

    ancho = 42

    # Table header
    print("\n" + "─" * ancho)
    print(f"  {'PRODUCT':<20} {'PRICE':>8} {'STOCK':>6}")
    print("─" * ancho)

    # Print each product
    for p in inventario:
        # Lambda used to calculate subtotal (optional use)
        subtotal = (lambda x: x["precio"] * x["cantidad"])(p)

        print(f"  {p['nombre']:<20} ${p['precio']:>7.2f} {p['cantidad']:>6} units")

    print("─" * ancho)
    print(f"  {len(inventario)} product(s) in inventory.\n")


def buscar_producto(inventario, nombre):
    """
    Searches for a product by name (case-insensitive).

    Parameters:
        inventario (list[dict]): List of products.
        nombre     (str):        Name to search.

    Returns:
        dict | None: Found product or None if not found.
    """
    nombre = nombre.strip().lower()

    # Linear search through inventory
    for p in inventario:
        if p["nombre"].lower() == nombre:
            return p

    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Updates price and/or quantity of an existing product.

    Parameters:
        inventario      (list[dict]): List of products.
        nombre          (str):        Product name to update.
        nuevo_precio    (float|None): New price (None = no change).
        nueva_cantidad  (int|None):   New quantity (None = no change).

    Returns:
        str: Result message.
    """
    # Find product
    producto = buscar_producto(inventario, nombre)

    if not producto:
        return f"⚠️  Product '{nombre}' not found."

    # Update fields only if provided
    if nuevo_precio is not None:
        producto["precio"] = nuevo_precio

    if nueva_cantidad is not None:
        producto["cantidad"] = nueva_cantidad

    return f"✅ '{nombre}' updated successfully."


def eliminar_producto(inventario, nombre):
    """
    Removes a product from the inventory.

    Parameters:
        inventario (list[dict]): List of products.
        nombre     (str):        Product name to delete.

    Returns:
        str: Result message.
    """
    # Find product
    producto = buscar_producto(inventario, nombre)

    if not producto:
        return f"⚠️  Product '{nombre}' not found."

    # Remove product from list
    inventario.remove(producto)

    return f"🗑️  '{nombre}' removed from inventory."


# ─────────────────────────────────────────────
#  STATISTICS
# ─────────────────────────────────────────────

def calcular_estadisticas(inventario):
    """
    Calculates general inventory metrics.

    Parameters:
        inventario (list[dict]): List of products.

    Returns:
        dict with keys:
            unidades_totales     (int)
            valor_total          (float)
            producto_mas_caro    (dict)
            producto_mayor_stock (dict)
        or None if inventory is empty.
    """
    if not inventario:
        return None

    # Lambda function to calculate subtotal
    subtotal = lambda p: p["precio"] * p["cantidad"]

    # Compute metrics
    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)

    # Find max values using key functions
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock,
    }


def mostrar_estadisticas(inventario):
    """
    Displays inventory statistics in a readable format.

    Parameters:
        inventario (list[dict]): List of products.

    Returns:
        None
    """
    stats = calcular_estadisticas(inventario)

    # Check if there is data
    if not stats:
        print("\n  📭  No data available for statistics.\n")
        return

    ancho = 42

    # Header
    print("\n" + "═" * ancho)
    print("  📊  INVENTORY STATISTICS")
    print("═" * ancho)

    # Print statistics
    print(f"  Distinct products : {len(inventario)}")
    print(f"  Total units       : {stats['unidades_totales']}")
    print(f"  Total value       : ${stats['valor_total']:,.2f}")

    print(f"  Most expensive    : {stats['producto_mas_caro']['nombre']}"
          f" (${stats['producto_mas_caro']['precio']:.2f})")

    print(f"  Highest stock     : {stats['producto_mayor_stock']['nombre']}"
          f" ({stats['producto_mayor_stock']['cantidad']} units)")

    print("═" * ancho + "\n")