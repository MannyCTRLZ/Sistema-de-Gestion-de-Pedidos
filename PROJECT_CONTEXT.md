# PROJECT_CONTEXT.md
# Sistema de Gestión de Pedidos para Cafetería

## 1. Contexto académico

Este proyecto se desarrolla para una materia de **Gestión de Proyectos de Software** a lo largo de un semestre de **16 semanas**.

El objetivo no es quedarse en una propuesta conceptual: al final del semestre debe existir un **software funcional y demostrable**.

El anteproyecto contempla al menos:
- Planteamiento del problema.
- Justificación.
- Hipótesis.
- Objetivo general.
- Objetivos específicos.
- Metodología.
- Cronograma.
- Conclusión.

## 2. Idea seleccionada

Se eligió desarrollar un:

**Sistema web de gestión y realización de pedidos para una cafetería universitaria.**

Se evaluó también un gestor de proyectos para estudiantes, pero se descartó porque el sistema de cafetería tiene un alcance más controlable y menor riesgo para un equipo sin experiencia previa y con un límite de 16 semanas.

## 3. Problema que busca resolver

En una cafetería escolar con alta afluencia pueden presentarse:
- Filas para realizar pedidos.
- Tiempos de espera innecesarios.
- Errores al tomar pedidos.
- Falta de organización entre pedido, caja y preparación.
- Dificultad para consultar el estado de cada pedido.

El sistema busca digitalizar y organizar el proceso de realización, pago y seguimiento de pedidos.

## 4. Regla principal del proyecto

**Los estudiantes/clientes NO crean una cuenta y NO inician sesión.**

La experiencia debe ser rápida, similar a un sistema de autoservicio de comida rápida.

El estudiante:
1. Abre la página web.
2. Consulta el menú.
3. Selecciona productos.
4. Revisa el carrito.
5. Ingresa únicamente el nombre para el pedido.
6. Confirma.
7. Recibe un número de pedido.
8. Pasa a caja a pagar.

No se solicita al cliente:
- Correo.
- Contraseña.
- Teléfono.
- Dirección.
- Registro.
- Cuenta de usuario.

## 5. Localizador físico

La cafetería ya cuenta con localizadores físicos que la cajera entrega después del pago.

El localizador:
- Es parte del proceso real de la cafetería.
- NO forma parte del desarrollo.
- NO se comunicará con nuestro software.
- NO se implementará Bluetooth, RF, Arduino, sensores ni ningún mecanismo de activación.

El software solo puede registrar que un pedido cambió a estado **LISTO**. La notificación física al estudiante queda fuera del alcance.

## 6. Flujo general

Cliente:
Menú -> Selección de productos -> Carrito -> Nombre -> Confirmar -> Número de pedido

Caja:
Número de pedido -> Ver pedido -> Cobrar físicamente -> Confirmar pago -> Entregar localizador físico

Cocina:
Ver pedidos pagados -> Comenzar preparación -> Marcar como listo

Entrega:
El personal entrega el pedido físicamente y el sistema puede marcarlo como entregado.

## 7. Usuarios y áreas

### Cliente / estudiante
No requiere cuenta.

Puede:
- Consultar menú.
- Ver productos disponibles.
- Agregar productos al carrito.
- Aumentar/disminuir cantidades.
- Eliminar productos.
- Ver subtotal y total.
- Ingresar nombre.
- Confirmar pedido.
- Obtener número de pedido.

### Personal de cafetería
El acceso interno sí debe estar protegido.

Para reducir complejidad en el MVP se puede comenzar con una sola cuenta o tipo de acceso interno y separar después permisos/roles.

Las vistas lógicas del personal son:

#### Caja
- Ver pedidos pendientes de pago.
- Buscar un pedido por número.
- Ver detalle y total.
- Confirmar pago.
- Cancelar un pedido cuando corresponda.

#### Cocina
- Ver pedidos pagados.
- Ver detalle de productos y cantidades.
- Cambiar a "En preparación".
- Cambiar a "Listo".

#### Administración
- Crear productos.
- Editar productos.
- Cambiar precios.
- Editar descripción/categoría.
- Activar o desactivar disponibilidad.
- Consultar pedidos.
- Agregar estadísticas en una fase posterior si el tiempo lo permite.

## 8. MVP

El MVP se considera terminado cuando se pueda demostrar de principio a fin:

1. El cliente abre el menú.
2. Agrega productos.
3. Modifica el carrito.
4. Ve el total.
5. Ingresa su nombre.
6. Confirma el pedido.
7. El sistema genera un número.
8. El pedido aparece en caja como "Pendiente de pago".
9. Caja confirma el pago.
10. El pedido aparece para cocina.
11. Cocina cambia a "En preparación".
12. Cocina cambia a "Listo".
13. El pedido puede marcarse como "Entregado".

## 9. Estados del pedido

Estados definidos para el MVP:

- PENDIENTE DE PAGO
- PAGADO
- EN PREPARACIÓN
- LISTO
- ENTREGADO
- CANCELADO

Flujo normal:

PENDIENTE DE PAGO -> PAGADO -> EN PREPARACIÓN -> LISTO -> ENTREGADO

CANCELADO es un estado alternativo.

## 10. Funcionalidades obligatorias del MVP

### Menú
Cada producto debe manejar como mínimo:
- Nombre.
- Descripción.
- Precio.
- Categoría.
- Disponibilidad.

### Carrito
Debe permitir:
- Agregar producto.
- Aumentar cantidad.
- Disminuir cantidad.
- Eliminar producto.
- Vaciar carrito.
- Calcular subtotal.
- Calcular total.

### Confirmación
- Campo para nombre del pedido.
- Validación de nombre no vacío.
- Creación del pedido.
- Número de pedido generado automáticamente.

### Caja
- Listado de pedidos pendientes.
- Visualización de detalle.
- Confirmación de pago.

### Cocina
- Listado de pedidos pagados/en preparación.
- Cambio de estado.

### Administración
- Alta de producto.
- Edición de producto.
- Disponibilidad.
- Precio.
- Categoría.

## 11. Fuera del MVP / fuera de alcance inicial

No incluir de inicio:
- Registro de estudiantes.
- Login de clientes.
- Aplicación móvil nativa.
- Pagos en línea.
- Tarjetas bancarias.
- Integración con terminal bancaria.
- Integración con localizadores físicos.
- SMS.
- Correo electrónico.
- Sistema de puntos.
- Cupones.
- Delivery.
- Inteligencia artificial.
- Predicción de ventas.
- Integraciones externas.
- React.
- Node.js.
- PostgreSQL.

Estas funciones solo podrían considerarse después de completar el MVP.

## 12. Tecnologías elegidas

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Base de datos
- SQLite

### Desarrollo y control de versiones
- Visual Studio Code
- Git
- GitHub

## 13. Razón de la elección tecnológica

El equipo no tiene experiencia previa con las tecnologías evaluadas.

Se eligió **HTML + CSS + JavaScript + Python + Flask + SQLite** porque:
- Tiene menor curva de aprendizaje.
- Evita aprender React al mismo tiempo.
- Evita configurar un servidor PostgreSQL.
- SQLite funciona como un archivo local.
- Flask permite una arquitectura sencilla para principiantes.
- Es suficiente para el volumen esperado de una cafetería escolar y para el MVP.
- Reduce el riesgo de no terminar en 16 semanas.
- Permite crecer posteriormente.

No se eligió React + FastAPI + PostgreSQL porque, aunque es una arquitectura válida y más escalable, introduce más conceptos y configuración de los necesarios para este proyecto y nivel actual del equipo.

## 14. Arquitectura general

Navegador
-> HTML + CSS + JavaScript
-> Flask / Python
-> SQLite

Flask sirve las plantillas HTML y gestiona la lógica del sistema.

## 15. Base de datos propuesta

### usuarios
Para acceso interno del personal.

Campos iniciales:
- id
- usuario
- password / hash_password
- rol

### productos
- id
- nombre
- descripcion
- precio
- categoria
- disponible

### pedidos
- id
- numero_pedido
- nombre_cliente
- fecha
- estado
- total

### detalle_pedido
- id
- pedido_id
- producto_id
- cantidad
- precio

Relación principal:

pedido 1 -> N detalle_pedido N -> 1 producto

## 16. Estructura inicial del repositorio

Nombre actual del repositorio/proyecto:

`Sistema-de-Gestion-de-Pedidos`

Estructura objetivo inicial:

```text
Sistema-de-Gestion-de-Pedidos/
├── .venv/
├── .gitignore
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_CONTEXT.md
├── SPRINT_STATUS.md
├── AGENTS.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── styles.css
    ├── js/
    │   └── main.js
    └── img/
```

`.venv/` no debe subirse al repositorio.

## 17. Entorno observado al comenzar

En la máquina principal se verificó:
- Python 3.14.4
- Git 2.53.0
- SQLite 3.46.1
- VS Code 1.137.0
- Entorno virtual `.venv` activo

La carpeta del proyecto ya contiene al menos:
- `.venv/`
- `app.py`
- `requirements.txt`
- `templates/index.html`
- `static/`
- `.gitignore`
- README/bitácora existentes

## 18. Plan de desarrollo del frontend

La conversación de desarrollo actual se decidió enfocar primero en el **frontend**.

Orden propuesto:

1. Crear estructura HTML base.
2. Diseñar encabezado/navegación.
3. Crear sección de menú.
4. Crear tarjetas de productos.
5. Hacer diseño responsive.
6. Crear carrito visual.
7. Agregar JavaScript para:
   - agregar productos,
   - cambiar cantidades,
   - eliminar,
   - actualizar total,
   - contador del carrito.
8. Crear formulario para nombre.
9. Crear pantalla visual de confirmación/número.
10. Después conectar el frontend con Flask y SQLite.

## 19. Primera pantalla prevista

La primera pantalla debe incluir:
- Nombre/logo de cafetería.
- Navegación sencilla.
- Botón/indicador del carrito.
- Título tipo "¿Qué quieres ordenar?"
- Categorías/filtros (opcional al inicio).
- Tarjetas de productos.
- Botón Agregar.

Para empezar pueden usarse productos ficticios:
- Hamburguesa sencilla.
- Burrito.
- Refresco.

No se busca un diseño final desde el primer commit. Primero estructura, después estilo, luego interactividad.

## 20. Convenciones para avanzar

- Trabajar incrementalmente.
- No construir todo de golpe.
- Cada fase debe funcionar antes de avanzar.
- Priorizar el MVP.
- Evitar incorporar tecnologías nuevas sin una necesidad clara.
- Mantener requisitos y decisiones en este archivo.
- Si una decisión cambia, actualizar este archivo.
- Nunca guardar contraseñas reales, tokens o secretos en Git.
- Usar `.gitignore` para `.venv`, cachés y archivos secretos.
- Antes de cambios grandes, revisar el estado actual del repositorio.

## 21. Plan aproximado de 16 semanas

- Semanas 1–2: anteproyecto, problema, alcance y requisitos.
- Semana 3: HTML y CSS.
- Semana 4: JavaScript básico.
- Semana 5: Python y Flask.
- Semana 6: diseño de base de datos.
- Semana 7: menú/productos.
- Semana 8: carrito.
- Semana 9: creación de pedidos.
- Semana 10: caja.
- Semana 11: cocina.
- Semana 12: administración.
- Semana 13: mejoras visuales y responsive.
- Semana 14: pruebas.
- Semana 15: correcciones.
- Semana 16: documentación y presentación.

Este cronograma es orientativo y puede ajustarse según avance real.

## 22. Regla para asistentes/agentes de programación

Antes de modificar código:
1. Leer `PROJECT_CONTEXT.md`.
<<<<<<< HEAD
2. Revisar la estructura y estado actual del repositorio.
3. No asumir funcionalidades que no estén definidas.
4. Priorizar una implementación sencilla entendible por principiantes.
5. Explicar cambios importantes.
6. No agregar frameworks o dependencias sin justificar su necesidad.
7. Mantener el alcance del MVP.
8. No modificar o publicar repositorios remotos sin autorización explícita del usuario.

## 23. Estrategia de ramas

El equipo trabajará con cuatro ramas:

- `main`: versión estable y demostrable del proyecto.
- `dev`: integración y pruebas conjuntas del frontend y el backend.
- `frontend`: trabajo del flujo visual y la interacción del cliente.
- `backend`: trabajo de Flask, SQLite y la lógica del servidor.

Flujo de integración:

1. Cada integrante trabaja y crea commits en su rama (`frontend` o `backend`).
2. El trabajo terminado y probado se integra en `dev`.
3. En `dev` se comprueba que frontend y backend funcionen juntos.
4. Solo una versión estable de `dev` se integra en `main`.

No se debe desarrollar directamente en `main`. Antes de modificar archivos compartidos,
especialmente plantillas HTML o `app.py`, el equipo debe coordinarse para reducir conflictos.
=======
2. Leer `SPRINT_STATUS.md`.
3. Revisar la estructura y estado actual del repositorio.
4. No asumir funcionalidades que no estén definidas.
5. Priorizar una implementación sencilla entendible por principiantes.
6. Explicar cambios importantes.
7. No agregar frameworks o dependencias sin justificar su necesidad.
8. Mantener el alcance del MVP.
9. No modificar o publicar repositorios remotos sin autorización explícita del usuario.

## 23. Plan de desarrollo Scrum: 10 sprints / 10 semanas

Cada sprint dura una semana y debe terminar con un incremento funcional y demostrable. El contenido de los próximos sprints puede ajustarse según lo aprendido, pero sin ampliar el MVP ni comprometer la meta final.

| Sprint | Meta | Acciones principales | Incremento entregable |
|---|---|---|---|
| 1. Preparación y estructura | Tener el entorno y la base inicial funcionando. | Configurar herramientas, Git, entorno virtual, Flask, carpetas y página inicial. | Aplicación Flask ejecutándose localmente y mostrando la página inicial. |
| 2. Base de datos y productos | Almacenar y recuperar productos desde SQLite. | Diseñar la base de datos, crear la tabla `productos`, insertar datos de prueba y conectar Flask con SQLite. | Productos almacenados en SQLite y recuperados correctamente desde Flask. |
| 3. Menú de la cafetería | Mostrar un menú funcional obtenido desde la base de datos. | Crear catálogo y categorías; mostrar nombre, descripción, precio y disponibilidad; adaptar la interfaz a celular. | Página que muestra dinámicamente los productos disponibles. |
| 4. Carrito de compras | Permitir construir y revisar un pedido. | Agregar y eliminar productos, modificar cantidades y calcular subtotal y total con JavaScript. | El estudiante selecciona productos y revisa su carrito completo. |
| 5. Creación del pedido | Registrar pedidos reales en la base de datos. | Crear las tablas `pedidos` y `detalle_pedido`, solicitar el nombre, validar el carrito, generar el número y guardar el pedido. | Flujo Menú → Carrito → Nombre → Número de pedido funcional. |
| 6. Módulo de caja | Recibir y confirmar pedidos. | Crear el panel de caja, consultar pendientes, mostrar detalles, buscar por número y confirmar el pago físico. | Un pedido aparece en caja y cambia de Pendiente de pago a Pagado. |
| 7. Módulo de cocina | Gestionar la preparación de pedidos pagados. | Mostrar pedidos pagados y agregar controles para cambiar sus estados. | Flujo Pagado → En preparación → Listo → Entregado funcional. |
| 8. Administración | Administrar el menú sin modificar código. | Crear el panel y el CRUD de productos: agregar, editar y activar o desactivar disponibilidad. | Los cambios administrativos aparecen en el menú del estudiante. |
| 9. Integración, seguridad y pruebas | Integrar módulos y corregir problemas importantes. | Añadir validaciones, proteger el área interna, manejar errores, probar el flujo completo y mejorar el diseño responsive. | Versión candidata completa y estable. |
| 10. MVP final y entrega | Preparar el software para su demostración. | Ejecutar pruebas finales, preparar datos de demostración, mejorar la presentación, documentar y respaldar el repositorio. | MVP terminado, documentado y demostrable de principio a fin. |

### Ciclo semanal

- Inicio: Sprint Planning y selección del Sprint Backlog.
- Durante la semana: desarrollo y Daily Scrum breve.
- Final: Sprint Review del incremento y Sprint Retrospective.

### Criterio de entrega final

La demostración debe ejecutar el flujo completo sin modificar código ni datos manualmente:

Menú → Carrito → Nombre → Número de pedido → Caja → Pago confirmado → Cocina → En preparación → Listo → Entregado.

Los sprints 9 y 10 reservan tiempo para integración, correcciones y entrega. Las estadísticas, promociones, pagos en línea, notificaciones e integración con localizadores físicos permanecen fuera del MVP.

## 24. Seguimiento compartido y ramas

- `SPRINT_STATUS.md` registra el sprint activo, tareas, responsables, ramas, impedimentos y avance integrado.
- La versión integrada en `main` es la única fuente oficial del estado.
- Las ramas de trabajo pueden tener diferencias temporales, pero no deben mantener planes oficiales independientes.
- Se recomienda una rama por funcionalidad, no una rama permanente por integrante.
- Una tarea puede estar en progreso o terminada en su rama, pero solo se considera parte del incremento cuando se prueba e integra en `main`.
- Para reducir conflictos, el equipo debe acordar quién actualiza `SPRINT_STATUS.md` al integrar trabajo.
>>>>>>> main
