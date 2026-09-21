# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 2 — Base de datos y productos**

Estado: **EN PROGRESO**

## Objetivo del sprint

Almacenar productos en SQLite y recuperarlos desde Flask.

## Incremento esperado

Productos de prueba almacenados en la base de datos y recuperados correctamente desde Flask.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Diseñar la tabla `productos` | Por asignar | Integrada en `main` | `main` |
| Crear la conexión entre Python y SQLite | Por asignar | Integrada en `main` | `main` |
| Crear automáticamente la tabla `productos` | Por asignar | Integrada en `main` | `main` |
| Insertar productos de prueba | Por asignar | Pendiente | Por definir |
| Crear una consulta para obtener productos disponibles | Por asignar | Pendiente | Por definir |
| Recuperar los productos desde la ruta de Flask | Por asignar | Pendiente | Por definir |
| Verificar la creación y consulta de datos | Por asignar | Pendiente | Por definir |

## Trabajo integrado en `main`

- La aplicación Flask se ejecuta y muestra la página inicial.
- Existe la estructura inicial de plantillas y archivos estáticos.
- SQLite está conectado mediante `database.py`.
- La tabla `productos` se crea automáticamente si todavía no existe.
- Hay un boceto estático del menú con tres productos de ejemplo.

## Impedimentos

Ninguno documentado.

## Criterios para cerrar el sprint

- Existen productos de prueba persistidos en SQLite.
- Flask puede consultar los productos almacenados.
- La consulta devuelve solamente la información necesaria para continuar con el menú dinámico del Sprint 3.
- El equipo prueba el incremento antes de integrarlo en `main`.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

- Actualizar este archivo cuando una tarea se asigne, cambie de estado, se integre o quede bloqueada.
- Acordar una sola persona para integrar cada actualización y evitar ediciones simultáneas.
- Usar estados claros: `Pendiente`, `En progreso`, `Terminada en rama`, `Integrada en main` o `Bloqueada`.
- Al cerrar el sprint, registrar el resultado de la Review y la Retrospective antes de preparar el siguiente Sprint Backlog.

## Sprint anterior

### Sprint 1 — Preparación y estructura

Estado: **COMPLETADO**

Incremento verificado en el repositorio: aplicación Flask local con página inicial y estructura base de archivos.
