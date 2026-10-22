import os
import re
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch
from urllib.parse import parse_qs, urlsplit

import database
from acceso import crear_personal
from ayuda_acceso import USUARIO_PRUEBA, PASSWORD_PRUEBA, autenticar

with tempfile.TemporaryDirectory() as temporal_importacion:
    original = database.DATABASE
    database.DATABASE = str(Path(temporal_importacion) / "arranque.db")
    from app import app
    database.DATABASE = original


class AccesoTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.original = database.DATABASE
        database.DATABASE = str(Path(self.temporal.name) / "seguridad.db")
        database.crear_tablas()
        database.insertar_productos_iniciales()
        self.cliente = app.test_client()
        self.pedido = database.crear_pedido("Estudiante", [{"id": 1, "cantidad": 1}])["numero_pedido"]

    def tearDown(self):
        database.DATABASE = self.original
        self.temporal.cleanup()

    def token(self, cliente=None, ruta="/login"):
        cliente = cliente or self.cliente
        html = cliente.get(ruta).get_data(as_text=True)
        return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)

    def login(self, cliente=None, siguiente="/caja", password=PASSWORD_PRUEBA):
        cliente = cliente or self.cliente
        return cliente.post("/login", data={
            "usuario": USUARIO_PRUEBA, "password": password,
            "csrf_token": self.token(cliente), "next": siguiente,
        })

    def test_qr_sin_sesion_exige_acceso_y_conserva_numero(self):
        enlace = f"/caja?numero={self.pedido}"
        respuesta = self.cliente.get(enlace)
        self.assertEqual(respuesta.status_code, 302)
        destino = urlsplit(respuesta.location)
        self.assertEqual(destino.path, "/login")
        self.assertEqual(parse_qs(destino.query)["next"], [enlace])
        self.assertNotIn("Estudiante", respuesta.get_data(as_text=True))
        crear_personal(USUARIO_PRUEBA, PASSWORD_PRUEBA)
        respuesta = self.login(siguiente=enlace)
        self.assertEqual(respuesta.location, enlace)
        html = self.cliente.get(enlace).get_data(as_text=True)
        self.assertIn("Estudiante", html)
        self.assertIn("Confirmar pago", html)

    def test_paginas_y_apis_rechazan_visitante_sin_modificar_datos(self):
        for pagina in ("/caja", "/caja?vista=historial", "/cocina", "/admin"):
            self.assertEqual(self.cliente.get(pagina).status_code, 302)
        intentos = [
            ("post", f"/api/pedidos/{self.pedido}/estado", {"estado": "PAGADO"}),
            ("post", f"/api/pedidos/{self.pedido}/estado", {"estado": "CANCELADO"}),
            ("post", f"/api/cocina/pedidos/{self.pedido}/estado", {"estado": "ENTREGADO"}),
            ("post", "/api/productos", {}),
            ("put", "/api/productos/1", {}),
            ("patch", "/api/productos/1/disponibilidad", {"disponible": False}),
        ]
        for metodo, url, datos in intentos:
            with self.subTest(url=url, metodo=metodo):
                respuesta = getattr(self.cliente, metodo)(url, json=datos)
                self.assertEqual(respuesta.status_code, 401)
                self.assertIn("Inicia sesión", respuesta.get_json()["error"])
        self.assertEqual(database.obtener_pedidos()[0]["estado"], "PENDIENTE DE PAGO")
        self.assertEqual(len(database.obtener_productos()), 8)
        self.assertEqual(database.obtener_productos()[0]["disponible"], 1)

    def test_estudiante_sigue_sin_cuenta_y_genera_qr(self):
        for pagina in ("/", "/menu"):
            self.assertEqual(self.cliente.get(pagina).status_code, 200)
        respuesta = self.cliente.post("/api/pedidos", json={
            "nombre_cliente": "Estudiante sin cuenta", "productos": [{"id": 1, "cantidad": 1}],
        })
        self.assertEqual(respuesta.status_code, 201)
        self.assertIn("codigo_qr", respuesta.get_json())

    def test_csrf_login_y_acciones_no_se_pueden_omitir(self):
        self.assertEqual(self.cliente.post("/login", data={}).status_code, 403)
        autenticar(self.cliente)
        self.cliente.environ_base.pop("HTTP_X_CSRF_TOKEN")
        for cabeceras in ({}, {"X-CSRF-Token": "inventado"}, {"X-CSRF-Token": "inválido"}):
            respuesta = self.cliente.post(f"/api/pedidos/{self.pedido}/estado",
                                          json={"estado": "PAGADO"}, headers=cabeceras)
            self.assertEqual(respuesta.status_code, 403)
        self.assertEqual(database.obtener_pedidos()[0]["estado"], "PENDIENTE DE PAGO")
        self.assertEqual(self.cliente.post("/logout").status_code, 403)
        self.assertEqual(self.cliente.get("/caja").status_code, 200)

    def test_credenciales_invalidas_no_crean_sesion_y_hash_no_es_password(self):
        crear_personal(USUARIO_PRUEBA, PASSWORD_PRUEBA)
        self.assertEqual(self.login(password="incorrecta").status_code, 401)
        self.assertEqual(self.cliente.get("/admin").status_code, 302)
        with closing(database.obtener_conexion()) as conexion:
            usuario = conexion.execute("SELECT hash_password FROM usuarios").fetchone()
            self.assertNotEqual(usuario["hash_password"], PASSWORD_PRUEBA)
            self.assertEqual(conexion.execute("SELECT count(*) FROM sesiones_personal").fetchone()[0], 0)
        self.assertEqual(self.login().status_code, 302)

    def test_redireccion_solo_a_rutas_internas(self):
        crear_personal(USUARIO_PRUEBA, PASSWORD_PRUEBA)
        for siguiente in ("https://externo.example", "//externo.example/caja", "/\\externo.example",
                          "http://[", "/login", "/api/pedidos", "/%2fexterno.example"):
            respuesta = self.login(cliente=app.test_client(), siguiente=siguiente)
            self.assertEqual(respuesta.status_code, 302)
            self.assertEqual(respuesta.location, "/caja")

    def test_logout_revoca_cookie_copiada_y_sesion_vencida(self):
        autenticar(self.cliente)
        cookie = self.cliente.get_cookie("session").value
        self.assertEqual(self.cliente.post("/logout").status_code, 302)
        self.cliente.set_cookie("session", cookie)
        self.assertEqual(self.cliente.get("/caja").status_code, 302)
        autenticar(self.cliente, crear=False)
        with closing(database.obtener_conexion()) as conexion, conexion:
            conexion.execute("UPDATE sesiones_personal SET vence = datetime('now', '-1 second')")
        self.assertEqual(self.cliente.get("/caja").status_code, 302)
        self.assertEqual(self.cliente.post(f"/api/pedidos/{self.pedido}/estado",
                                          json={"estado": "PAGADO"}).status_code, 401)

    def test_limite_de_intentos_y_cabeceras(self):
        for intento in range(6):
            token = self.token()
            respuesta = self.cliente.post("/login", data={
                "usuario": "inexistente", "password": "incorrecta", "csrf_token": token,
            }, environ_overrides={"REMOTE_ADDR": "198.51.100.42"})
            self.assertEqual(respuesta.status_code, 401 if intento < 5 else 429)
        respuesta = self.cliente.get("/login")
        self.assertEqual(respuesta.headers["Cache-Control"], "no-store")
        self.assertIn("frame-ancestors 'none'", respuesta.headers["Content-Security-Policy"])
        cookie = app.test_client().get("/login").headers["Set-Cookie"]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)

    def test_nombre_largo_total_excesivo_y_base_qr_invalida_no_guardan(self):
        for nombre, cantidad in (("a" * 51, 1), ("Ana", 2**62)):
            respuesta = self.cliente.post("/api/pedidos", json={
                "nombre_cliente": nombre, "productos": [{"id": 1, "cantidad": cantidad}],
            })
            self.assertEqual(respuesta.status_code, 400)
        for base in ("javascript:alert(1)", "http://[", "https://u:p@example.com"):
            with patch.dict(os.environ, {"PUBLIC_BASE_URL": base}):
                respuesta = self.cliente.post("/api/pedidos", json={
                    "nombre_cliente": "Ana", "productos": [{"id": 1, "cantidad": 1}],
                })
            self.assertEqual(respuesta.status_code, 503)
        self.assertEqual(len(database.obtener_pedidos()), 1)

    def test_cli_crea_cuenta_sin_contrasena_por_defecto(self):
        ejecutor = app.test_cli_runner()
        respuesta = ejecutor.invoke(args=["crear-personal", "--usuario", "cajera"],
                                    input="contrasena-solo-prueba\ncontrasena-solo-prueba\n")
        self.assertEqual(respuesta.exit_code, 0, respuesta.output)
        self.assertNotIn("contrasena-solo-prueba", respuesta.output)
        respuesta = ejecutor.invoke(args=["crear-personal", "--usuario", "cajera"],
                                    input="otra-contrasena-prueba\notra-contrasena-prueba\n")
        self.assertNotEqual(respuesta.exit_code, 0)


if __name__ == "__main__":
    unittest.main()
