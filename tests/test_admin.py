import io
import tempfile
import unittest
from pathlib import Path

import database
from ayuda_acceso import autenticar

with tempfile.TemporaryDirectory() as temporal_importacion:
    base_original = database.DATABASE
    database.DATABASE = str(Path(temporal_importacion) / "importacion.db")
    from app import app
    database.DATABASE = base_original


class AdministracionTest(unittest.TestCase):
    def setUp(self):
        self.temporal = tempfile.TemporaryDirectory()
        self.base_original = database.DATABASE
        database.DATABASE = str(Path(self.temporal.name) / "admin.db")
        database.crear_tablas()
        database.insertar_productos_iniciales()
        self.cliente = app.test_client()
        self.carpeta_imagenes_original = app.config["CARPETA_IMAGENES_PRODUCTOS"]
        app.config["CARPETA_IMAGENES_PRODUCTOS"] = str(Path(self.temporal.name) / "imagenes")
        autenticar(self.cliente)
        self.datos = {"nombre": "Pan de prueba", "descripcion": "Recién horneado",
                      "categoria": "Panadería", "precio": "22.50", "disponible": True}

    def tearDown(self):
        app.config["CARPETA_IMAGENES_PRODUCTOS"] = self.carpeta_imagenes_original
        database.DATABASE = self.base_original
        self.temporal.cleanup()

    def test_crear_editar_y_reflejar_en_menu(self):
        self.assertEqual(self.cliente.get("/admin").status_code, 200)
        respuesta = self.cliente.post("/api/productos", json=self.datos)
        self.assertEqual(respuesta.status_code, 201)
        numero = respuesta.get_json()["id"]
        self.assertIn("Pan de prueba", self.cliente.get("/menu").get_data(as_text=True))
        self.datos.update(nombre="Pan integral", precio="25.75", descripcion="Con semillas", categoria="Alimentos")
        self.assertEqual(self.cliente.put(f"/api/productos/{numero}", json=self.datos).status_code, 200)
        producto = next(p for p in database.obtener_productos() if p["id"] == numero)
        self.assertEqual(producto["precio"], 25.75)
        self.assertEqual(producto["descripcion"], "Con semillas")
        html = self.cliente.get("/menu").get_data(as_text=True)
        self.assertIn("Pan integral", html)
        self.assertNotIn("Pan de prueba", html)

    def test_disponibilidad_rechaza_pedido_y_preserva_registros(self):
        pedido = database.crear_pedido("Ana", [{"id": 1, "cantidad": 2}])
        total_anterior = pedido["total"]
        url = "/api/productos/1/disponibilidad"
        self.assertEqual(self.cliente.patch(url, json={"disponible": False}).status_code, 200)
        html = self.cliente.get("/menu").get_data(as_text=True)
        self.assertIn("Tacos capeados", html)
        self.assertIn("Agotado", html)
        self.assertEqual(self.cliente.post("/api/pedidos", json={
            "nombre_cliente": "Luis", "productos": [{"id": 1, "cantidad": 1}],
        }).status_code, 400)
        registros = database.obtener_pedidos()
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["total"], total_anterior)
        self.assertEqual(registros[0]["productos"][0]["cantidad"], 2)
        self.assertEqual(self.cliente.patch(url, json={"disponible": True}).status_code, 200)
        database.crear_pedido("Luis", [{"id": 1, "cantidad": 1}])

    def test_validaciones_no_guardan_datos_parciales(self):
        cantidad = len(database.obtener_productos())
        for campo, valor in (("nombre", " "), ("categoria", ""), ("descripcion", "a" * 501),
                             ("nombre", "a" * 101), ("precio", "NaN"), ("precio", "Infinity"),
                             ("precio", "-1"), ("precio", "0"), ("precio", "1.234"),
                             ("precio", "1000000"), ("precio", True), ("disponible", "false")):
            with self.subTest(campo=campo, valor=valor):
                datos = {**self.datos, campo: valor}
                self.assertEqual(self.cliente.post("/api/productos", json=datos).status_code, 400)
                self.assertEqual(self.cliente.put("/api/productos/1", json=datos).status_code, 400)
        self.assertEqual(len(database.obtener_productos()), cantidad)
        self.assertEqual(next(p for p in database.obtener_productos() if p["id"] == 1)["nombre"], "Tacos capeados")

    def test_errores_de_peticion_y_producto_inexistente(self):
        self.assertEqual(self.cliente.post("/api/productos", json=[]).status_code, 400)
        self.assertEqual(self.cliente.post("/api/productos").status_code, 400)
        self.assertEqual(self.cliente.put("/api/productos/999", json=self.datos).status_code, 404)
        self.assertEqual(self.cliente.put(f"/api/productos/{2**63}", json=self.datos).status_code, 400)
        self.assertEqual(self.cliente.patch("/api/productos/999/disponibilidad", json={"disponible": True}).status_code, 404)
        self.assertEqual(self.cliente.patch("/api/productos/1/disponibilidad", json={"disponible": 0}).status_code, 400)
        self.assertEqual(self.cliente.delete("/api/productos/999").status_code, 404)

    def test_agregar_reemplazar_y_quitar_imagen(self):
        datos = {
            **{clave: str(valor) for clave, valor in self.datos.items() if clave != "disponible"},
            "disponible": "true",
            "quitar_imagen": "false",
            "imagen": (io.BytesIO(b"\xff\xd8\xff\xe0imagen-jpeg"), "pan.jpg"),
        }
        respuesta = self.cliente.post(
            "/api/productos", data=datos, content_type="multipart/form-data"
        )
        self.assertEqual(respuesta.status_code, 201)
        producto = respuesta.get_json()
        primera = producto["imagen"]
        self.assertTrue(primera.startswith("img/productos/"))
        self.assertTrue((Path(app.config["CARPETA_IMAGENES_PRODUCTOS"]) / Path(primera).name).is_file())
        self.assertIn(primera, self.cliente.get("/menu").get_data(as_text=True))

        datos["imagen"] = (io.BytesIO(b"\x89PNG\r\n\x1a\nimagen-png"), "pan.png")
        respuesta = self.cliente.put(
            f"/api/productos/{producto['id']}", data=datos, content_type="multipart/form-data"
        )
        self.assertEqual(respuesta.status_code, 200)
        segunda = respuesta.get_json()["imagen"]
        self.assertNotEqual(primera, segunda)
        self.assertFalse((Path(app.config["CARPETA_IMAGENES_PRODUCTOS"]) / Path(primera).name).exists())

        datos.pop("imagen")
        datos["quitar_imagen"] = "true"
        respuesta = self.cliente.put(
            f"/api/productos/{producto['id']}", data=datos, content_type="multipart/form-data"
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertIsNone(respuesta.get_json()["imagen"])
        self.assertFalse((Path(app.config["CARPETA_IMAGENES_PRODUCTOS"]) / Path(segunda).name).exists())

    def test_imagen_invalida_y_borrado_protegido(self):
        datos = {
            **{clave: str(valor) for clave, valor in self.datos.items() if clave != "disponible"},
            "disponible": "true",
            "quitar_imagen": "false",
            "imagen": (io.BytesIO(b"esto no es una imagen"), "archivo.txt"),
        }
        self.assertEqual(self.cliente.post(
            "/api/productos", data=datos, content_type="multipart/form-data"
        ).status_code, 400)

        creado = self.cliente.post("/api/productos", json=self.datos).get_json()
        self.assertEqual(self.cliente.delete(f"/api/productos/{creado['id']}").status_code, 200)
        self.assertNotIn(creado["id"], [p["id"] for p in database.obtener_productos()])

        database.crear_pedido("Ana", [{"id": 1, "cantidad": 1}])
        respuesta = self.cliente.delete("/api/productos/1")
        self.assertEqual(respuesta.status_code, 409)
        self.assertIn("pedidos", respuesta.get_json()["error"])
        self.assertIn(1, [p["id"] for p in database.obtener_productos()])

    def test_renombrar_no_recrea_productos_iniciales(self):
        producto = next(p for p in database.obtener_productos() if p["id"] == 1)
        producto.update(nombre="Tacos especiales", disponible=False)
        database.guardar_producto(producto, 1)
        cantidad = len(database.obtener_productos())
        database.insertar_productos_iniciales()
        productos = database.obtener_productos()
        self.assertEqual(len(productos), cantidad)
        self.assertNotIn("Tacos capeados", [p["nombre"] for p in productos])
        self.assertEqual(next(p for p in productos if p["id"] == 1)["disponible"], 0)

    def test_textos_se_muestran_escapados(self):
        self.datos["nombre"] = '<b>Pan "especial"</b>'
        self.assertEqual(self.cliente.post("/api/productos", json=self.datos).status_code, 201)
        for ruta in ("/admin", "/menu"):
            html = self.cliente.get(ruta).get_data(as_text=True)
            self.assertNotIn('<b>Pan "especial"</b>', html)
            self.assertIn("&lt;b&gt;", html)


if __name__ == "__main__":
    unittest.main()
