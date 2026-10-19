const formularioProducto = document.getElementById("formulario-producto");
const idProducto = document.getElementById("producto-id");
const nombreProducto = document.getElementById("producto-nombre");
const categoriaProducto = document.getElementById("producto-categoria");
const precioProducto = document.getElementById("producto-precio");
const descripcionProducto = document.getElementById("producto-descripcion");
const disponibleProducto = document.getElementById("producto-disponible");
const guardarProducto = document.getElementById("guardar-producto");
const cancelarEdicion = document.getElementById("cancelar-edicion");
const tituloProducto = document.getElementById("titulo-formulario-producto");
const errorProducto = document.getElementById("producto-error");
const mensajeAdmin = document.getElementById("admin-mensaje");
let urlEdicion = null;
let guardando = false;

const resultadoAdmin = sessionStorage.getItem("resultado-admin");
if (resultadoAdmin) {
    mensajeAdmin.textContent = resultadoAdmin;
    mensajeAdmin.hidden = false;
    sessionStorage.removeItem("resultado-admin");
}

async function enviarProducto(url, metodo, datos) {
    const respuesta = await fetch(url, {
        method: metodo,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
    });
    if (!respuesta.headers.get("Content-Type")?.includes("application/json")) {
        throw new Error("El servidor no pudo procesar la solicitud. Intenta nuevamente.");
    }
    const resultado = await respuesta.json();
    if (!respuesta.ok) throw new Error(resultado.error || "No se pudo guardar el producto.");
    return resultado;
}

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
        await enviarProducto(editando ? urlEdicion : formularioProducto.dataset.url,
            editando ? "PUT" : "POST", {
                nombre: nombreProducto.value,
                categoria: categoriaProducto.value,
                precio: precioProducto.value,
                descripcion: descripcionProducto.value,
                disponible: disponibleProducto.checked,
            });
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
