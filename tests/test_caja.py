import base64
import os
import tempfile
import unittest
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import database
import segno
from ayuda_acceso import autenticar

# Importar Flask con una base temporal evita tocar cafeteria.db.
BASE_IMPORTACION = tempfile.TemporaryDirectory()
BASE_ORIGINAL = database.DATABASE
database.DATABASE = str(Path(BASE_IMPORTACION.name) / "importacion.db")
from app import app
database.DATABASE = BASE_ORIGINAL
BASE_IMPORTACION.cleanup()


class CajaTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.base_original = database.DATABASE
        database.DATABASE = str(Path(self.temporal.name) / "caja.db")
        database.crear_tablas()
        database.insertar_productos_iniciales()
        self.cliente = app.test_client()
        autenticar(self.cliente)

    def tearDown(self):
        database.DATABASE = self.base_original
        self.temporal.cleanup()

    def crear_pedido(self, nombre="María"):
        respuesta = self.cliente.post("/api/pedidos", json={
            "nombre_cliente": nombre,
            "productos": [{"id": 1, "cantidad": 2}, {"id": 3, "cantidad": 1}],
        })
        self.assertEqual(respuesta.status_code, 201)
        return respuesta.get_json()["numero_pedido"]

    def cambiar(self, numero, estado):
        return self.cliente.post(f"/api/pedidos/{numero}/estado", json={"estado": estado})

    def test_flujo_creacion_busqueda_pago_y_persistencia(self):
        numero = self.crear_pedido()
        self.crear_pedido("Carlos")
        pagina = self.cliente.get("/caja", query_string={"numero": f"#{numero:04d}"})
        html = pagina.get_data(as_text=True)
        self.assertEqual(pagina.status_code, 200)
        self.assertIn("María", html)
        self.assertNotIn("Carlos", html)
        self.assertIn("2 × Tacos capeados", html)
        self.assertIn("$155.00", html)
        self.assertIn("Confirmar pago", html)
        self.assertEqual(self.cambiar(numero, "PAGADO").status_code, 200)
        with closing(database.obtener_conexion()) as conexion:
            fila = conexion.execute(
                "SELECT estado, total FROM pedidos WHERE numero_pedido = ?", (numero,)
            ).fetchone()
            self.assertEqual(fila["estado"], "PAGADO")
            self.assertEqual(fila["total"], 155)
        html = self.cliente.get("/caja", query_string={"numero": numero}).get_data(as_text=True)
        self.assertIn("PAGADO", html)
        self.assertNotIn("Confirmar pago", html)
        self.assertNotIn("Cancelar pedido", html)

    def test_qr_del_pedido_abre_caja_con_su_numero_filtrado(self):
        self.crear_pedido("Carlos")
        with patch.dict(os.environ, {"PUBLIC_BASE_URL": "https://cafeteria.example"}):
            with patch("app.segno.make_qr", wraps=segno.make_qr) as generar:
                respuesta = self.cliente.post("/api/pedidos", json={
                    "nombre_cliente": "María",
                    "productos": [{"id": 1, "cantidad": 1}],
                })

        self.assertEqual(respuesta.status_code, 201)
        datos = respuesta.get_json()
        numero = datos["numero_pedido"]
        generar.assert_called_once_with(
            f"https://cafeteria.example/caja?numero={numero}", error="m"
        )
        self.assertTrue(datos["codigo_qr"].startswith("data:image/svg+xml;base64,"))
        imagen = base64.b64decode(datos["codigo_qr"].split(",", 1)[1])
        self.assertIn(b"<svg", imagen)

        caja = self.cliente.get("/caja", query_string={"numero": numero})
        html = caja.get_data(as_text=True)
        self.assertEqual(caja.status_code, 200)
        self.assertIn(f'value="{numero}"', html)
        self.assertIn("María", html)
        self.assertNotIn("Carlos", html)

        with patch.dict(os.environ, {"PUBLIC_BASE_URL": ""}):
            with patch("app.segno.make_qr", wraps=segno.make_qr) as generar_local:
                numero_local = self.crear_pedido("Luis")
        generar_local.assert_called_once_with(
            f"http://localhost/caja?numero={numero_local}", error="m"
        )

    def test_cancelar_no_borra_detalles_y_no_permite_pagar_despues(self):
        numero = self.crear_pedido()
        self.assertEqual(self.cambiar(numero, "CANCELADO").status_code, 200)
        self.assertEqual(self.cambiar(numero, "PAGADO").status_code, 400)
        pedido = database.obtener_pedidos()[0]
        self.assertEqual(pedido["estado"], "CANCELADO")
        self.assertEqual(len(pedido["productos"]), 2)

    def test_acciones_repetidas_y_transiciones_invalidas(self):
        numero = self.crear_pedido()
        self.assertEqual(self.cambiar(numero, "LISTO").status_code, 400)
        self.assertEqual(self.cambiar(numero, None).status_code, 400)
        self.assertEqual(self.cambiar(numero, {}).status_code, 400)
        self.assertEqual(self.cambiar(numero, "PAGADO").status_code, 200)
        self.assertEqual(self.cambiar(numero, "PAGADO").status_code, 400)
        self.assertEqual(self.cambiar(numero, "CANCELADO").status_code, 400)
        self.assertEqual(database.obtener_pedidos()[0]["estado"], "PAGADO")

    def test_pedido_inexistente_y_peticion_invalida(self):
        self.assertEqual(self.cambiar(999, "PAGADO").status_code, 404)
        self.assertEqual(self.cambiar(2**63, "PAGADO").status_code, 400)
        self.assertEqual(self.cliente.post("/api/pedidos/1/estado").status_code, 400)
        self.assertEqual(self.cliente.get("/api/pedidos/1/estado").status_code, 405)

    def test_busqueda_invalida_y_sin_resultados(self):
        self.crear_pedido()
        for valor in ("abc", "0", "-1", "1 OR 1=1", str(2**63), "9" * 100):
            html = self.cliente.get("/caja", query_string={"numero": valor}).get_data(as_text=True)
            self.assertIn("Ingresa un número de pedido válido", html)
        html = self.cliente.get("/caja?numero=999").get_data(as_text=True)
        self.assertIn("No se encontraron pedidos", html)

    def test_caja_vacia_y_regresion_menu(self):
        self.assertIn("No hay pedidos registrados", self.cliente.get("/caja").get_data(as_text=True))
        self.assertEqual(self.cliente.get("/").status_code, 200)
        self.assertEqual(self.cliente.get("/menu").status_code, 200)


if __name__ == "__main__":
    unittest.main()
