# Sistema-de-Gestion-de-Pedidos

## Ejecutar el sistema

En PowerShell, activa el entorno del proyecto y ejecuta la aplicación:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Si PowerShell impide activar scripts, puedes iniciar la aplicación sin activar
el entorno con `.\.venv\Scripts\python.exe app.py`. En VS Code, selecciona
`.venv\Scripts\python.exe` como intérprete del proyecto.

## Ticket y código QR de pedidos

Al confirmar un pedido, la página muestra un ticket con nombre, número,
productos, cantidades, total y QR. El botón «Guardar imagen del ticket» descarga
un PNG para que el estudiante lo muestre en caja. El QR abre `/caja` con el
número del pedido en el filtro de búsqueda. Para escanearlo desde otro dispositivo, el servidor debe
ser accesible desde ese dispositivo. Puedes configurar `PUBLIC_BASE_URL` con
su dirección, por ejemplo:

```powershell
$env:PUBLIC_BASE_URL = "http://192.168.1.10:5000"
flask --app app run --host 0.0.0.0
```

En Render, si `PUBLIC_BASE_URL` está vacío, se usa automáticamente
`RENDER_EXTERNAL_URL` (la URL pública HTTPS del servicio). Para un dominio
propio, configura `PUBLIC_BASE_URL` con esa dirección. Fuera de Render, si no
configuras ninguna de las dos, el QR usa la dirección con la que se hizo el
pedido. Una dirección `localhost` solo funciona en el mismo dispositivo.
Si quedó un valor antiguo de `PUBLIC_BASE_URL` con `localhost` en Render,
elimínalo o sustitúyelo por la URL pública.

## Acceso interno del personal (Sprint 9)

Antes de usar caja, cocina o administración, crea una cuenta desde la terminal:

```bash
.venv/bin/python -m flask --app app crear-personal
.venv/bin/python app.py
```

En PowerShell:

```powershell
.\.venv\Scripts\python.exe -m flask --app app crear-personal
.\.venv\Scripts\python.exe app.py
```

El comando pide el usuario y una contraseña de 12 a 128 caracteres, sin mostrarla
en pantalla. No existe cuenta ni contraseña por defecto. SQLite guarda únicamente
su hash. No agregues credenciales reales al código, ejemplos, capturas o Git.

Entra por «Personal» en la portada o por `/login`. Una cuenta interna da acceso
a caja, cocina y administración; la separación por roles queda fuera de esta
primera cuenta compartida del MVP. El estudiante sigue usando menú, carrito y
confirmación sin cuenta.

El QR mantiene `/caja?numero=...` como atajo alternativo a la búsqueda manual.
Sin sesión muestra el acceso del personal y, al ingresar correctamente, recupera
ese número. Escanear el QR no autoriza a consultar ni modificar pedidos: el
servidor protege también las API. Si ya existe una sesión del personal en ese
navegador, puede abrir el pedido directamente; cierra sesión antes de entregar
un dispositivo a un estudiante.

Las sesiones duran como máximo ocho horas y se revocan en el servidor al cerrar
sesión. Los formularios y acciones internas verifican un token CSRF. Cinco
intentos fallidos bloquean temporalmente el acceso desde esa dirección durante
cinco minutos; el límite es local a cada proceso de Flask.

La clave de firma se genera automáticamente en `instance/session.key`, ignorada
por Git, y debe conservarse entre reinicios. También se puede proporcionar una
`SECRET_KEY` aleatoria de al menos 32 caracteres mediante el entorno. En un
despliegue con varios procesos usa la misma clave para todos.

Para publicar con HTTPS configura `COOKIE_SECURE=1` y los dominios permitidos en
`TRUSTED_HOSTS` (separados por comas). Define `PUBLIC_BASE_URL` con la URL http(s)
que deba codificar el QR. El servidor de desarrollo local usa HTTP y no activa
la cookie Secure por defecto. El modo debug está desactivado.

## Comprobación local

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Las pruebas crean cuentas ficticias y bases temporales; no necesitan credenciales
del personal ni modifican productos o pedidos reales.
