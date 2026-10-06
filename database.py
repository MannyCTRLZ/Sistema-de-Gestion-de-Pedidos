import sqlite3
from decimal import Decimal


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
