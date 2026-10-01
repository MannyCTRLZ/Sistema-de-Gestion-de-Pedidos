from flask import Flask, jsonify, render_template
from database import (
    crear_tablas,
    insertar_productos_prueba,
    obtener_productos_disponibles,
)

app = Flask(__name__)

crear_tablas()
insertar_productos_prueba()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/menu")
def menu():
    return render_template("menu.html")


@app.route("/api/productos")
def api_productos():
    return jsonify(obtener_productos_disponibles())


if __name__ == "__main__":
    app.run(debug=True)
