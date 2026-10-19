const carrusel = document.querySelector(".carrusel");

if (carrusel) {
    const diapositivas = [...carrusel.querySelectorAll(".carrusel-diapositiva")];
    const indicadores = [...carrusel.querySelectorAll(".carrusel-indicadores button")];
    const pausa = carrusel.querySelector("#carrusel-pausa");
    const movimientoReducido = window.matchMedia("(prefers-reduced-motion: reduce)");
    const contenido = carrusel.querySelector(".carrusel-diapositivas");
    let actual = 0;
    let pausado = movimientoReducido.matches;
    let temporizador;

    function mostrar(indice) {
        actual = (indice + diapositivas.length) % diapositivas.length;
        diapositivas.forEach((diapositiva, posicion) => {
            diapositiva.hidden = posicion !== actual;
            indicadores[posicion].setAttribute("aria-current", String(posicion === actual));
        });
    }

    function actualizarReproduccion() {
        clearInterval(temporizador);
        pausa.textContent = pausado ? "Reproducir" : "Pausar";
        const detenido = pausado || document.hidden || carrusel.matches(":hover")
            || carrusel.contains(document.activeElement);
        contenido.setAttribute("aria-live", detenido ? "polite" : "off");
        if (!detenido) {
            temporizador = setInterval(() => mostrar(actual + 1), 5000);
        }
    }

    carrusel.querySelector(".carrusel-controles").hidden = false;
    carrusel.querySelector("#carrusel-anterior").addEventListener("click", () => mostrar(actual - 1));
    carrusel.querySelector("#carrusel-siguiente").addEventListener("click", () => mostrar(actual + 1));
    indicadores.forEach((boton, indice) => boton.addEventListener("click", () => mostrar(indice)));
    pausa.addEventListener("click", () => {
        pausado = !pausado;
        actualizarReproduccion();
    });
    carrusel.addEventListener("mouseenter", actualizarReproduccion);
    carrusel.addEventListener("mouseleave", actualizarReproduccion);
    carrusel.addEventListener("focusin", actualizarReproduccion);
    carrusel.addEventListener("focusout", () => setTimeout(actualizarReproduccion, 0));
    document.addEventListener("visibilitychange", actualizarReproduccion);
    movimientoReducido.addEventListener("change", () => {
        pausado = movimientoReducido.matches;
        actualizarReproduccion();
    });
    actualizarReproduccion();
}
