const carrito = [];

const botonCarrito = document.querySelector("#boton-carrito");
const contadorCarrito = document.querySelector("#contador-carrito");
const panelCarrito = document.querySelector("#carrito-panel");
const fondoCarrito = document.querySelector("#carrito-fondo");
const botonCerrar = document.querySelector("#carrito-cerrar");
const listaCarrito = document.querySelector("#carrito-productos");
const mensajeVacio = document.querySelector("#carrito-vacio");
const totalCarrito = document.querySelector("#carrito-total");
const botonVaciar = document.querySelector("#carrito-vaciar");
const botonContinuar = document.querySelector("#carrito-continuar");
const fondoPedido = document.querySelector("#pedido-fondo");
const modalPedido = document.querySelector("#pedido-modal");
const botonCerrarPedido = document.querySelector("#pedido-cerrar");
const pasoNombre = document.querySelector("#paso-nombre");
const pasoResumen = document.querySelector("#paso-resumen");
const formularioNombre = document.querySelector("#formulario-nombre");
const campoNombre = document.querySelector("#nombre-cliente");
const errorNombre = document.querySelector("#nombre-error");
const resumenNombre = document.querySelector("#resumen-nombre");
const resumenPedido = document.querySelector("#pedido-resumen");
const resumenTotal = document.querySelector("#resumen-total");
const botonEditarNombre = document.querySelector("#editar-nombre");
const botonVolverCarrito = document.querySelector("#volver-carrito");
const botonConfirmarPedido = document.querySelector("#confirmar-pedido");
const errorPedido = document.querySelector("#pedido-error");
const pasoConfirmacion = document.querySelector("#paso-confirmacion");
const numeroPedido = document.querySelector("#numero-pedido");
const estadoPedido = document.querySelector("#estado-pedido");
const totalConfirmado = document.querySelector("#total-confirmado");
const botonNuevoPedido = document.querySelector("#nuevo-pedido");

function formatearPrecio(precio) {
    return `$${precio.toFixed(2)}`;
}

function abrirCarrito() {
    panelCarrito.classList.add("carrito-panel-abierto");
    panelCarrito.setAttribute("aria-hidden", "false");
    fondoCarrito.hidden = false;
    document.body.classList.add("carrito-visible");
    botonCerrar.focus();
}

function cerrarCarrito() {
    panelCarrito.classList.remove("carrito-panel-abierto");
    panelCarrito.setAttribute("aria-hidden", "true");
    fondoCarrito.hidden = true;
    document.body.classList.remove("carrito-visible");
    botonCarrito.focus();
}

function abrirFormularioPedido() {
    cerrarCarrito();
    pasoNombre.hidden = false;
    pasoResumen.hidden = true;
    pasoConfirmacion.hidden = true;
    errorNombre.hidden = true;
    campoNombre.removeAttribute("aria-invalid");
    modalPedido.classList.add("pedido-modal-abierto");
    modalPedido.setAttribute("aria-hidden", "false");
    fondoPedido.hidden = false;
    document.body.classList.add("carrito-visible");
    campoNombre.focus();
}

function cerrarFormularioPedido() {
    modalPedido.classList.remove("pedido-modal-abierto");
    modalPedido.setAttribute("aria-hidden", "true");
    fondoPedido.hidden = true;
    document.body.classList.remove("carrito-visible");
    botonCarrito.focus();
}

function actualizarCarrito() {
    listaCarrito.innerHTML = "";

    carrito.forEach((producto) => {
        const elemento = document.createElement("article");
        elemento.className = "carrito-producto";
        elemento.innerHTML = `
            <div class="carrito-producto-datos">
                <h3>${producto.nombre}</h3>
                <span>${formatearPrecio(producto.precio)} c/u</span>
            </div>
            <div class="carrito-producto-acciones">
                <div class="control-cantidad" aria-label="Cantidad de ${producto.nombre}">
                    <button type="button" data-accion="disminuir" data-id="${producto.id}" aria-label="Disminuir ${producto.nombre}">−</button>
                    <span>${producto.cantidad}</span>
                    <button type="button" data-accion="aumentar" data-id="${producto.id}" aria-label="Aumentar ${producto.nombre}" ${producto.cantidad >= producto.existencia ? "disabled" : ""}>+</button>
                </div>
                <strong>${formatearPrecio(producto.precio * producto.cantidad)}</strong>
                <button class="carrito-eliminar" type="button" data-accion="eliminar" data-id="${producto.id}">
                    Eliminar
                </button>
            </div>
        `;
        listaCarrito.appendChild(elemento);
    });

    const cantidadTotal = carrito.reduce(
        (total, producto) => total + producto.cantidad,
        0,
    );
    const precioTotal = carrito.reduce(
        (total, producto) => total + producto.precio * producto.cantidad,
        0,
    );

    contadorCarrito.textContent = cantidadTotal;
    contadorCarrito.setAttribute(
        "aria-label",
        `${cantidadTotal} ${cantidadTotal === 1 ? "producto" : "productos"}`,
    );
    totalCarrito.textContent = formatearPrecio(precioTotal);
    mensajeVacio.hidden = carrito.length > 0;
    botonVaciar.disabled = carrito.length === 0;
    botonContinuar.disabled = carrito.length === 0;

    document.querySelectorAll(".boton-agregar").forEach((boton) => {
        const producto = carrito.find((item) => item.id === Number(boton.dataset.id));
        const existencia = Number(boton.dataset.existencia);
        const disponible = boton.dataset.disponible === "1";
        const alcanzoLimite = producto && producto.cantidad >= existencia;

        boton.disabled = !disponible || existencia === 0 || alcanzoLimite;
        boton.textContent = alcanzoLimite ? "Máximo agregado" : "Agregar";
    });
}

function mostrarResumenPedido(nombre) {
    resumenNombre.textContent = nombre;
    resumenPedido.innerHTML = "";

    carrito.forEach((producto) => {
        const renglon = document.createElement("p");
        const descripcion = document.createElement("span");
        const subtotal = document.createElement("strong");

        descripcion.textContent = `${producto.cantidad} × ${producto.nombre}`;
        subtotal.textContent = formatearPrecio(producto.precio * producto.cantidad);
        renglon.append(descripcion, subtotal);
        resumenPedido.appendChild(renglon);
    });

    const total = carrito.reduce(
        (acumulado, producto) => acumulado + producto.precio * producto.cantidad,
        0,
    );
    resumenTotal.textContent = formatearPrecio(total);
    pasoNombre.hidden = true;
    pasoResumen.hidden = false;
    errorPedido.hidden = true;
}

async function confirmarPedido() {
    botonConfirmarPedido.disabled = true;
    botonConfirmarPedido.textContent = "Guardando...";
    errorPedido.hidden = true;

    try {
        const respuesta = await fetch("/api/pedidos", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                nombre_cliente: campoNombre.value.trim(),
                productos: carrito.map((producto) => ({
                    id: producto.id,
                    cantidad: producto.cantidad,
                })),
            }),
        });
        const datos = await respuesta.json();

        if (!respuesta.ok) {
            throw new Error(datos.error || "No fue posible registrar el pedido.");
        }

        numeroPedido.textContent = `#${String(datos.numero_pedido).padStart(4, "0")}`;
        estadoPedido.textContent = datos.estado;
        totalConfirmado.textContent = formatearPrecio(datos.total);
        pasoResumen.hidden = true;
        pasoConfirmacion.hidden = false;
        carrito.length = 0;
        actualizarCarrito();
    } catch (error) {
        errorPedido.textContent = error.message;
        errorPedido.hidden = false;
    } finally {
        botonConfirmarPedido.disabled = false;
        botonConfirmarPedido.textContent = "Confirmar pedido";
    }
}

function agregarProducto(boton) {
    const id = Number(boton.dataset.id);
    const productoExistente = carrito.find((producto) => producto.id === id);

    if (productoExistente) {
        if (productoExistente.cantidad >= productoExistente.existencia) {
            return;
        }
        productoExistente.cantidad += 1;
    } else {
        carrito.push({
            id,
            nombre: boton.dataset.nombre,
            precio: Number(boton.dataset.precio),
            existencia: Number(boton.dataset.existencia),
            cantidad: 1,
        });
    }

    actualizarCarrito();
}

function cambiarCantidad(id, cambio) {
    const producto = carrito.find((item) => item.id === id);

    if (!producto) {
        return;
    }

    producto.cantidad += cambio;

    if (producto.cantidad <= 0) {
        eliminarProducto(id);
        return;
    }

    actualizarCarrito();
}

function eliminarProducto(id) {
    const indice = carrito.findIndex((producto) => producto.id === id);

    if (indice !== -1) {
        carrito.splice(indice, 1);
        actualizarCarrito();
    }
}

document.querySelectorAll(".boton-agregar:not(:disabled)").forEach((boton) => {
    boton.addEventListener("click", () => agregarProducto(boton));
});

botonCarrito.addEventListener("click", abrirCarrito);
botonCerrar.addEventListener("click", cerrarCarrito);
fondoCarrito.addEventListener("click", cerrarCarrito);

listaCarrito.addEventListener("click", (evento) => {
    const boton = evento.target.closest("button[data-accion]");

    if (!boton) {
        return;
    }

    const id = Number(boton.dataset.id);

    if (boton.dataset.accion === "aumentar") {
        cambiarCantidad(id, 1);
    } else if (boton.dataset.accion === "disminuir") {
        cambiarCantidad(id, -1);
    } else if (boton.dataset.accion === "eliminar") {
        eliminarProducto(id);
    }
});

botonVaciar.addEventListener("click", () => {
    carrito.length = 0;
    actualizarCarrito();
});

botonContinuar.addEventListener("click", abrirFormularioPedido);
botonCerrarPedido.addEventListener("click", cerrarFormularioPedido);
fondoPedido.addEventListener("click", cerrarFormularioPedido);

formularioNombre.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const nombre = campoNombre.value.trim();

    if (nombre === "") {
        errorNombre.hidden = false;
        campoNombre.setAttribute("aria-invalid", "true");
        campoNombre.focus();
        return;
    }

    errorNombre.hidden = true;
    campoNombre.removeAttribute("aria-invalid");
    mostrarResumenPedido(nombre);
});

campoNombre.addEventListener("input", () => {
    if (campoNombre.value.trim() !== "") {
        errorNombre.hidden = true;
        campoNombre.removeAttribute("aria-invalid");
    }
});

botonEditarNombre.addEventListener("click", () => {
    pasoResumen.hidden = true;
    pasoNombre.hidden = false;
    campoNombre.focus();
});

botonVolverCarrito.addEventListener("click", () => {
    cerrarFormularioPedido();
    abrirCarrito();
});

botonConfirmarPedido.addEventListener("click", confirmarPedido);

botonNuevoPedido.addEventListener("click", () => {
    window.location.reload();
});

document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && panelCarrito.classList.contains("carrito-panel-abierto")) {
        cerrarCarrito();
    } else if (evento.key === "Escape" && modalPedido.classList.contains("pedido-modal-abierto")) {
        cerrarFormularioPedido();
    }
});

actualizarCarrito();
