from flask import Flask, render_template
from database import crear_tablas

app = Flask(__name__)

crear_tablas()


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)