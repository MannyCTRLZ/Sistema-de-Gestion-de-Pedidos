# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 5 — Creación del pedido**

Estado: **COMPLETADO**

## Objetivo del sprint

Registrar pedidos reales a partir del carrito y entregar un número de pedido al estudiante.

## Incremento esperado

Flujo Menú → Carrito → Nombre → Número de pedido funcional.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Agregar el botón para continuar desde el carrito | Equipo | Integrada en `main` | `main` |
| Crear el formulario para el nombre del pedido | Equipo | Integrada en `main` | `main` |
| Validar que el nombre no esté vacío | Equipo | Integrada en `main` | `main` |
| Mostrar el resumen previo del pedido | Equipo | Integrada en `main` | `main` |
| Permitir editar el nombre y volver al carrito | Equipo | Integrada en `main` | `main` |
| Crear las tablas `pedidos` y `detalle_pedido` | Equipo | Integrada en `main` | `main` |
| Validar productos y precios en Flask | Equipo | Integrada en `main` | `main` |
| Guardar el pedido y su detalle | Equipo | Integrada en `main` | `main` |
| Generar el número de pedido | Equipo | Integrada en `main` | `main` |
| Mostrar la confirmación final | Equipo | Integrada en `main` | `main` |
| Probar la persistencia completa | Equipo | Integrada en `main` | `main` |

## Trabajo integrado en `main`

- El carrito incluye un botón para continuar que solo se habilita cuando contiene productos.
- El estudiante puede ingresar únicamente el nombre que usará en caja.
- El formulario rechaza nombres vacíos.
- La interfaz muestra un resumen con nombre, productos, cantidades y total.
- El estudiante puede editar el nombre o regresar al carrito sin perder su selección.
- Flask recibe el nombre y las cantidades mediante `POST /api/pedidos`.
- Los precios y la disponibilidad se validan nuevamente desde SQLite.
- El pedido y sus detalles se guardan en una sola transacción.
- La confirmación final muestra número, estado y total calculados por el servidor.

## Trabajo verificado localmente

- Se comprobó que el botón para continuar aparece habilitado con productos en el carrito.
- Se verificó el mensaje de error al intentar continuar con un nombre vacío.
- El resumen mostró correctamente el nombre `María`, tres unidades y un total de `$170.00`.
- Se verificó que editar el nombre conserva los datos capturados.
- Se regresó al carrito y se confirmó que los productos y cantidades permanecen intactos.
- Se verificó la creación de `pedidos` y `detalle_pedido` con claves foráneas activas.
- Flask recalculó el total desde SQLite y rechazó un producto agotado sin guardar datos parciales.
- El flujo completo generó el pedido `#0001`, con estado `PENDIENTE DE PAGO` y total `$170.00`.
- La base temporal conservó un pedido y dos detalles sin violaciones de integridad referencial.

## Sprint Review

- Se verificó el flujo completo Menú → Carrito → Nombre → Número de pedido.
- El incremento cumple el objetivo del Sprint 5 y quedó integrado localmente en `main`.

## Sprint Retrospective

- Separar la revisión visual del guardado permitió conectar el backend de forma incremental.
- Recalcular precios y disponibilidad en Flask evita confiar en datos modificables del navegador.
- Las pruebas con una base temporal permitieron validar transacciones sin contaminar los datos locales.

## Impedimentos

Ninguno documentado.

## Criterios para cerrar el sprint

- Existen las tablas `pedidos` y `detalle_pedido`.
- El nombre del pedido se valida en frontend y backend.
- Flask valida productos, disponibilidad, cantidades y precios.
- El pedido y sus detalles se guardan en una sola transacción.
- Se genera un número de pedido único.
- La confirmación final muestra el número y el total real almacenado.
- El pedido queda registrado como `PENDIENTE DE PAGO`.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

- Actualizar este archivo cuando una tarea se asigne, cambie de estado, se integre o quede bloqueada.
- Acordar una sola persona para integrar cada actualización y evitar ediciones simultáneas.
- Usar estados claros: `Pendiente`, `En progreso`, `Terminada en rama`, `Integrada en main` o `Bloqueada`.
- Al cerrar el sprint, registrar el resultado de la Review y la Retrospective antes de preparar el siguiente Sprint Backlog.

## Sprints anteriores

### Sprint 4 — Carrito de compras

Estado: **COMPLETADO**

Incremento verificado en `main`: el estudiante puede agregar productos, modificar cantidades, eliminar, vaciar y revisar el total de su carrito.

#### Sprint Review

- El contador y el total se actualizan después de cada cambio.
- Los productos repetidos se agrupan y los agotados no pueden agregarse.
- El panel lateral funciona en escritorio y se adapta a pantallas pequeñas.

#### Sprint Retrospective

- La delegación de eventos simplificó los controles creados dinámicamente.
- Mantener el carrito en JavaScript evitó adelantar la persistencia del Sprint 5.
- El servidor deberá validar nuevamente todos los datos antes de guardar pedidos.

### Sprint 3 — Menú de la cafetería

Estado: **COMPLETADO**

Incremento verificado en `main`: el menú obtiene los productos desde SQLite, muestra sus datos y presenta los productos no disponibles como agotados con el botón deshabilitado.

#### Sprint Review

- Las tarjetas se generan dinámicamente con Flask y Jinja.
- Cada producto muestra nombre, descripción, categoría, precio y disponibilidad.
- Se verificaron el diseño responsive y el estado sin productos registrados.

#### Sprint Retrospective

- Reutilizar el diseño existente permitió conectar el frontend sin ampliar el alcance.
- Las pruebas con una base temporal permitieron verificar la disponibilidad sin alterar los datos locales.
- La lógica del carrito se mantuvo separada de la consulta de productos.

### Sprint 2 — Base de datos y productos

Estado: **COMPLETADO**

Incremento verificado en `main`: la tabla `productos` se crea automáticamente, los productos de prueba se almacenan en SQLite y Flask recupera únicamente los productos disponibles.

#### Sprint Backlog completado

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Diseñar la tabla `productos` | Equipo | Integrada en `main` | `main` |
| Crear la conexión entre Python y SQLite | Equipo | Integrada en `main` | `main` |
| Crear automáticamente la tabla `productos` | Equipo | Integrada en `main` | `main` |
| Insertar productos de prueba | Equipo | Integrada en `main` | `main` |
| Crear una consulta para obtener productos disponibles | Equipo | Integrada en `main` | `main` |
| Recuperar los productos desde la ruta de Flask | Equipo | Integrada en `main` | `main` |
| Verificar la creación y consulta de datos | Equipo | Integrada en `main` | `main` |

#### Sprint Review

- Se verificó la persistencia de tres productos de prueba en `cafeteria.db`.
- La consulta devuelve solo productos con `disponible = 1`.
- Flask recupera los productos y responde correctamente en la ruta del menú.
- El incremento cumple el objetivo definido para el Sprint 2.

#### Sprint Retrospective

- Funcionó bien separar la conexión, creación de tablas y consultas en `database.py`.
- Se debe mantener coordinada la edición de archivos compartidos para evitar conflictos de integración.
- En los siguientes sprints se continuará probando cada incremento antes de marcarlo como completado.

### Sprint 1 — Preparación y estructura

Estado: **COMPLETADO**

Incremento verificado en el repositorio: aplicación Flask local con página inicial y estructura base de archivos.
