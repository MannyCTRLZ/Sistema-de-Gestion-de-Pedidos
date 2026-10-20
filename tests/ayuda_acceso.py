import re

from acceso import crear_personal

USUARIO_PRUEBA = "personal-prueba"
PASSWORD_PRUEBA = "solo-para-pruebas-2026"


def autenticar(cliente, crear=True):
    if crear:
        crear_personal(USUARIO_PRUEBA, PASSWORD_PRUEBA)
    html = cliente.get("/login").get_data(as_text=True)
    token = re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)
    respuesta = cliente.post("/login", data={
        "usuario": USUARIO_PRUEBA, "password": PASSWORD_PRUEBA, "csrf_token": token,
    })
    assert respuesta.status_code == 302
    cliente.get("/caja")
    with cliente.session_transaction() as sesion:
        cliente.environ_base["HTTP_X_CSRF_TOKEN"] = sesion["csrf"]
