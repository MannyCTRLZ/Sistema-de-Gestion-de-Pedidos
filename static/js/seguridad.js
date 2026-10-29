// Todas las acciones internas envían el token de la sesión actual.
async function solicitarPersonal(url, opciones) {
    const cuerpoEsFormulario = opciones.body instanceof FormData;
    const encabezados = {
        ...opciones.headers,
        "X-CSRF-Token": document.querySelector('meta[name="csrf-token"]').content,
    };
    if (cuerpoEsFormulario) delete encabezados["Content-Type"];
    const respuesta = await fetch(url, {
        ...opciones,
        headers: encabezados,
    });
    if (respuesta.status === 401) {
        const regreso = window.location.pathname + window.location.search;
        window.location.assign(`/login?next=${encodeURIComponent(regreso)}`);
        throw new Error("Tu sesión venció. Inicia sesión para continuar.");
    }
    if (!respuesta.headers.get("Content-Type")?.includes("application/json")) {
        throw new Error("El servidor no pudo procesar la solicitud. Actualiza antes de reintentar.");
    }
    const datos = await respuesta.json();
    if (!respuesta.ok) throw new Error(datos.error || "No se pudo completar la operación.");
    return datos;
}
