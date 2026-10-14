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

## Código QR de pedidos

Al confirmar un pedido, la página muestra un QR que abre `/caja` con el número
del pedido en el filtro de búsqueda. Para escanearlo desde otro dispositivo,
el servidor debe ser accesible desde ese dispositivo. Puedes configurar
`PUBLIC_BASE_URL` con su dirección, por ejemplo:

```powershell
$env:PUBLIC_BASE_URL = "http://192.168.1.10:5000"
flask --app app run --host 0.0.0.0
```

Si no configuras `PUBLIC_BASE_URL`, el QR usa la dirección con la que se hizo
el pedido. Una dirección `localhost` solo funciona en el mismo dispositivo.
