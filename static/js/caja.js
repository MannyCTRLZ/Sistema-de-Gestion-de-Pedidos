const mensajeCaja = document.getElementById("caja-mensaje");
const confirmacionCaja = document.getElementById("confirmacion-caja");

function confirmarAccion(pregunta) {
    document.getElementById("detalle-confirmacion-caja").textContent = pregunta;
    confirmacionCaja.returnValue = "volver";
    return new Promise((resolver) => {
        confirmacionCaja.addEventListener("close", () => {
            resolver(confirmacionCaja.returnValue === "confirmar");
        }, { once: true });
        confirmacionCaja.showModal();
    });
}

const resultadoAnterior = sessionStorage.getItem("resultado-caja");
if (resultadoAnterior) {
    mensajeCaja.textContent = resultadoAnterior;
    mensajeCaja.hidden = false;
    sessionStorage.removeItem("resultado-caja");
}

document.querySelectorAll(".pedido-caja .pedido-caja-acciones button").forEach((boton) => {
    boton.addEventListener("click", async () => {
        const numero = boton.dataset.numero;
        const estado = boton.dataset.estado;
        const pregunta = estado === "PAGADO"
            ? `¿Confirmas que recibiste el pago físico del pedido #${numero}?`
            : `¿Cancelar el pedido #${numero}? Esta acción no se puede deshacer desde caja.`;
        if (!await confirmarAccion(pregunta)) return;

        const controles = boton.closest(".pedido-caja-acciones").querySelectorAll("button");
        controles.forEach((control) => { control.disabled = true; });
        mensajeCaja.hidden = true;
        try {
            const respuesta = await fetch(boton.dataset.url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estado }),
            });
            const datos = await respuesta.json();
            if (!respuesta.ok) throw new Error(datos.error || "No se pudo actualizar el pedido.");
            sessionStorage.setItem("resultado-caja", estado === "PAGADO"
                ? `Pago del pedido #${numero} confirmado.`
                : `Pedido #${numero} cancelado.`);
            window.location.reload();
        } catch (error) {
            mensajeCaja.textContent = `${error.message} Si perdiste la conexión, actualiza la lista para comprobar el estado.`;
            mensajeCaja.classList.add("caja-error");
            mensajeCaja.hidden = false;
            mensajeCaja.scrollIntoView({ behavior: "smooth", block: "center" });
            controles.forEach((control) => { control.disabled = false; });
        }
    });
});
