# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 7 — Módulo de cocina**

Estado: **EN PROGRESO**

## Objetivo del sprint

Gestionar la preparación y entrega de los pedidos pagados.

## Incremento esperado

Flujo Pagado → En preparación → Listo → Entregado funcional.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Crear la ruta e interfaz de cocina | Equipo | Integrada en `main` | `dev` → `main` |
| Mostrar pedidos pagados, en preparación y listos con sus cantidades | Equipo | Integrada en `main` | `dev` → `main` |
| Agregar acciones de preparación, listo y entrega | Equipo | Integrada en `main` | `dev` → `main` |
| Validar las transiciones básicas en Flask | Equipo | Integrada en `main` | `dev` → `main` |
| Separar en caja el historial de pedidos entregados con búsqueda por número | Equipo | Integrada en `main` | `dev` → `main` |
| Validar interfaz, errores, concurrencia y persistencia completa | Equipo | Pendiente | `dev` |
| Probar el flujo completo Menú → Caja → Cocina → Entrega | Equipo | Pendiente | `dev` |
| Integrar el incremento con comprobación básica en main | Equipo | Integrada en `main` | `dev` → `main` |

## Trabajo integrado en `main`

- `/cocina` muestra pedidos activos pagados, en preparación y listos, del más antiguo al más reciente.
- Cada tarjeta muestra número, cliente, fecha, estado, productos y cantidades.
- El resumen cuenta los pedidos por preparar, en preparación y listos.
- Cada estado ofrece únicamente su siguiente acción con un diálogo de confirmación.
- Flask permite PAGADO → EN PREPARACIÓN → LISTO → ENTREGADO y comprueba el estado anterior al actualizar.
- Los pendientes de pago, cancelados y entregados quedan fuera de la lista activa.
- Caja incluye un enlace a cocina y cocina permite volver a caja o actualizar la lista manualmente.
- La interfaz reutiliza los estilos responsive de caja.
- Caja separa los pedidos en seguimiento del historial de entregados; la búsqueda se aplica a la sección seleccionada.
- El historial conserva número, cliente, fecha de creación, productos, cantidades y total sin acciones de caja.
- El incremento fue desarrollado en `dev` e integrado en `main` tras su comprobación básica, por autorización del usuario.

### Ajuste solicitado: QR para localizar pedidos en caja

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Mostrar un QR al confirmar cada pedido que abra caja con el filtro `numero` | Equipo | En progreso; pendiente de integrar en `main` | `codigoQr` |

Este ajuste no modifica el flujo de cocina ni las acciones existentes de caja.
La prueba local confirmó el enlace codificado, la imagen SVG y la búsqueda
filtrada en caja; las siete pruebas de caja pasan.

## Trabajo verificado localmente

- Comprobación básica con una base temporal: `/cocina` carga, excluye pedidos sin pagar y muestra los productos y cantidades de un pedido pagado.
- La API recorrió preparación, listo y entrega; rechazó un salto directo de pagado a listo.
- El pedido entregado salió de la lista activa y `/caja` siguió respondiendo.
- Se comprobó con una base temporal que un pedido entregado aparece en el historial de caja, conserva sus cantidades y total, se puede buscar por número y no muestra acciones de pago o cancelación.
- Las seis pruebas existentes de caja siguen pasando después de separar el historial.
- Quedan pendientes la revisión en navegador y las validaciones completas solicitadas para el siguiente incremento.

## Sprint Review

- Cocina y el historial de entregados quedaron integrados en `main`.
- El Sprint 7 permanece abierto hasta completar la revisión en navegador y las validaciones del flujo completo, errores, concurrencia y persistencia.

## Sprint Retrospective

- Pendiente al cierre del sprint.

## Impedimentos

Ninguno documentado.

## Criterios para cerrar el sprint

- Solo los pedidos pagados pueden entrar a preparación.
- Cada acción avanza al siguiente estado permitido y persiste en SQLite.
- Los pedidos entregados dejan de aparecer como activos.
- La interfaz y el flujo completo están probados e integrados en `main`.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

### Ajuste del menú solicitado después del Sprint 6

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Mostrar confirmación animada al agregar al carrito y bloquear dobles clics accidentales | Equipo | Integrada en `main` | `main` |

- El botón muestra «✓ Agregado» durante 700 ms, el carrito hace un pulso breve y aparece un aviso con el nombre del producto durante dos segundos.
- La animación respeta la preferencia de reducir movimiento.
- Se verificó en el navegador que un doble clic agrega una sola unidad; un clic posterior agrega otra normalmente y actualiza el total.
- Integrado y publicado en `main` en el commit `34b6b18`; este ajuste no cambia el cierre del Sprint 6.

### Reglas compartidas

- Todo nuevo trabajo de frontend y backend se desarrolla y prueba en `dev`.
- El flujo acordado es `dev` → pruebas → integración en `main` → push autorizado al remoto.
- `frontend` y `backend` dejan de utilizarse como ramas de trabajo.
- Actualizar este archivo cuando una tarea se asigne, cambie de estado, se integre o quede bloqueada.
- Acordar una sola persona para integrar cada actualización y evitar ediciones simultáneas.
- Usar estados claros: `Pendiente`, `En progreso`, `Terminada en rama`, `Integrada en main` o `Bloqueada`.
- Al cerrar el sprint, registrar el resultado de la Review y la Retrospective antes de preparar el siguiente Sprint Backlog.

## Sprints anteriores

### Sprint 6 — Módulo de caja

Estado: **COMPLETADO**

Incremento verificado en `main`: el personal consulta pedidos, busca por número, confirma el pago físico o cancela pedidos pendientes.

#### Sprint Review

- El módulo muestra el detalle completo, total y estado de los pedidos.
- Las acciones persisten en SQLite y rechazan cambios repetidos o inválidos.
- Se verificaron seis pruebas automatizadas y los controles de pago y cancelación en navegador con datos temporales.

#### Sprint Retrospective

- Reutilizar la consulta de detalles simplificó la interfaz.
- Las pruebas temporales evitaron modificar pedidos reales.
- Confirmar las acciones mediante un diálogo claro ayudó a evitar errores.

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
