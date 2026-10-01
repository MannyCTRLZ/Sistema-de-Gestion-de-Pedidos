# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 4 — Carrito de compras**

Estado: **COMPLETADO**

## Objetivo del sprint

Permitir que el estudiante construya y revise su pedido antes de proporcionar su nombre.

## Incremento esperado

Carrito interactivo que permite agregar y eliminar productos, modificar cantidades y calcular el total.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
<<<<<<< HEAD
| Diseñar la tabla `productos` | Por asignar | Integrada en `main` | `main` |
| Crear la conexión entre Python y SQLite | Por asignar | Integrada en `main` | `main` |
| Crear automáticamente la tabla `productos` | Por asignar | Integrada en `main` | `main` |
| Insertar productos de prueba | Codex | Terminada en rama | `Jesus` |
| Crear una consulta para obtener productos disponibles | Codex | Terminada en rama | `Jesus` |
| Recuperar los productos desde la ruta de Flask | Codex | Terminada en rama | `Jesus` |
| Verificar la creación y consulta de datos | Codex | Terminada en rama | `Jesus` |
=======
| Abrir y cerrar el panel del carrito | Equipo | Integrada en `main` | `main` |
| Agregar productos disponibles | Equipo | Integrada en `main` | `main` |
| Agrupar productos repetidos | Equipo | Integrada en `main` | `main` |
| Aumentar y disminuir cantidades | Equipo | Integrada en `main` | `main` |
| Eliminar un producto | Equipo | Integrada en `main` | `main` |
| Vaciar el carrito | Equipo | Integrada en `main` | `main` |
| Calcular contador y total | Equipo | Integrada en `main` | `main` |
| Adaptar el panel a dispositivos móviles | Equipo | Integrada en `main` | `main` |
| Probar el flujo completo del carrito | Equipo | Integrada en `main` | `main` |
>>>>>>> frontend

## Trabajo integrado en `main`

- El botón del encabezado abre un panel lateral con el contenido del carrito.
- Los productos repetidos se agrupan y aumentan su cantidad.
- Cada producto permite aumentar, disminuir o eliminar su cantidad.
- El contador representa el total de unidades seleccionadas.
- El total se recalcula después de cada cambio.
- El carrito se puede vaciar completamente.
- Los productos agotados no se pueden agregar.
- El panel se adapta al ancho disponible en dispositivos móviles.

## Trabajo verificado localmente

- Se agregaron dos productos y se comprobó un contador de tres unidades.
- Se verificó el total de dos burritos y un plato de chilaquiles: `$170.00`.
- Se probaron los controles para aumentar y disminuir cantidades.
- Se eliminó un producto y se verificó el nuevo total.
- Se vació el carrito y el total regresó a `$0.00`.
- Se confirmó que los botones de productos agotados permanecen deshabilitados.

## Sprint Review

- El estudiante puede construir y revisar un carrito completo desde el menú.
- Las cantidades, el contador y el total se actualizan correctamente.
- El estado vacío y la acción de vaciar carrito funcionan correctamente.
- El incremento cumple el objetivo definido para el Sprint 4 y quedó integrado localmente en `main`.

## Sprint Retrospective

- La delegación de eventos simplificó los controles creados dinámicamente dentro del carrito.
- Mantener el carrito únicamente en JavaScript permitió completar el incremento sin adelantar la creación de pedidos.
- En el Sprint 5 será necesario validar nuevamente precios y disponibilidad antes de guardar el pedido.

## Trabajo terminado en la rama `Jesus`

- Se agregaron cuatro productos de prueba con una carga que evita duplicarlos.
- Se creó una consulta que devuelve únicamente productos disponibles.
- La ruta `/api/productos` recupera los productos desde Flask en formato JSON.
- Se verificó la creación, la carga idempotente y el filtro de disponibilidad con una base temporal.

## Impedimentos

Ninguno documentado.

## Criterios para cerrar el sprint

- Se pueden agregar varios productos al carrito.
- Se pueden aumentar y disminuir cantidades.
- Se puede eliminar un producto y vaciar todo el carrito.
- El contador y el total se actualizan correctamente.
- Los productos agotados no se pueden agregar.
- El panel funciona correctamente en computadora y celular.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

- Actualizar este archivo cuando una tarea se asigne, cambie de estado, se integre o quede bloqueada.
- Acordar una sola persona para integrar cada actualización y evitar ediciones simultáneas.
- Usar estados claros: `Pendiente`, `En progreso`, `Terminada en rama`, `Integrada en main` o `Bloqueada`.
- Al cerrar el sprint, registrar el resultado de la Review y la Retrospective antes de preparar el siguiente Sprint Backlog.

## Sprints anteriores

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
