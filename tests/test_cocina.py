import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import database

# El arranque de Flask también queda aislado de la base real.
with tempfile.TemporaryDirectory() as temporal_importacion:
    base_original = database.DATABASE
    database.DATABASE = str(Path(temporal_importacion) / "importacion.db")
    from app import app
    database.DATABASE = base_original


class CocinaTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.base_original = database.DATABASE
        database.DATABASE = str(Path(self.temporal.name) / "cocina.db")
        database.crear_tablas()
        database.insertar_productos_iniciales()
        self.cliente = app.test_client()

    def tearDown(self):
        database.DATABASE = self.base_original
        self.temporal.cleanup()

    def crear(self, nombre="Ana cocina"):
        respuesta = self.cliente.post("/api/pedidos", json={
            "nombre_cliente": nombre,
            "productos": [{"id": 1, "cantidad": 2}, {"id": 3, "cantidad": 1}],
        })
        self.assertEqual(respuesta.status_code, 201)
        return respuesta.get_json()["numero_pedido"]

    def cambiar(self, numero, estado):
        return self.cliente.post(
            f"/api/cocina/pedidos/{numero}/estado", json={"estado": estado}
        )

    def estado(self, numero):
        conexion = database.obtener_conexion()
        try:
            return conexion.execute(
                "SELECT estado FROM pedidos WHERE numero_pedido = ?", (numero,)
            ).fetchone()["estado"]
        finally:
            conexion.close()

    def fijar_estado(self, numero, estado):
        conexion = database.obtener_conexion()
        try:
            conexion.execute(
                "UPDATE pedidos SET estado = ? WHERE numero_pedido = ?",
                (estado, numero),
            )
            conexion.commit()
        finally:
            conexion.close()

    def test_flujo_completo_pago_preparacion_entrega_e_historial(self):
        numero = self.crear()
        self.assertEqual(database.obtener_pedidos_cocina(), [])
        pago = self.cliente.post(f"/api/pedidos/{numero}/estado", json={"estado": "PAGADO"})
        self.assertEqual(pago.status_code, 200)
        for estado, boton in (
            ("EN PREPARACIÓN", "Comenzar preparación"),
            ("LISTO", "Marcar como listo"),
            ("ENTREGADO", "Marcar como entregado"),
        ):
            html = self.cliente.get("/cocina").get_data(as_text=True)
            self.assertIn(boton, html)
            self.assertIn("<strong>2 ×</strong> Tacos capeados", html)
            self.assertEqual(self.cambiar(numero, estado).status_code, 200)
            self.assertEqual(self.estado(numero), estado)
        self.assertEqual(database.obtener_pedidos_cocina(), [])
        self.assertIn("No hay pedidos activos", self.cliente.get("/cocina").get_data(as_text=True))
        self.assertNotIn("Ana cocina", self.cliente.get("/caja").get_data(as_text=True))
        historial = self.cliente.get("/caja", query_string={
            "vista": "historial", "numero": f"#{numero:04d}",
        }).get_data(as_text=True)
        self.assertIn("Ana cocina", historial)
        self.assertIn("ENTREGADO", historial)
        self.assertIn("$155.00", historial)
        self.assertIn("2 × Tacos capeados", historial)
        self.assertNotIn("Confirmar pago", historial)
        self.assertNotIn("Cancelar pedido", historial)

    def test_todas_las_transiciones_y_reintentos(self):
        numero = self.crear()
        permitidas = {("PAGADO", "EN PREPARACIÓN"),
                      ("EN PREPARACIÓN", "LISTO"), ("LISTO", "ENTREGADO")}
        for anterior in ("PENDIENTE DE PAGO", "PAGADO", "EN PREPARACIÓN", "LISTO", "ENTREGADO", "CANCELADO"):
            for siguiente in ("EN PREPARACIÓN", "LISTO", "ENTREGADO"):
                with self.subTest(anterior=anterior, siguiente=siguiente):
                    self.fijar_estado(numero, anterior)
                    respuesta = self.cambiar(numero, siguiente)
                    valido = (anterior, siguiente) in permitidas
                    self.assertEqual(respuesta.status_code, 200 if valido else 400)
                    self.assertEqual(self.estado(numero), siguiente if valido else anterior)

    def test_peticiones_invalidas_no_cambian_el_pedido(self):
        numero = self.crear()
        self.fijar_estado(numero, "PAGADO")
        for valor in (None, {}, [], 1, "PAGADO", "CANCELADO", "estado inventado"):
            self.assertEqual(self.cambiar(numero, valor).status_code, 400)
        url = f"/api/cocina/pedidos/{numero}/estado"
        for payload in (None, [], "texto", {}):
            self.assertEqual(self.cliente.post(url, json=payload).status_code, 400)
        self.assertEqual(self.cliente.post(url, data='{', content_type='application/json').status_code, 400)
        self.assertEqual(self.cliente.get(url).status_code, 405)
        self.assertEqual(self.cambiar(999, "EN PREPARACIÓN").status_code, 404)
        self.assertEqual(self.cambiar(2**63, "EN PREPARACIÓN").status_code, 400)
        self.assertEqual(self.estado(numero), "PAGADO")

    def test_lista_excluye_inactivos_y_respeta_orden(self):
        numeros = []
        for estado in ("PENDIENTE DE PAGO", "LISTO", "PAGADO", "CANCELADO", "ENTREGADO", "EN PREPARACIÓN"):
            numero = self.crear(estado)
            self.fijar_estado(numero, estado)
            if estado in ("LISTO", "PAGADO", "EN PREPARACIÓN"):
                numeros.append(numero)
        self.assertEqual([p["numero_pedido"] for p in database.obtener_pedidos_cocina()], numeros)

    def test_dos_cocineros_avanzando_el_mismo_pedido(self):
        numero = self.crear()
        self.fijar_estado(numero, "PAGADO")
        barrera = threading.Barrier(2)

        def avanzar():
            cliente = app.test_client()
            barrera.wait(timeout=5)
            return cliente.post(
                f"/api/cocina/pedidos/{numero}/estado", json={"estado": "EN PREPARACIÓN"}
            ).status_code

        with ThreadPoolExecutor(max_workers=2) as executor:
            respuestas = list(executor.map(lambda _: avanzar(), range(2)))
        self.assertEqual(sorted(respuestas), [200, 400])
        self.assertEqual(self.estado(numero), "EN PREPARACIÓN")

    def test_persistencia_conserva_detalle_total_y_fecha(self):
        numero = self.crear()
        antes = database.obtener_pedidos()[0]
        self.fijar_estado(numero, "PAGADO")
        for estado in ("EN PREPARACIÓN", "LISTO", "ENTREGADO"):
            self.assertEqual(self.cambiar(numero, estado).status_code, 200)
        despues = database.obtener_pedidos()[0]
        self.assertEqual(despues["estado"], "ENTREGADO")
        for campo in ("productos", "fecha", "nombre_cliente", "total", "numero_pedido"):
            self.assertEqual(antes[campo], despues[campo])
        conexion = database.obtener_conexion()
        try:
            self.assertEqual(conexion.execute("PRAGMA foreign_key_check").fetchall(), [])
            self.assertEqual(conexion.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        finally:
            conexion.close()

    def test_historial_vacio_busqueda_y_escape_de_texto(self):
        self.assertIn("Todavía no hay pedidos entregados", self.cliente.get("/caja?vista=historial").get_data(as_text=True))
        numero = self.crear('<script>alert("x")</script>')
        self.fijar_estado(numero, "ENTREGADO")
        html = self.cliente.get("/caja?vista=historial").get_data(as_text=True)
        self.assertNotIn('<script>alert("x")</script>', html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("No se encontraron pedidos", self.cliente.get("/caja?vista=historial&numero=999").get_data(as_text=True))
        self.assertIn("Ingresa un número de pedido válido", self.cliente.get("/caja?vista=historial&numero=abc").get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
