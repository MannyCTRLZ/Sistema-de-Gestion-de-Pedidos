# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 3 — Menú de la cafetería**

Estado: **COMPLETADO**

## Objetivo del sprint

Mostrar un menú funcional obtenido desde la base de datos y adaptado a dispositivos móviles.

## Incremento esperado

Página de menú que muestra dinámicamente los productos disponibles con su nombre, descripción, precio y categoría.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Crear la ruta independiente `/menu` | Equipo | Integrada en `main` | `main` |
| Renderizar los productos recuperados desde SQLite | Equipo | Integrada en `main` | `main` |
| Mostrar nombre, descripción, precio y categoría | Equipo | Integrada en `main` | `main` |
| Ocultar productos no disponibles | Equipo | Integrada en `main` | `main` |
| Mostrar un mensaje cuando no existan productos disponibles | Equipo | Integrada en `main` | `main` |
| Adaptar las tarjetas y la navegación a dispositivos móviles | Equipo | Integrada en `main` | `main` |
| Probar manualmente el menú en computadora y celular | Equipo | Integrada en `main` | `main` |
| Realizar la Review y Retrospective del Sprint 3 | Equipo | Integrada en `main` | `main` |

## Trabajo integrado en `main`

- La página de presentación se encuentra en `/` y conduce al menú.
- La ruta `/menu` recupera los productos disponibles mediante Flask.
- Las tarjetas del menú se generan dinámicamente desde SQLite.
- El menú muestra nombre, descripción, precio y categoría.
- Los productos no disponibles no aparecen en el menú.
- Existe un estado vacío para cuando no haya productos disponibles.
- La interfaz incluye estilos responsive para pantallas pequeñas.

## Trabajo verificado localmente

- El menú se revisó en navegador con una vista de escritorio y una vista móvil de 390 × 844 px.
- Las tarjetas se acomodan en una columna en pantallas pequeñas sin desbordamiento horizontal.
- El navegador no reportó errores ni advertencias durante la revisión.
- Se verificó el mensaje mostrado cuando la consulta no devuelve productos, sin modificar la base de datos.

## Sprint Review

- El menú obtiene los productos desde SQLite y genera sus tarjetas con Flask y Jinja.
- Se comprobó que únicamente aparecen productos disponibles.
- Cada tarjeta muestra nombre, descripción, categoría y precio.
- Se verificaron el diseño de escritorio, la adaptación móvil y el estado sin productos.
- El incremento cumple el objetivo definido para el Sprint 3 y quedó integrado localmente en `main`.

## Sprint Retrospective

- Reutilizar el diseño existente permitió conectar el frontend sin ampliar el alcance del sprint.
- Las pruebas con una base temporal facilitaron validar disponibilidad y estado vacío sin alterar los datos locales.
- En el siguiente sprint conviene mantener la lógica del carrito separada de la consulta de productos.

## Impedimentos

Ninguno documentado.

## Criterios para cerrar el sprint

- El menú obtiene sus productos desde SQLite, sin tarjetas escritas manualmente en HTML.
- Solo aparecen productos disponibles.
- Cada producto muestra nombre, descripción, precio y categoría.
- La interfaz se puede utilizar correctamente en computadora y celular.
- Se prueba el estado sin productos disponibles.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

- Actualizar este archivo cuando una tarea se asigne, cambie de estado, se integre o quede bloqueada.
- Acordar una sola persona para integrar cada actualización y evitar ediciones simultáneas.
- Usar estados claros: `Pendiente`, `En progreso`, `Terminada en rama`, `Integrada en main` o `Bloqueada`.
- Al cerrar el sprint, registrar el resultado de la Review y la Retrospective antes de preparar el siguiente Sprint Backlog.

## Sprints anteriores

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
