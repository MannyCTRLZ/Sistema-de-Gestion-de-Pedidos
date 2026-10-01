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
                    <button type="button" data-accion="aumentar" data-id="${producto.id}" aria-label="Aumentar ${producto.nombre}">+</button>
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
}

function agregarProducto(boton) {
    const id = Number(boton.dataset.id);
    const productoExistente = carrito.find((producto) => producto.id === id);

    if (productoExistente) {
        productoExistente.cantidad += 1;
    } else {
        carrito.push({
            id,
            nombre: boton.dataset.nombre,
            precio: Number(boton.dataset.precio),
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

document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && panelCarrito.classList.contains("carrito-panel-abierto")) {
        cerrarCarrito();
    }
});

actualizarCarrito();
