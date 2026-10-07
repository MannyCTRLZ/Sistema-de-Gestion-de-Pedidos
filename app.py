from flask import Flask, render_template
from database import (
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



if __name__ == "__main__":
    app.run(debug=True)
