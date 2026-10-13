# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 6 — Módulo de caja**

Estado: **EN PROGRESO**

## Objetivo del sprint

Recibir los pedidos creados por los estudiantes y permitir confirmar su pago físico.

## Incremento esperado

Un pedido aparece en caja con su detalle y puede cambiar de Pendiente de pago a Pagado.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Crear la ruta y la interfaz de caja | Equipo | Integrada en `main` | `main` |
| Consultar los pedidos con sus productos desde SQLite | Equipo | Integrada en `main` | `main` |
| Mostrar número, cliente, fecha, productos, total y estado | Equipo | Integrada en `main` | `main` |
| Mostrar un resumen de pedidos por estado | Equipo | Integrada en `main` | `main` |
| Adaptar el panel de caja a celular | Equipo | Integrada en `main` | `main` |
| Buscar un pedido por número | Equipo | Pendiente | — |
| Confirmar el pago físico de un pedido pendiente | Equipo | Pendiente | — |
| Cancelar un pedido pendiente | Equipo | Pendiente | — |
| Probar los cambios de estado y sus validaciones | Equipo | Pendiente | — |

## Trabajo integrado en `main`

- La ruta `/caja` recupera los pedidos guardados y presenta primero los más recientes.
- Cada tarjeta muestra número, nombre del cliente, fecha, estado, productos y total.
- La pantalla resume el total de pedidos, los pendientes y los pagados.
- Los estados tienen indicadores visuales diferentes para facilitar su identificación.
- La interfaz muestra un mensaje claro cuando todavía no existen pedidos.
- El diseño se adapta a pantallas de escritorio y dispositivos pequeños.

## Trabajo verificado localmente

- Se crearon dos pedidos en una base temporal y se comprobó su orden del más reciente al más antiguo.
- Se verificaron pedidos con estados `PENDIENTE DE PAGO` y `PAGADO`.
- La ruta `/caja` respondió correctamente y mostró números, clientes, productos, cantidades y estados.
- Se verificó el mensaje de caja vacía sin modificar la base de datos real.

## Sprint Review

- El primer incremento del Sprint 6 permite consultar en caja los pedidos reales y sus estados.
- El sprint permanece abierto hasta implementar la búsqueda y las acciones de pago y cancelación.

## Sprint Retrospective

- Agrupar los detalles en la consulta de caja mantiene sencilla la plantilla HTML.
- Las pruebas con una base temporal siguen evitando cambios accidentales en los pedidos reales.

## Impedimentos

Ninguno documentado.

## Criterios para cerrar el sprint

- Los pedidos pendientes aparecen en el panel de caja con su detalle completo.
- El personal puede buscar un pedido por número.
- Solo un pedido `PENDIENTE DE PAGO` puede confirmarse como `PAGADO`.
- El personal puede cancelar un pedido pendiente.
- Los cambios de estado quedan almacenados en SQLite.
- Las acciones muestran mensajes claros y están probadas.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

- Todo nuevo trabajo de frontend y backend se desarrolla y prueba en `dev`.
- El flujo acordado es `dev` → pruebas → integración en `main` → push autorizado al remoto.
- `frontend` y `backend` dejan de utilizarse como ramas de trabajo.
- Actualizar este archivo cuando una tarea se asigne, cambie de estado, se integre o quede bloqueada.
- Acordar una sola persona para integrar cada actualización y evitar ediciones simultáneas.
- Usar estados claros: `Pendiente`, `En progreso`, `Terminada en rama`, `Integrada en main` o `Bloqueada`.
- Al cerrar el sprint, registrar el resultado de la Review y la Retrospective antes de preparar el siguiente Sprint Backlog.

## Sprints anteriores

### Sprint 5 — Creación del pedido

Estado: **COMPLETADO**

Incremento verificado en `main`: el estudiante puede ingresar su nombre, confirmar el carrito, guardar el pedido y recibir un número único con estado `PENDIENTE DE PAGO`.

#### Sprint Review

- Se verificó el flujo completo Menú → Carrito → Nombre → Número de pedido.
- Flask valida nuevamente productos, disponibilidad, cantidades y precios antes de guardar.
- El pedido y sus detalles se almacenan en una sola transacción.

#### Sprint Retrospective

- Separar la revisión visual del guardado permitió conectar el backend de forma incremental.
- Recalcular precios y disponibilidad en Flask evita confiar en datos modificables del navegador.
- Las pruebas con una base temporal permitieron validar transacciones sin contaminar los datos locales.

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
