import sqlite3


DATABASE = "cafeteria.db"

PRODUCTOS_PRUEBA = [
    (
        "Hamburguesa sencilla",
        "Carne, queso, lechuga, tomate y aderezo de la casa.",
        95.00,
        "Alimentos",
        1,
    ),
    (
        "Tacos capeados",
        "Camarones capeados, doble tortilla, lechuga, col y aderezo de la casa.",
        65.00,
        "Alimentos",
        1,
    ),
    (
        "Burrito",
        "Tortilla de harina con frijoles, carne y queso.",
        55.00,
        "Alimentos",
        1,
    ),
    (
        "Refresco",
        "Refresco frio de 600 ml. Diferentes sabores disponibles.",
        25.00,
        "Bebidas",
        1,
    ),
]


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

    conexion.commit()
    conexion.close()


<<<<<<< HEAD
def insertar_productos_prueba():
    conexion = obtener_conexion()
    cantidad_productos = conexion.execute(
        "SELECT COUNT(*) FROM productos"
    ).fetchone()[0]

    if cantidad_productos == 0:
        conexion.executemany(
            """
            INSERT INTO productos
                (nombre, descripcion, precio, categoria, disponible)
            VALUES (?, ?, ?, ?, ?)
            """,
            PRODUCTOS_PRUEBA,
        )
        conexion.commit()
=======
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
>>>>>>> frontend

    conexion.close()


<<<<<<< HEAD
def obtener_productos_disponibles():
    conexion = obtener_conexion()
    productos = conexion.execute(
        """
        SELECT id, nombre, descripcion, precio, categoria
        FROM productos
        WHERE disponible = 1
        ORDER BY categoria, nombre
        """
    ).fetchall()
    conexion.close()

=======
def obtener_productos():
    conexion = obtener_conexion()
    productos = conexion.execute("""
        SELECT id, nombre, descripcion, precio, categoria, disponible
        FROM productos
        ORDER BY categoria, nombre
    """).fetchall()
    conexion.close()
>>>>>>> frontend
    return [dict(producto) for producto in productos]
