# 📦 Sistema de Gestión de Inventario

Sistema de inventario por consola desarrollado en Python. Permite realizar operaciones CRUD sobre productos, calcular estadísticas del negocio y persistir los datos en archivos CSV entre sesiones.

---

## 🗂️ Estructura del proyecto

```
inventario/
├── app.py          # Punto de entrada: menú principal e interfaz de usuario
├── servicios.py    # Operaciones CRUD y estadísticas
├── archivos.py     # Lectura y escritura de archivos CSV
└── README.md
```

---

## ▶️ Cómo ejecutar

Requiere **Python 3.8 o superior**. No necesita librerías externas.

```bash
python app.py
```

---

## 🧭 Menú principal

Al ejecutar el programa se muestra este menú:

```
  +--------------------------------------+
  |      GESTION DE INVENTARIO           |
  +------------------+-------------------+
  |  [1] Agregar     |  [2] Mostrar      |
  |  [3] Buscar      |  [4] Actualizar   |
  |  [5] Eliminar    |  [6] Estadisticas |
  |  [7] Guardar CSV |  [8] Cargar CSV   |
  +------------------+-------------------+
  |            [9] Salir                 |
  +--------------------------------------+
```

---

## ⚙️ Funcionalidades

### [1] Agregar producto
Solicita nombre, precio y cantidad. Si el producto ya existe, suma la cantidad y actualiza el precio al nuevo valor.

### [2] Mostrar inventario
Imprime todos los productos en formato tabular con nombre, precio y stock.

### [3] Buscar producto
Busca por nombre (sin distinguir mayúsculas). Si lo encuentra, muestra nombre, precio, cantidad y subtotal.

### [4] Actualizar producto
Permite modificar el precio, la cantidad, o ambos de un producto existente.

### [5] Eliminar producto
Solicita confirmación antes de eliminar un producto del inventario.

### [6] Estadísticas
Muestra un resumen del inventario con:
- Número de productos distintos
- Unidades totales en stock
- Valor total del inventario (`precio × cantidad`)
- Producto más caro
- Producto con mayor stock

### [7] Guardar CSV
Exporta el inventario a un archivo `.csv` con el encabezado `nombre,precio,cantidad`. Si no se ingresa ruta, usa `inventario.csv` por defecto.

### [8] Cargar CSV
Importa productos desde un archivo `.csv`. Al cargar, el programa pregunta si se desea **sobrescribir** el inventario actual o **fusionar**:

| Acción | Comportamiento |
|--------|----------------|
| **Sobrescribir (S)** | Reemplaza todo el inventario con los datos del CSV |
| **Fusionar (N)** | Productos nuevos se agregan; los existentes suman cantidad y actualizan precio |

Al finalizar muestra un resumen: productos cargados, filas inválidas omitidas y acción realizada.

---

## 📄 Formato del archivo CSV

```
nombre,precio,cantidad
Manzana,1.50,100
Leche,2.30,50
Pan,0.80,200
```

Reglas de validación al cargar:
- El encabezado debe ser exactamente `nombre,precio,cantidad`
- Cada fila debe tener exactamente 3 columnas
- `precio` debe ser un número decimal no negativo
- `cantidad` debe ser un número entero no negativo
- Las filas inválidas se omiten y se informa cuántas fueron

---

## 🗃️ Módulos

### `app.py`
Punto de entrada del programa. Contiene el menú principal, las funciones de interfaz (`titulo`, `pausar`, `pedir_float`, `pedir_int`, `pedir_ruta`) y las acciones de cada opción. El ciclo del menú se implementa de forma **recursiva** mediante `ciclo_menu()`, sin usar `while`.

### `servicios.py`

| Función | Descripción |
|---------|-------------|
| `agregar_producto(inv, nombre, precio, cantidad)` | Agrega o actualiza un producto |
| `mostrar_inventario(inv)` | Imprime la tabla de productos |
| `buscar_producto(inv, nombre)` | Retorna el dict del producto o `None` |
| `actualizar_producto(inv, nombre, nuevo_precio, nueva_cantidad)` | Modifica precio y/o cantidad |
| `eliminar_producto(inv, nombre)` | Elimina un producto de la lista |
| `calcular_estadisticas(inv)` | Retorna dict con métricas del inventario |
| `mostrar_estadisticas(inv)` | Imprime las métricas con formato |

### `archivos.py`

| Función | Descripción |
|---------|-------------|
| `guardar_csv(inv, ruta, incluir_header)` | Escribe el inventario en un CSV |
| `cargar_csv(ruta)` | Lee y valida un CSV; retorna `(productos, filas_invalidas)` |
| `fusionar(inventario_actual, nuevos)` | Combina dos listas de productos según la política definida |

---

## 🛡️ Manejo de errores

El programa nunca se cierra por un error del usuario. Todos los casos están cubiertos:

- Opción de menú fuera de rango → mensaje y regresa al menú
- Precio o cantidad no numérico → se vuelve a pedir (recursivo)
- Producto no encontrado → mensaje informativo
- CSV no encontrado → `FileNotFoundError` capturado, regresa al menú
- CSV con encabezado incorrecto → se informa y se cancela la carga
- Filas con datos inválidos → se omiten y se cuenta el total
- Error de permisos al guardar → se informa sin cerrar el programa
- Error de codificación (`UnicodeDecodeError`) → mensaje claro al usuario

---

## 🧱 Estructura de datos

El inventario se mantiene en memoria como una **lista de diccionarios**:

```python
inventario = [
    {"nombre": "Manzana", "precio": 1.50, "cantidad": 100},
    {"nombre": "Leche",   "precio": 2.30, "cantidad": 50},
]
```

---

## 👤 Autor

Proyecto académico — Programación en Python  
Módulo: Colecciones, Modularización y Persistencia en Archivos
