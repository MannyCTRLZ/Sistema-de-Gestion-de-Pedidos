<<<<<<< HEAD
from flask import Flask, jsonify, render_template
from database import (
    crear_tablas,
    insertar_productos_prueba,
    obtener_productos_disponibles,
=======
from flask import Flask, render_template
from database import (
    crear_tablas,
    insertar_productos_iniciales,
    obtener_productos,
>>>>>>> frontend
)

app = Flask(__name__)

crear_tablas()
<<<<<<< HEAD
insertar_productos_prueba()
=======
insertar_productos_iniciales()
>>>>>>> frontend


@app.route("/")
def inicio():
    productos = obtener_productos()
    return render_template("index.html", productos=productos)


@app.route("/menu")
def menu():
    productos = obtener_productos()
    return render_template("menu.html", productos=productos)


@app.route("/api/productos")
def api_productos():
    return jsonify(obtener_productos_disponibles())


if __name__ == "__main__":
    app.run(debug=True)
