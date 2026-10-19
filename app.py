import base64
import io
import os
from urllib.parse import urljoin

import segno
from flask import Flask, jsonify, render_template, request, url_for
from database import (
    MAX_ENTERO_SQLITE,
    cambiar_estado_en_caja,
    cambiar_estado_en_cocina,
    cambiar_disponibilidad,
    crear_pedido,
    crear_tablas,
    insertar_productos_iniciales,
    guardar_producto,
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


@app.route("/admin")
def administracion():
    productos = obtener_productos()
    disponibles = sum(bool(producto["disponible"]) for producto in productos)
    return render_template(
        "admin.html", productos=productos, disponibles=disponibles,
    )


@app.post("/api/productos")
@app.put("/api/productos/<int:producto_id>")
def api_guardar_producto(producto_id=None):
    try:
        producto = guardar_producto(request.get_json(silent=True), producto_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    return jsonify(producto), 201 if producto_id is None else 200


@app.patch("/api/productos/<int:producto_id>/disponibilidad")
def api_cambiar_disponibilidad(producto_id):
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify({"error": "Los datos no son válidos."}), 400
    try:
        producto = cambiar_disponibilidad(producto_id, datos.get("disponible"))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    return jsonify(producto)


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

    numero = pedido["numero_pedido"]
    ruta_caja = url_for("caja", numero=numero)
    base_publica = os.environ.get("PUBLIC_BASE_URL", "").strip()
    if base_publica:
        enlace_caja = urljoin(base_publica.rstrip("/") + "/", ruta_caja.lstrip("/"))
    else:
        enlace_caja = url_for("caja", numero=numero, _external=True)

    imagen = io.BytesIO()
    segno.make_qr(enlace_caja, error="m").save(
        imagen, kind="svg", scale=5, border=4
    )
    pedido["codigo_qr"] = (
        "data:image/svg+xml;base64,"
        + base64.b64encode(imagen.getvalue()).decode("ascii")
    )
    return jsonify(pedido), 201


if __name__ == "__main__":
    app.run(debug=True)
