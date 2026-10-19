import sqlite3
from decimal import Decimal, InvalidOperation


DATABASE = "cafeteria.db"
MAX_ENTERO_SQLITE = 2**63 - 1


def obtener_conexion():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tablas():
    conexion = obtener_conexion()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL,
            disponible INTEGER NOT NULL DEFAULT 1
        )
    """)

    columnas_productos = {
        columna["name"]
        for columna in conexion.execute("PRAGMA table_info(productos)").fetchall()
    }
    if "existencia" in columnas_productos:
        conexion.execute(
            "ALTER TABLE productos DROP COLUMN existencia"
        )

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero_pedido INTEGER UNIQUE,
            nombre_cliente TEXT NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            estado TEXT NOT NULL DEFAULT 'PENDIENTE DE PAGO',
            total REAL
        )
    """)

    tabla_anterior = conexion.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'table' AND name = 'detalles_pedidos'
    """).fetchone()
    tabla_actual = conexion.execute("""
        SELECT name FROM sqlite_master
        WHERE type = 'table' AND name = 'detalle_pedido'
    """).fetchone()

    if tabla_anterior is not None and tabla_actual is None:
        conexion.execute(
            "ALTER TABLE detalles_pedidos RENAME TO detalle_pedido"
        )
        conexion.execute(
            "ALTER TABLE detalle_pedido RENAME COLUMN id_pedido TO pedido_id"
        )
        conexion.execute(
            "ALTER TABLE detalle_pedido RENAME COLUMN id_producto TO producto_id"
        )

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS detalle_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            precio REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
            FOREIGN KEY (producto_id) REFERENCES productos(id)
        )
    """)

    conexion.commit()
    conexion.close()


def insertar_productos_iniciales():
    conexion = obtener_conexion()
    if conexion.execute("SELECT 1 FROM productos LIMIT 1").fetchone() is not None:
        conexion.close()
        return

    productos = [
        (
            "Tacos capeados",
            "Tacos de pescado capeados con lechuga, col y aderezo de la casa.",
            65.00,
            "Alimentos",
            1
        ),
        (
            "Burrito",
            "Burrito de tortilla de harina con frijoles, carne y queso.",
            55.00,
            "Alimentos",
            1
        ),
        (
            "Refresco",
            "Refresco frío de 600 ml. Diferentes sabores disponibles.",
            25.00,
            "Bebidas",
            1
        ),
        (
            "Agua fresca",
            "Variedad de sabores.",
            20.00,
            "Bebidas",
            1
        ),
        (
            "Café",
            "Café americano recién preparado.",
            25.00,
            "Bebidas",
            1
        ),
        (
            "Sándwich sencillo",
            "Sándwich de jamón y queso con lechuga y tomate.",
            45.00,
            "Alimentos",
            1
        ),
        (
            "Chilaquiles",
            "Totopos con salsa, crema, queso y cebolla.",
            60.00,
            "Alimentos",
            1
        ),
        (
            "Huevos revueltos",
            "Huevos revueltos acompañados de frijoles.",
            50.00,
            "Alimentos",
            1
        )
    ]

    for producto in productos:
        existe = conexion.execute(
            "SELECT 1 FROM productos WHERE nombre = ?",
            (producto[0],)
        ).fetchone()

        if existe is None:
            conexion.execute("""
                INSERT INTO productos
                (nombre, descripcion, precio, categoria, disponible)
                VALUES (?, ?, ?, ?, ?)
            """, producto)

    conexion.commit()

    conexion.close()


def obtener_productos():
    conexion = obtener_conexion()
    productos = conexion.execute("""
        SELECT id, nombre, descripcion, precio, categoria, disponible
        FROM productos
        ORDER BY categoria, nombre
    """).fetchall()
    conexion.close()
    return [dict(producto) for producto in productos]


def obtener_pedidos():
    conexion = obtener_conexion()
    filas = conexion.execute("""
        SELECT
            pedidos.id,
            pedidos.numero_pedido,
            pedidos.nombre_cliente,
            pedidos.fecha,
            pedidos.estado,
            pedidos.total,
            productos.nombre AS producto_nombre,
            detalle_pedido.cantidad,
            detalle_pedido.precio
        FROM pedidos
        LEFT JOIN detalle_pedido
            ON detalle_pedido.pedido_id = pedidos.id
        LEFT JOIN productos
            ON productos.id = detalle_pedido.producto_id
        ORDER BY pedidos.id DESC, detalle_pedido.id
    """).fetchall()
    conexion.close()

    pedidos = {}
    for fila in filas:
        pedido_id = fila["id"]
        if pedido_id not in pedidos:
            pedidos[pedido_id] = {
                "id": pedido_id,
                "numero_pedido": fila["numero_pedido"],
                "nombre_cliente": fila["nombre_cliente"],
                "fecha": fila["fecha"],
                "estado": fila["estado"],
                "total": fila["total"],
                "productos": [],
            }

        if fila["producto_nombre"] is not None:
            pedidos[pedido_id]["productos"].append({
                "nombre": fila["producto_nombre"],
                "cantidad": fila["cantidad"],
                "precio": fila["precio"],
            })

    return list(pedidos.values())


def validar_producto(datos):
    if not isinstance(datos, dict):
        raise ValueError("Los datos del producto no son válidos.")
    campos = {}
    for campo, limite in (("nombre", 100), ("categoria", 50), ("descripcion", 500)):
        valor = datos.get(campo, "")
        if not isinstance(valor, str) or len(valor.strip()) > limite:
            raise ValueError(f"El campo {campo} debe ser texto de hasta {limite} caracteres.")
        campos[campo] = valor.strip()
    if not campos["nombre"] or not campos["categoria"]:
        raise ValueError("El nombre y la categoría son obligatorios.")
    precio = datos.get("precio")
    if type(precio) not in (str, int, float):
        raise ValueError("Ingresa un precio válido.")
    try:
        precio = Decimal(str(precio))
        if not precio.is_finite() or not Decimal("0") < precio <= Decimal("999999.99"):
            raise ValueError("El precio debe ser mayor que cero y hasta $999999.99.")
        if precio != precio.quantize(Decimal("0.01")):
            raise ValueError("El precio admite como máximo dos decimales.")
    except InvalidOperation:
        raise ValueError("Ingresa un precio válido.") from None
    if type(datos.get("disponible")) is not bool:
        raise ValueError("Indica si el producto está disponible.")
    campos.update(precio=float(precio), disponible=int(datos["disponible"]))
    return campos


def guardar_producto(datos, producto_id=None):
    producto = validar_producto(datos)
    conexion = obtener_conexion()
    try:
        with conexion:
            valores = (producto["nombre"], producto["descripcion"], producto["precio"],
                       producto["categoria"], producto["disponible"])
            if producto_id is None:
                cursor = conexion.execute("""
                    INSERT INTO productos (nombre, descripcion, precio, categoria, disponible)
                    VALUES (?, ?, ?, ?, ?)
                """, valores)
                producto_id = cursor.lastrowid
            else:
                if type(producto_id) is not int or not 0 < producto_id <= MAX_ENTERO_SQLITE:
                    raise ValueError("El producto no es válido.")
                cursor = conexion.execute("""
                    UPDATE productos SET nombre = ?, descripcion = ?, precio = ?,
                        categoria = ?, disponible = ? WHERE id = ?
                """, valores + (producto_id,))
                if cursor.rowcount == 0:
                    raise LookupError("No se encontró el producto.")
        return {"id": producto_id, **producto}
    finally:
        conexion.close()


def cambiar_disponibilidad(producto_id, disponible):
    if type(producto_id) is not int or not 0 < producto_id <= MAX_ENTERO_SQLITE:
        raise ValueError("El producto no es válido.")
    if type(disponible) is not bool:
        raise ValueError("La disponibilidad debe ser sí o no.")
    conexion = obtener_conexion()
    try:
        with conexion:
            cursor = conexion.execute(
                "UPDATE productos SET disponible = ? WHERE id = ?",
                (int(disponible), producto_id),
            )
            if cursor.rowcount == 0:
                raise LookupError("No se encontró el producto.")
        return {"id": producto_id, "disponible": disponible}
    finally:
        conexion.close()


def crear_pedido(nombre_cliente, productos):
    if not isinstance(nombre_cliente, str) or not nombre_cliente.strip():
        raise ValueError("Ingresa un nombre para el pedido.")
    if not isinstance(productos, list) or not productos:
        raise ValueError("El pedido debe incluir al menos un producto.")

    cantidades = {}
    for item in productos:
        if not isinstance(item, dict):
            raise ValueError("Los productos del pedido no son válidos.")
        producto_id = item.get("id")
        cantidad = item.get("cantidad")
        if (type(producto_id) is not int or not 0 < producto_id <= MAX_ENTERO_SQLITE
                or type(cantidad) is not int or not 0 < cantidad <= MAX_ENTERO_SQLITE):
            raise ValueError("Cada producto necesita un id y una cantidad positiva.")
        cantidades[producto_id] = cantidades.get(producto_id, 0) + cantidad
        if cantidades[producto_id] > MAX_ENTERO_SQLITE:
            raise ValueError("La cantidad solicitada no es válida.")

    conexion = obtener_conexion()
    try:
        with conexion:
            conexion.execute("BEGIN IMMEDIATE")
            detalles = []
            total = Decimal("0.00")

            for producto_id, cantidad in cantidades.items():
                producto = conexion.execute("""
                    SELECT precio FROM productos
                    WHERE id = ? AND disponible = 1
                """, (producto_id,)).fetchone()
                if producto is None:
                    raise ValueError(f"El producto {producto_id} no está disponible.")

                precio = Decimal(str(producto["precio"])).quantize(Decimal("0.01"))
                total += precio * cantidad
                detalles.append((producto_id, cantidad, float(precio)))

            estado = "PENDIENTE DE PAGO"
            cursor = conexion.execute("""
                INSERT INTO pedidos (nombre_cliente, estado, total)
                VALUES (?, ?, ?)
            """, (nombre_cliente.strip(), estado, float(total)))
            numero_pedido = cursor.lastrowid
            conexion.execute("""
                UPDATE pedidos SET numero_pedido = ? WHERE id = ?
            """, (numero_pedido, numero_pedido))

            conexion.executemany("""
                INSERT INTO detalle_pedido
                    (pedido_id, producto_id, cantidad, precio)
                VALUES (?, ?, ?, ?)
            """, [
                (numero_pedido, producto_id, cantidad, precio)
                for producto_id, cantidad, precio in detalles
            ])

        return {
            "numero_pedido": numero_pedido,
            "estado": estado,
            "total": float(total),
        }
    finally:
        conexion.close()


def cambiar_estado_en_caja(numero_pedido, estado):
    if type(numero_pedido) is not int or not 0 < numero_pedido <= MAX_ENTERO_SQLITE:
        raise ValueError("El número de pedido no es válido.")
    if estado not in ("PAGADO", "CANCELADO"):
        raise ValueError("La acción de caja no es válida.")

    conexion = obtener_conexion()
    try:
        with conexion:
            cursor = conexion.execute("""
                UPDATE pedidos SET estado = ?
                WHERE numero_pedido = ? AND estado = 'PENDIENTE DE PAGO'
            """, (estado, numero_pedido))
            if cursor.rowcount == 0:
                pedido = conexion.execute(
                    "SELECT estado FROM pedidos WHERE numero_pedido = ?",
                    (numero_pedido,),
                ).fetchone()
                if pedido is None:
                    raise LookupError("No se encontró el pedido.")
                raise ValueError(
                    "El pedido ya no está pendiente de pago. Actualiza la lista."
                )
        return {"numero_pedido": numero_pedido, "estado": estado}
    finally:
        conexion.close()


def obtener_pedidos_cocina():
    estados_activos = ("PAGADO", "EN PREPARACIÓN", "LISTO")
    return [
        pedido for pedido in reversed(obtener_pedidos())
        if pedido["estado"] in estados_activos
    ]


def cambiar_estado_en_cocina(numero_pedido, estado):
    if type(numero_pedido) is not int or not 0 < numero_pedido <= MAX_ENTERO_SQLITE:
        raise ValueError("El número de pedido no es válido.")
    anteriores = {
        "EN PREPARACIÓN": "PAGADO",
        "LISTO": "EN PREPARACIÓN",
        "ENTREGADO": "LISTO",
    }
    if not isinstance(estado, str) or estado not in anteriores:
        raise ValueError("La acción de cocina no es válida.")

    conexion = obtener_conexion()
    try:
        with conexion:
            cursor = conexion.execute("""
                UPDATE pedidos SET estado = ?
                WHERE numero_pedido = ? AND estado = ?
            """, (estado, numero_pedido, anteriores[estado]))
            if cursor.rowcount == 0:
                pedido = conexion.execute(
                    "SELECT estado FROM pedidos WHERE numero_pedido = ?",
                    (numero_pedido,),
                ).fetchone()
                if pedido is None:
                    raise LookupError("No se encontró el pedido.")
                raise ValueError(
                    "El pedido no puede avanzar a ese estado. Actualiza la lista."
                )
        return {"numero_pedido": numero_pedido, "estado": estado}
    finally:
        conexion.close()
