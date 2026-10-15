const movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)");
const animacionesBotones = new WeakMap();

// Capturar el clic antes de que la acción deshabilite u oculte su botón.
// La delegación incluye los controles creados dinámicamente en el carrito.
document.addEventListener("click", (evento) => {
    const boton = evento.target.closest("button, a:not(.logo)");
    if (!boton || boton.matches(":disabled, [aria-disabled='true']")
            || movimientoReducido.matches) return;

    animacionesBotones.get(boton)?.cancel();
    const animacion = boton.animate([
        { scale: "1", filter: "brightness(1)" },
        { scale: ".95", filter: "brightness(.92)", offset: .4 },
        { scale: "1", filter: "brightness(1)" },
    ], { duration: 180, easing: "ease-out" });
    animacionesBotones.set(boton, animacion);
}, true);
