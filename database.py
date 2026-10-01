import sqlite3


DATABASE = "cafeteria.db"


def obtener_conexion():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
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
            estado TEXT NOT NULL DEFAULT 'Pendiente de pago',
            total REAL
        )
    """)

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS detalles_pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pedido INTEGER NOT NULL,
            id_producto INTEGER NOT NULL,
            cantidad INTEGER NOT NULL DEFAULT 1,
            precio REAL NOT NULL,
            FOREIGN KEY (id_pedido) REFERENCES pedidos(id),
            FOREIGN KEY (id_producto) REFERENCES productos(id)
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


def obtener_productos_disponibles():
    conexion = obtener_conexion()
    productos = conexion.execute("""
        SELECT id, nombre, descripcion, precio, categoria, disponible
        FROM productos
        WHERE disponible = 1
        ORDER BY categoria, nombre
    """).fetchall()
    conexion.close()
    return [dict(producto) for producto in productos]
