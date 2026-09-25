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

    conexion.commit()
    conexion.close()


def insertar_productos_iniciales():
    conexion = obtener_conexion()

    cantidad = conexion.execute(
        "SELECT COUNT(*) FROM productos"
    ).fetchone()[0]

    if cantidad == 0:
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
            )
        ]

        conexion.executemany("""
            INSERT INTO productos
            (nombre, descripcion, precio, categoria, disponible)
            VALUES (?, ?, ?, ?, ?)
        """, productos)

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
