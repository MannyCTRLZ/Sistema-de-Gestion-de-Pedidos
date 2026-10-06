from flask import Flask, jsonify, render_template, request
from database import (
    crear_pedido,
    crear_tablas,
    insertar_productos_iniciales,
    obtener_productos,
)

app = Flask(__name__)

crear_tablas()
insertar_productos_iniciales()


@app.route("/")
def inicio():
    productos = obtener_productos()
    return render_template("index.html", productos=productos)


@app.route("/menu")
def menu():
    productos = obtener_productos()
    return render_template("menu.html", productos=productos)


@app.post("/api/pedidos")
def api_crear_pedido():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Los datos del pedido no son válidos."}), 400

    try:
        pedido = crear_pedido(
            datos.get("nombre_cliente"),
            datos.get("productos"),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    return jsonify(pedido), 201


if __name__ == "__main__":
    app.run(debug=True)
