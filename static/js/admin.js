const formularioProducto = document.getElementById("formulario-producto");
const idProducto = document.getElementById("producto-id");
const nombreProducto = document.getElementById("producto-nombre");
const categoriaProducto = document.getElementById("producto-categoria");
const precioProducto = document.getElementById("producto-precio");
const descripcionProducto = document.getElementById("producto-descripcion");
const disponibleProducto = document.getElementById("producto-disponible");
const imagenProducto = document.getElementById("producto-imagen");
const imagenActual = document.getElementById("producto-imagen-actual");
const imagenVista = document.getElementById("producto-imagen-vista");
const quitarImagen = document.getElementById("quitar-producto-imagen");
const guardarProducto = document.getElementById("guardar-producto");
const cancelarEdicion = document.getElementById("cancelar-edicion");
const tituloProducto = document.getElementById("titulo-formulario-producto");
const errorProducto = document.getElementById("producto-error");
const mensajeAdmin = document.getElementById("admin-mensaje");
let urlEdicion = null;
let guardando = false;
let urlVistaTemporal = null;

const resultadoAdmin = sessionStorage.getItem("resultado-admin");
if (resultadoAdmin) {
    mensajeAdmin.textContent = resultadoAdmin;
    mensajeAdmin.hidden = false;
    sessionStorage.removeItem("resultado-admin");
}

async function enviarProducto(url, metodo, datos) {
    if (datos instanceof FormData) {
        return solicitarPersonal(url, { method: metodo, body: datos });
    }
    return solicitarPersonal(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
    });
}

function limpiarVistaImagen() {
    if (urlVistaTemporal) URL.revokeObjectURL(urlVistaTemporal);
    urlVistaTemporal = null;
    imagenVista.removeAttribute("src");
    imagenActual.hidden = true;
    quitarImagen.checked = false;
}

function mostrarImagen(ruta) {
    imagenVista.src = ruta;
    imagenActual.hidden = false;
}

imagenProducto.addEventListener("change", () => {
    if (urlVistaTemporal) URL.revokeObjectURL(urlVistaTemporal);
    urlVistaTemporal = null;
    const archivo = imagenProducto.files[0];
    if (!archivo) return;
    urlVistaTemporal = URL.createObjectURL(archivo);
    mostrarImagen(urlVistaTemporal);
    quitarImagen.checked = false;
});

quitarImagen.addEventListener("change", () => {
    if (quitarImagen.checked) imagenProducto.value = "";
});

function finalizarCambio(mensaje) {
    sessionStorage.setItem("resultado-admin", mensaje);
    window.location.reload();
}

document.querySelectorAll("[data-editar]").forEach((boton) => {
    boton.addEventListener("click", () => {
        if (guardando) return;
        const producto = JSON.parse(boton.dataset.editar);
        idProducto.value = producto.id;
        urlEdicion = boton.dataset.url;
        nombreProducto.value = producto.nombre;
        categoriaProducto.value = producto.categoria;
        precioProducto.value = producto.precio.toFixed(2);
        descripcionProducto.value = producto.descripcion || "";
        disponibleProducto.checked = Boolean(producto.disponible);
        limpiarVistaImagen();
        if (producto.imagen) {
            mostrarImagen(formularioProducto.dataset.staticUrl + producto.imagen);
        }
        tituloProducto.textContent = `Editar: ${producto.nombre}`;
        guardarProducto.textContent = "Guardar cambios";
        cancelarEdicion.hidden = false;
        errorProducto.hidden = true;
        formularioProducto.scrollIntoView({ block: "center" });
        nombreProducto.focus();
    });
});

cancelarEdicion.addEventListener("click", () => {
    if (guardando) return;
    formularioProducto.reset();
    limpiarVistaImagen();
    idProducto.value = "";
    urlEdicion = null;
    tituloProducto.textContent = "Nuevo producto";
    guardarProducto.textContent = "Agregar producto";
    cancelarEdicion.hidden = true;
    errorProducto.hidden = true;
});

formularioProducto.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    if (guardando) return;
    guardando = true;
    guardarProducto.disabled = true;
    cancelarEdicion.disabled = true;
    errorProducto.hidden = true;
    const editando = Boolean(idProducto.value);
    try {
        const datos = new FormData();
        datos.append("nombre", nombreProducto.value);
        datos.append("categoria", categoriaProducto.value);
        datos.append("precio", precioProducto.value);
        datos.append("descripcion", descripcionProducto.value);
        datos.append("disponible", String(disponibleProducto.checked));
        datos.append("quitar_imagen", String(quitarImagen.checked));
        if (imagenProducto.files[0]) datos.append("imagen", imagenProducto.files[0]);
        await enviarProducto(
            editando ? urlEdicion : formularioProducto.dataset.url,
            editando ? "PUT" : "POST",
            datos,
        );
        finalizarCambio(editando ? "Producto actualizado." : "Producto agregado al menú.");
    } catch (error) {
        errorProducto.textContent = error.message;
        errorProducto.hidden = false;
    } finally {
        guardando = false;
        guardarProducto.disabled = false;
        cancelarEdicion.disabled = false;
    }
});

document.querySelectorAll("[data-disponible]").forEach((boton) => {
    boton.addEventListener("click", async () => {
        if (guardando) return;
        guardando = true;
        boton.disabled = true;
        try {
            const disponible = boton.dataset.disponible === "true";
            await enviarProducto(boton.dataset.url, "PATCH", { disponible });
            finalizarCambio(disponible ? "Producto disponible nuevamente." : "Producto marcado como agotado.");
        } catch (error) {
            mensajeAdmin.textContent = error.message;
            mensajeAdmin.classList.add("caja-error");
            mensajeAdmin.hidden = false;
            mensajeAdmin.scrollIntoView({ block: "center" });
        } finally {
            guardando = false;
            boton.disabled = false;
        }
    });
});

document.querySelectorAll("[data-eliminar]").forEach((boton) => {
    boton.addEventListener("click", async () => {
        if (guardando) return;
        const nombre = boton.dataset.eliminar;
        if (!window.confirm(`¿Borrar “${nombre}”? Esta acción no se puede deshacer.`)) return;
        guardando = true;
        boton.disabled = true;
        try {
            await enviarProducto(boton.dataset.url, "DELETE", null);
            finalizarCambio("Producto borrado del catálogo.");
        } catch (error) {
            mensajeAdmin.textContent = error.message;
            mensajeAdmin.classList.add("caja-error");
            mensajeAdmin.hidden = false;
            mensajeAdmin.scrollIntoView({ block: "center" });
        } finally {
            guardando = false;
            boton.disabled = false;
        }
    });
});
