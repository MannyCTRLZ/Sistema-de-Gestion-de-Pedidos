from flask import Flask, jsonify, render_template, request
from database import (
    MAX_ENTERO_SQLITE,
    cambiar_estado_en_caja,
    cambiar_estado_en_cocina,
    crear_pedido,
    crear_tablas,
    insertar_productos_iniciales,
    obtener_pedidos,
    obtener_pedidos_cocina,
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


@app.route("/caja")
def caja():
    pedidos = obtener_pedidos()
    vista = "historial" if request.args.get("vista") == "historial" else "seguimiento"
    cantidad_entregados = sum(pedido["estado"] == "ENTREGADO" for pedido in pedidos)
    busqueda = request.args.get("numero", "").strip()
    error_busqueda = None
    resumen = {
        "total": len(pedidos),
        "pendientes": sum(
            pedido["estado"] == "PENDIENTE DE PAGO" for pedido in pedidos
        ),
        "pagados": sum(pedido["estado"] == "PAGADO" for pedido in pedidos),
    }
    pedidos = [
        pedido for pedido in pedidos
        if (pedido["estado"] == "ENTREGADO") == (vista == "historial")
    ]
    if busqueda:
        numero = busqueda.removeprefix("#")
        if (not numero.isascii() or not numero.isdecimal()
                or len(numero) > 19 or not 0 < int(numero) <= MAX_ENTERO_SQLITE):
            error_busqueda = "Ingresa un número de pedido válido, por ejemplo 0001."
            pedidos = []
        else:
            pedidos = [
                pedido for pedido in pedidos
                if pedido["numero_pedido"] == int(numero)
            ]
    return render_template(
        "caja.html", pedidos=pedidos, resumen=resumen,
        busqueda=busqueda, error_busqueda=error_busqueda,
        vista=vista, cantidad_entregados=cantidad_entregados,
    )


@app.route("/cocina")
def cocina():
    pedidos = obtener_pedidos_cocina()
    resumen = {
        "pagados": sum(pedido["estado"] == "PAGADO" for pedido in pedidos),
        "preparacion": sum(pedido["estado"] == "EN PREPARACIÓN" for pedido in pedidos),
        "listos": sum(pedido["estado"] == "LISTO" for pedido in pedidos),
    }
    return render_template("cocina.html", pedidos=pedidos, resumen=resumen)


@app.post("/api/cocina/pedidos/<int:numero_pedido>/estado")
def api_cambiar_estado_en_cocina(numero_pedido):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"error": "Los datos de la acción no son válidos."}), 400
    try:
        pedido = cambiar_estado_en_cocina(numero_pedido, datos.get("estado"))
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(pedido)


@app.post("/api/pedidos/<int:numero_pedido>/estado")
def api_cambiar_estado_en_caja(numero_pedido):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"error": "Los datos de la acción no son válidos."}), 400
    try:
        pedido = cambiar_estado_en_caja(numero_pedido, datos.get("estado"))
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(pedido)


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
