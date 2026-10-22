# Estado actual del proyecto

Este documento es el seguimiento compartido del sprint. La versión integrada en `main` es la fuente oficial del estado del proyecto.

## Sprint actual

**Sprint 9 — Integración, seguridad y pruebas**

Estado: **EN PROGRESO**. Incremento implementado y verificado en `dev`; pendiente de autorización para integrar en `main` y cerrar oficialmente el sprint.

## Objetivo del sprint

Proteger el área interna, integrar los módulos y corregir problemas importantes del flujo completo.

## Incremento esperado

Versión candidata estable con acceso interno protegido y flujo Menú → Caja → Cocina → Entrega verificado.

## Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Implementar inicio y cierre de sesión del personal, con contraseñas almacenadas como hash | Equipo / Codex | Terminada en rama | `dev` |
| Proteger caja, cocina, administración y sus acciones del servidor; conservar el acceso público del estudiante | Equipo / Codex | Terminada en rama | `dev` |
| Corregir el acceso del QR: exigir sesión del personal y conservar el filtro, sin reemplazar la búsqueda manual | Equipo / Codex | Terminada en rama | `dev` |
| Revisar validaciones y manejo de errores de los módulos integrados | Equipo / Codex | Terminada en rama | `dev` |
| Probar el flujo completo y los accesos autorizados y rechazados, incluido el enlace QR a caja | Equipo / Codex | Terminada en rama | `dev` |
| Revisar navegación, accesibilidad y diseño responsive | Equipo / Codex | Terminada en rama | `dev` |
| Integrar la versión candidata probada en main con autorización | Equipo | Pendiente | `dev` → `main` |

## Prioridad de inicio y criterios de cierre del Sprint 9

- Comenzar con una sola cuenta interna, según el alcance del MVP; el estudiante sigue sin crear cuenta ni iniciar sesión.
- Proteger tanto las páginas internas como sus acciones de escritura; verificar el retorno a caja con el número del QR después del acceso.
- No almacenar contraseñas reales, claves de sesión ni secretos en Git.
- Cerrar el sprint cuando el acceso interno y el flujo completo estén probados, los problemas importantes resueltos y el incremento integrado en `main`.
- La autenticación está implementada en `dev`, sin cuenta ni contraseña predeterminadas. La cuenta real se crea localmente con `flask --app app crear-personal`.

## Corrección del QR y trabajo verificado en dev

- Causa: `/caja` y las API de cambios estaban abiertas. El QR solo codificaba `/caja?numero=...`; no era un mecanismo de autorización.
- Abrir el QR sin sesión ahora conduce al acceso del personal y conserva el número para después del inicio de sesión. La búsqueda manual continúa disponible para el personal autenticado.
- Caja, historial, cocina y administración requieren sesión; las acciones directas del servidor sin sesión responden 401 y no modifican datos.
- Las acciones internas y el acceso verifican CSRF. Las sesiones caducan a las ocho horas y se revocan en SQLite al salir, incluso si alguien intenta reutilizar una cookie copiada.
- La clave de firma queda en el entorno o en `instance/`, ignorada por Git. No se crearon credenciales reales ni se añadieron dependencias.
- Se limita el tamaño de las solicitudes y se validan nombre, tamaño del pedido, total y configuración del enlace QR antes de guardar. El modo debug queda desactivado y los errores de API mantienen respuestas JSON comprensibles.
- Pasaron 30 pruebas automatizadas con bases temporales: las 20 existentes adaptadas al acceso real y diez de seguridad, QR, sesión, límites y errores.
- Se completó en navegador Menú → Carrito → Nombre → QR → Acceso del personal → Caja → Pago → Cocina → Preparación → Listo → Entregado → Historial.
- El pedido temporal #0001 de Ana Sprint 9 conservó un Burrito y total $55.00. Se verificó además el alta de un producto desde administración con el token de sesión.
- Se revisaron acceso, caja, cocina y administración a 375 px sin desbordamiento horizontal. Cerrar sesión y volver al enlace del QR vuelve a pedir acceso.
- La cuenta y todos los pedidos de revisión fueron ficticios y temporales. La creación de la cuenta real y la configuración para HTTPS están documentadas en `README.md`.

## Review y Retrospective preliminares

- El incremento técnico cubre las tareas del Sprint 9, incluida la corrección del QR solicitada; falta integrar y comprobar en `main` con autorización antes de registrar su cierre.
- Proteger las acciones en el servidor evita depender de ocultar botones o enlaces en el navegador.
- Recorrer el QR sin sesión y después del acceso confirmó que seguridad y rapidez de búsqueda pueden coexistir.

## Registro del Sprint 8 — Administración

Estado: **COMPLETADO**.

Objetivo cumplido: administrar productos desde `/admin`, con altas, edición, precios y disponibilidad persistidos en SQLite y reflejados en el menú.

### Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Crear panel y catálogo de productos con acceso desde caja y cocina | Equipo / Codex | Integrada en `main` | `dev` → `main` |
| Agregar y editar nombre, descripción, categoría, precio y disponibilidad | Equipo / Codex | Integrada en `main` | `dev` → `main` |
| Activar o desactivar disponibilidad sin eliminar productos | Equipo / Codex | Integrada en `main` | `dev` → `main` |
| Validar datos en Flask y reflejar cambios en el menú | Equipo / Codex | Integrada en `main` | `dev` → `main` |
| Probar persistencia, errores e interfaz | Equipo / Codex | Integrada en `main` | `dev` → `main` |
| Integrar el incremento probado en main con autorización | Equipo / Codex | Integrada en `main` | `dev` → `main` |

### Trabajo verificado del Sprint 8

- El 15 de octubre de 2026 pasaron las 20 pruebas automatizadas: las 14 existentes y seis nuevas de administración.
- Se verificaron altas, edición, disponibilidad, datos inválidos y productos inexistentes sin escrituras parciales.
- Marcar un producto agotado impide nuevos pedidos que lo incluyan, pero conserva los pedidos anteriores y permite reactivarlo.
- Los textos del catálogo se escapan en HTML; el carrito muestra los nombres editables como texto.
- Renombrar un producto inicial ya no provoca que se vuelva a insertar al reiniciar: los datos iniciales solo se cargan en un catálogo vacío.
- En navegador se agregó un producto, se cambió su nombre y precio, se marcó agotado y se reactivó; el menú conservó su tarjeta con «Agotado» y el botón deshabilitado.
- Se revisaron el catálogo en escritorio y el formulario a 375 px de ancho, sin desbordamiento horizontal.
- Todas las pruebas usaron bases temporales, sin modificar productos ni pedidos reales.
- La autenticación y los roles internos siguen pendientes para el Sprint 9; este incremento no debe exponerse públicamente sin ese control.

### Sprint Review

- El panel de administración cumple el incremento del Sprint 8 y se integra en `main` por autorización del usuario el 20 de octubre de 2026.
- Antes de integrar volvieron a pasar las 20 pruebas automatizadas con bases temporales; se comprobaron nuevamente en `main` después de integrar.
- Los productos agotados siguen visibles y no se aceptan en nuevos pedidos; el historial se conserva.

### Sprint Retrospective

- Probar las altas, ediciones y disponibilidad con bases temporales permitió verificar el módulo sin alterar los datos reales.
- Separar la disponibilidad del inventario numérico mantuvo sencilla la administración.
- Documentar el carrusel aparte evita confundir un ajuste visual con los criterios de cierre de administración.

### Aclaración del carrusel del inicio

- El commit `0886a51` añade un carrusel de tres platillos en la portada, con controles anterior/siguiente, indicadores y pausa; respeta la preferencia de reducir movimiento.
- Se integra junto con administración como ajuste visual adicional, no como requisito del Sprint 8 ni como implementación de seguridad del Sprint 9.
- Sus fotos y nombres se configuran en la plantilla y los archivos estáticos; editar productos en `/admin` no actualiza este carrusel.
- Se revisaron su código, el HTML generado y la disponibilidad de sus tres imágenes y del script; esta comprobación no sustituye una prueba interactiva en navegador.

## Registro del Sprint 7 — Módulo de cocina

Estado: **COMPLETADO**

### Objetivo del sprint

Gestionar la preparación y entrega de los pedidos pagados.

### Incremento esperado

Flujo Pagado → En preparación → Listo → Entregado funcional.

### Sprint Backlog

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Crear la ruta e interfaz de cocina | Equipo | Integrada en `main` | `dev` → `main` |
| Mostrar pedidos pagados, en preparación y listos con sus cantidades | Equipo | Integrada en `main` | `dev` → `main` |
| Agregar acciones de preparación, listo y entrega | Equipo | Integrada en `main` | `dev` → `main` |
| Validar las transiciones básicas en Flask | Equipo | Integrada en `main` | `dev` → `main` |
| Separar en caja el historial de pedidos entregados con búsqueda por número | Equipo | Integrada en `main` | `dev` → `main` |
| Validar interfaz, errores, concurrencia y persistencia completa | Equipo | Integrada en `main` | `dev` → `main` |
| Probar el flujo completo Menú → Caja → Cocina → Entrega | Equipo | Integrada en `main` | `dev` → `main` |
| Integrar el incremento con comprobación básica en main | Equipo | Integrada en `main` | `dev` → `main` |

### Trabajo integrado en `main`

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
| Mostrar un QR al confirmar cada pedido que abra caja con el filtro `numero` | Equipo | Integrada en `main` | `main` |

Este ajuste no modifica el flujo de cocina ni las acciones existentes de caja.
La prueba local confirmó el enlace codificado, la imagen SVG y la búsqueda
filtrada en caja; las siete pruebas de caja pasan.
Integración del QR confirmada en `main` en el commit `3af503a`.

### Trabajo verificado localmente

- Comprobación básica con una base temporal: `/cocina` carga, excluye pedidos sin pagar y muestra los productos y cantidades de un pedido pagado.
- La API recorrió preparación, listo y entrega; rechazó un salto directo de pagado a listo.
- El pedido entregado salió de la lista activa y `/caja` siguió respondiendo.
- Se comprobó con una base temporal que un pedido entregado aparece en el historial de caja, conserva sus cantidades y total, se puede buscar por número y no muestra acciones de pago o cancelación.
- Las seis pruebas existentes de caja siguen pasando después de separar el historial.
- El 14 de octubre de 2026 pasaron 13 pruebas automatizadas: seis de caja y siete de cocina e historial.
- Se comprobaron las 18 combinaciones de estados de origen y destino de cocina; solo las tres transiciones permitidas avanzan el pedido.
- Los datos inválidos, pedidos inexistentes, saltos de estado y reintentos se rechazan sin modificar el pedido.
- Dos solicitudes simultáneas de preparación producen un avance correcto y un rechazo, sin duplicar acciones.
- Se reabrió la conexión para verificar estado final, detalle, cantidades, total, cliente y fecha; SQLite pasó las comprobaciones de integridad y claves foráneas.
- En navegador se completó Menú → Carrito → Nombre → Número → Caja → Pago → Cocina → Preparación → Listo → Entregado → Historial.
- El pedido de prueba #0001 de Ana Sprint 7 conservó un Burrito y total $55.00 al llegar al historial; se verificó la búsqueda por número.
- Se revisó cocina en escritorio y cocina e historial a 375 px de ancho sin desbordamiento horizontal.
- El diálogo «Volver» conserva el estado; una segunda ventana desactualizada mostró el error de acción repetida y recuperó el estado correcto al actualizar.
- Todas las pruebas usaron bases temporales; no se modificaron los pedidos reales.

### Sprint Review

- Cocina y el historial de entregados quedaron integrados en `main`.
- Se verificaron el flujo completo, la interfaz, los errores, la concurrencia y la persistencia.
- El Sprint 7 cumple sus criterios de cierre. Sus pruebas y resultados quedan integrados en `main`.

### Sprint Retrospective

- Probar con una base temporal permitió recorrer todo el flujo sin alterar datos reales.
- La actualización condicional del estado evita que dos ventanas avancen dos veces la misma acción.
- Validar los diálogos y mensajes en navegador complementó las pruebas automatizadas de Flask y SQLite.

### Impedimentos

Ninguno documentado.

### Criterios para cerrar el sprint

- Solo los pedidos pagados pueden entrar a preparación.
- Cada acción avanza al siguiente estado permitido y persiste en SQLite.
- Los pedidos entregados dejan de aparecer como activos.
- La interfaz y el flujo completo están probados e integrados en `main`.
- `SPRINT_STATUS.md` queda actualizado con responsables, ramas y resultados reales.

## Acuerdos de actualización

### Ajustes visuales solicitados después del Sprint 7

| Tarea | Responsable | Estado | Rama |
|---|---|---|---|
| Reemplazar la taza del inicio por la imagen proporcionada | Equipo | Integrada en `main` | `main` |
| Añadir una animación breve al pulsar botones y enlaces de acción | Equipo | Integrada en `main` | `main` |

- La portada utiliza `static/img/cafeteria-universitaria.png`, conservando el emblema completo y su proporción, con transparencia fuera del borde circular por petición del usuario.
- Inicio, menú, caja y cocina cargan una animación compartida de 180 ms; incluye los botones dinámicos del carrito y la activación con teclado.
- Los botones deshabilitados quedan excluidos y se respeta la preferencia de reducir movimiento.
- Se revisó la portada en navegador y se comprobó que agregar con doble clic conserva una sola unidad y que el control de cantidad funciona.
- Los ajustes visuales quedaron integrados y publicados en `main` en el commit `f8cc160`; `dev` se sincronizó con esa versión.
- El 15 de octubre de 2026 pasaron las 14 pruebas existentes, incluida la generación del QR y su enlace filtrado en caja.
- Estos ajustes no cambian el cierre del Sprint 7.

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
