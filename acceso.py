"""Acceso interno del personal. El estudiante conserva su flujo público."""
import hashlib
import os
import secrets
import sqlite3
from collections import defaultdict, deque
from contextlib import closing
from datetime import timedelta
from pathlib import Path
from threading import Lock
from time import monotonic
from urllib.parse import urlsplit

import click
from flask import g, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from database import obtener_conexion


def crear_personal(usuario, password):
    usuario = usuario.strip()
    if (not usuario or len(usuario) > 50 or len(password) < 12
            or len(password) > 128 or not password.strip()):
        raise ValueError("Usa un usuario de hasta 50 caracteres y una contraseña de 12 a 128 caracteres.")
    with closing(obtener_conexion()) as conexion, conexion:
        try:
            conexion.execute(
                "INSERT INTO usuarios (usuario, hash_password) VALUES (?, ?)",
                (usuario, generate_password_hash(password)),
            )
        except sqlite3.IntegrityError:
            raise ValueError("Ese usuario ya existe.") from None


def destino_interno(valor):
    """Solo se permite volver a vistas internas conocidas, nunca a otro sitio."""
    if not isinstance(valor, str) or any(c in valor for c in ("\\", "\r", "\n")):
        return url_for("caja")
    try:
        partes = urlsplit(valor)
    except ValueError:
        return url_for("caja")
    if partes.scheme or partes.netloc or partes.path not in ("/caja", "/cocina", "/admin"):
        return url_for("caja")
    return partes.path + ("?" + partes.query if partes.query else "")


def token_csrf():
    if "csrf" not in session:
        session["csrf"] = secrets.token_urlsafe(32)
    return session["csrf"]


def instalar_acceso(app):
    # La clave local persiste entre reinicios y queda fuera de Git (instance/).
    clave = os.environ.get("SECRET_KEY")
    if not clave:
        directorio = Path(app.instance_path)
        directorio.mkdir(mode=0o700, parents=True, exist_ok=True)
        archivo = directorio / "session.key"
        try:
            descriptor = os.open(archivo, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError:
            pass
        else:
            with os.fdopen(descriptor, "w") as salida:
                salida.write(secrets.token_hex(32))
        clave = archivo.read_text().strip()
    if len(clave) < 32:
        raise RuntimeError("SECRET_KEY debe contener al menos 32 caracteres aleatorios.")
    app.config.update(
        SECRET_KEY=clave,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE") == "1",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=8),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    )
    hosts = os.environ.get("TRUSTED_HOSTS", "")
    if hosts:
        app.config["TRUSTED_HOSTS"] = [h.strip() for h in hosts.split(",") if h.strip()]
    app.jinja_env.globals["token_csrf"] = token_csrf
    publicas = {"inicio", "menu", "api_crear_pedido", "static", "login"}
    intentos = defaultdict(deque)
    bloqueo = Lock()
    hash_ficticio = generate_password_hash(secrets.token_urlsafe(32))

    @app.before_request
    def proteger_acceso():
        g.personal = None
        acceso = session.get("acceso")
        if isinstance(acceso, str):
            with closing(obtener_conexion()) as conexion:
                g.personal = conexion.execute("""
                    SELECT usuarios.id, usuarios.usuario FROM sesiones_personal
                    JOIN usuarios ON usuarios.id = sesiones_personal.usuario_id
                    WHERE token_hash = ? AND vence > datetime('now')
                """, (hashlib.sha256(acceso.encode()).hexdigest(),)).fetchone()
        if request.endpoint and request.endpoint not in publicas and g.personal is None:
            if request.path.startswith("/api/"):
                return jsonify(error="Inicia sesión como personal para realizar esta acción."), 401
            return redirect(url_for("login", next=request.full_path.rstrip("?")))
        if request.method not in ("GET", "HEAD", "OPTIONS") and request.endpoint != "api_crear_pedido":
            esperado = session.get("csrf")
            recibido = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
            if (not isinstance(esperado, str) or not isinstance(recibido, str)
                    or not recibido.isascii()
                    or not secrets.compare_digest(esperado, recibido)):
                if request.path.startswith("/api/"):
                    return jsonify(error="La sesión cambió o el formulario venció. Actualiza la página."), 403
                return render_template("error.html", mensaje="El formulario venció. Vuelve a abrir la página."), 403

    @app.after_request
    def cabeceras_seguras(respuesta):
        respuesta.headers["X-Content-Type-Options"] = "nosniff"
        respuesta.headers["X-Frame-Options"] = "DENY"
        respuesta.headers["Referrer-Policy"] = "same-origin"
        respuesta.headers["Content-Security-Policy"] = (
            "default-src 'self'; img-src 'self' data:; "
            "frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        )
        if request.endpoint != "static":
            respuesta.headers["Cache-Control"] = "no-store"
        return respuesta

    @app.route("/login", methods=["GET", "POST"])
    def login():
        siguiente = destino_interno(request.values.get("next", ""))
        if g.personal is not None:
            return redirect(siguiente)
        error = None
        estado = 200
        if request.method == "POST":
            # Límite básico por dirección, con limpieza y protección entre hilos.
            direccion = request.remote_addr or "local"
            ahora = monotonic()
            with bloqueo:
                for clave in list(intentos):
                    while intentos[clave] and intentos[clave][0] < ahora - 300:
                        intentos[clave].popleft()
                    if not intentos[clave]:
                        del intentos[clave]
                limitado = len(intentos[direccion]) >= 5 or len(intentos) > 1000
                if not limitado:
                    intentos[direccion].append(ahora)
            if limitado:
                error, estado = "Demasiados intentos. Espera cinco minutos antes de volver a intentar.", 429
            else:
                usuario = request.form.get("usuario", "").strip()
                password = request.form.get("password", "")
                with closing(obtener_conexion()) as conexion:
                    personal = conexion.execute(
                        "SELECT id, hash_password FROM usuarios WHERE usuario = ?", (usuario,)
                    ).fetchone()
                valido = check_password_hash(
                    personal["hash_password"] if personal else hash_ficticio, password[:129]
                )
                if personal and valido and len(password) <= 128:
                    acceso = secrets.token_urlsafe(32)
                    with closing(obtener_conexion()) as conexion, conexion:
                        conexion.execute("DELETE FROM sesiones_personal WHERE vence <= datetime('now')")
                        conexion.execute(
                            "INSERT INTO sesiones_personal VALUES (?, ?, datetime('now', '+8 hours'))",
                            (hashlib.sha256(acceso.encode()).hexdigest(), personal["id"]),
                        )
                    session.clear()
                    session["acceso"] = acceso
                    session.permanent = True
                    with bloqueo:
                        intentos.pop(direccion, None)
                    return redirect(siguiente)
                error, estado = "Usuario o contraseña incorrectos.", 401
        return render_template("login.html", siguiente=siguiente, error=error), estado

    @app.post("/logout")
    def logout():
        acceso = session.get("acceso", "")
        with closing(obtener_conexion()) as conexion, conexion:
            conexion.execute(
                "DELETE FROM sesiones_personal WHERE token_hash = ?",
                (hashlib.sha256(acceso.encode()).hexdigest(),),
            )
        session.clear()
        return redirect(url_for("login"))

    @app.cli.command("crear-personal")
    @click.option("--usuario", prompt="Usuario del personal")
    @click.password_option(prompt="Contraseña (mínimo 12 caracteres)")
    def crear_cuenta(usuario, password):
        """Crea una cuenta interna local sin guardar la contraseña en el código."""
        try:
            crear_personal(usuario, password)
        except ValueError as error:
            raise click.ClickException(str(error)) from None
        click.echo("Cuenta del personal creada. Ya puedes iniciar sesión en /login.")
