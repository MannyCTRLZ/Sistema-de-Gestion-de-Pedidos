# AGENTS.md

## Proyecto
Sistema web de gestión de pedidos para una cafetería universitaria.

## Antes de trabajar
Antes de modificar archivos:
1. Lee `PROJECT_CONTEXT.md` completo para conocer el alcance, requisitos, arquitectura, MVP, decisiones y límites del proyecto.
2. Lee `SPRINT_STATUS.md` para identificar el sprint actual, las tareas priorizadas y el trabajo ya integrado.
3. Revisa la estructura y el estado actual del repositorio; el documento de seguimiento no sustituye la verificación del código.

## Seguimiento de sprints
- `PROJECT_CONTEXT.md` contiene la hoja de ruta general de los 10 sprints.
- `SPRINT_STATUS.md` es la fuente compartida del estado actual del sprint.
- La versión de `SPRINT_STATUS.md` integrada en `main` es el estado oficial del proyecto.
- Prioriza las tareas del sprint actual y no adelantes funcionalidades de otros sprints salvo petición explícita.
- No marques una tarea como terminada solo porque funciona en una rama: debe estar probada e integrada en `main`.
- Al integrar una tarea, actualiza `SPRINT_STATUS.md` con su estado, responsable y rama cuando esos datos se conozcan.
- Evita que dos personas editen simultáneamente `SPRINT_STATUS.md`; el equipo debe acordar quién integra cada actualización para reducir conflictos.

## Principios
- El equipo es principiante.
- Prefiere soluciones sencillas, legibles y fáciles de explicar.
- Stack actual: HTML + CSS + JavaScript + Python + Flask + SQLite.
- No introducir React, Node.js, FastAPI, PostgreSQL u otros frameworks/servicios salvo petición explícita.
- Trabajar de forma incremental y probar cada etapa.
- No ampliar el alcance del MVP sin consultarlo.
- El cliente no crea cuenta ni inicia sesión.
- El cliente solo ingresa un nombre para identificar el pedido.
- El localizador físico de la cafetería está fuera del alcance del software.
- No implementar pagos en línea.

## Frontend
La prioridad actual es desarrollar primero el frontend del flujo del estudiante:
menú -> carrito -> nombre -> confirmación/número de pedido.

Estructura esperada:
- `templates/` para HTML.
- `static/css/` para CSS.
- `static/js/` para JavaScript.
- `static/img/` para imágenes.

## Seguridad y repositorio
- Nunca guardar tokens, contraseñas reales ni secretos en el repositorio.
- `.venv/` debe permanecer fuera de Git.
- No hacer push, merge, publicación o cambios remotos sin autorización explícita del usuario.
- No reemplazar decisiones documentadas sin actualizar `PROJECT_CONTEXT.md`.
- No mantener estados oficiales diferentes del sprint en cada rama.

## Ramas de trabajo
- `main`: rama estable; no desarrollar directamente en ella.
- `dev`: rama de integración y pruebas conjuntas.
- `frontend`: rama para HTML, CSS, JavaScript y la experiencia visual del cliente.
- `backend`: rama para Flask, SQLite y la lógica del servidor.
- Antes de implementar, comprobar la rama activa con `git branch --show-current`.
- Usar la rama que corresponda al tipo de tarea. Si una tarea afecta frontend y backend,
  consultar al usuario en qué rama trabajar o dividirla en cambios coordinados.
- No hacer merge entre ramas ni push al remoto sin autorización explícita del usuario.

## Estilo de trabajo
Cuando se solicite una implementación:
1. Inspeccionar archivos actuales.
2. Explicar brevemente qué se modificará.
3. Hacer el cambio mínimo necesario.
4. Probarlo cuando sea posible.
5. Resumir archivos modificados y cómo ejecutar/probar.
