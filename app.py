import base64
import io
import os
import secrets
from pathlib import Path
from urllib.parse import urljoin, urlsplit

import segno
from flask import Flask, jsonify, render_template, request, url_for
from acceso import instalar_acceso
from database import (
    MAX_ENTERO_SQLITE,
    cambiar_estado_en_caja,
    cambiar_estado_en_cocina,
    cambiar_disponibilidad,
    crear_pedido,
    crear_tablas,
    eliminar_producto,
    insertar_productos_iniciales,
    guardar_producto,
    obtener_pedidos,
    obtener_pedidos_cocina,
    obtener_producto,
    obtener_productos,
)

app = Flask(__name__)
app.config["CARPETA_IMAGENES_PRODUCTOS"] = str(
    Path(app.static_folder) / "img" / "productos"
)

TIPOS_IMAGEN_PRODUCTO = {
    "jpeg": lambda cabecera: cabecera.startswith(b"\xff\xd8\xff"),
    "png": lambda cabecera: cabecera.startswith(b"\x89PNG\r\n\x1a\n"),
    "webp": lambda cabecera: cabecera.startswith(b"RIFF") and cabecera[8:12] == b"WEBP",
}


def guardar_imagen_producto(archivo):
    cabecera = archivo.stream.read(16)
    archivo.stream.seek(0)
    extension = next(
        (tipo for tipo, coincide in TIPOS_IMAGEN_PRODUCTO.items() if coincide(cabecera)),
        None,
    )
    if extension is None:
        raise ValueError("La imagen debe ser un archivo JPEG, PNG o WebP válido.")

    carpeta = Path(app.config["CARPETA_IMAGENES_PRODUCTOS"])
    carpeta.mkdir(parents=True, exist_ok=True)
    nombre = f"{secrets.token_hex(16)}.{extension}"
    archivo.save(carpeta / nombre)
    return f"img/productos/{nombre}"


def borrar_archivo_imagen(imagen):
    if not isinstance(imagen, str) or not imagen.startswith("img/productos/"):
        return
    nombre = Path(imagen).name
    if nombre != imagen.removeprefix("img/productos/"):
        return
    try:
        (Path(app.config["CARPETA_IMAGENES_PRODUCTOS"]) / nombre).unlink(missing_ok=True)
    except OSError:
        pass


crear_tablas()
insertar_productos_iniciales()
instalar_acceso(app)


@app.errorhandler(413)
def peticion_grande(error):
    return jsonify(error="La solicitud es demasiado grande. Reduce su contenido."), 413


@app.errorhandler(500)
def error_interno(error):
    if request.path.startswith("/api/"):
        return jsonify(error="No se pudo completar la operación. Actualiza antes de reintentar."), 500
    return render_template("error.html", mensaje="No se pudo completar la operación. Intenta más tarde."), 500


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
    es_formulario = request.mimetype == "multipart/form-data"
    if es_formulario:
        datos = request.form.to_dict()
        datos["disponible"] = request.form.get("disponible") == "true"
    else:
        datos = request.get_json(silent=True)

    imagen_nueva = None
    cambiar_imagen = False
    imagen_anterior = None
    try:
        if producto_id is not None:
            imagen_anterior = obtener_producto(producto_id)["imagen"]
        if es_formulario:
            archivo = request.files.get("imagen")
            quitar_imagen = request.form.get("quitar_imagen") == "true"
            if archivo and archivo.filename and quitar_imagen:
                raise ValueError("Elige una imagen nueva o quita la actual, no ambas opciones.")
            if archivo and archivo.filename:
                imagen_nueva = guardar_imagen_producto(archivo)
                cambiar_imagen = True
            elif quitar_imagen:
                cambiar_imagen = True

        if cambiar_imagen:
            producto = guardar_producto(datos, producto_id, imagen_nueva)
        else:
            producto = guardar_producto(datos, producto_id)
    except ValueError as error:
        borrar_archivo_imagen(imagen_nueva)
        return jsonify({"error": str(error)}), 400
    except LookupError as error:
        borrar_archivo_imagen(imagen_nueva)
        return jsonify({"error": str(error)}), 404
    except OSError:
        borrar_archivo_imagen(imagen_nueva)
        return jsonify({"error": "No se pudo guardar la imagen. Intenta nuevamente."}), 500

    if cambiar_imagen and imagen_anterior != imagen_nueva:
        borrar_archivo_imagen(imagen_anterior)
    return jsonify(producto), 201 if producto_id is None else 200


@app.delete("/api/productos/<int:producto_id>")
def api_eliminar_producto(producto_id):
    try:
        producto = eliminar_producto(producto_id)
    except ValueError as error:
        return jsonify({"error": str(error)}), 409
    except LookupError as error:
        return jsonify({"error": str(error)}), 404
    borrar_archivo_imagen(producto["imagen"])
    return jsonify({"id": producto_id})


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

    # Render publica su URL HTTPS; una dirección explícita permite usar un dominio propio.
    base_publica = (os.environ.get("PUBLIC_BASE_URL", "").strip()
                    or os.environ.get("RENDER_EXTERNAL_URL", "").strip())
    try:
        base = urlsplit(base_publica)
    except ValueError:
        return jsonify(error="La dirección del QR no está configurada correctamente. Avisa al personal."), 503
    if base_publica and (base.scheme not in ("http", "https") or not base.netloc
                         or base.username or base.password or base.query or base.fragment
                         or len(base_publica) > 2000):
        return jsonify(error="La dirección del QR no está configurada correctamente. Avisa al personal."), 503
    try:
        pedido = crear_pedido(
            datos.get("nombre_cliente"),
            datos.get("productos"),
        )
    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    numero = pedido["numero_pedido"]
    ruta_caja = url_for("caja", numero=numero)
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
    app.run(debug=False)
