const mensajeCocina = document.getElementById("cocina-mensaje");
const confirmacionCocina = document.getElementById("confirmacion-cocina");
const detalleConfirmacionCocina = document.getElementById("detalle-confirmacion-cocina");

const resultadoCocina = sessionStorage.getItem("resultado-cocina");
if (resultadoCocina) {
    mensajeCocina.textContent = resultadoCocina;
    mensajeCocina.hidden = false;
    sessionStorage.removeItem("resultado-cocina");
}

function confirmarAvance(pregunta) {
    detalleConfirmacionCocina.textContent = pregunta;
    confirmacionCocina.returnValue = "volver";
    return new Promise((resolver) => {
        confirmacionCocina.addEventListener("close", () => {
            resolver(confirmacionCocina.returnValue === "confirmar");
        }, { once: true });
        confirmacionCocina.showModal();
    });
}

document.querySelectorAll(".pedido-cocina .cocina-acciones button").forEach((boton) => {
    boton.addEventListener("click", async () => {
        const numero = boton.dataset.numero;
        const estado = boton.dataset.estado;
        const pregunta = estado === "ENTREGADO"
            ? `¿Confirmas que el pedido #${numero} ya fue entregado al estudiante?`
            : `¿Cambiar el pedido #${numero} a ${estado.toLowerCase()}?`;
        if (!await confirmarAvance(pregunta)) return;

        boton.disabled = true;
        mensajeCocina.hidden = true;
        try {
            const respuesta = await fetch(boton.dataset.url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ estado }),
            });
            const datos = await respuesta.json();
            if (!respuesta.ok) throw new Error(datos.error || "No se pudo actualizar el pedido.");
            sessionStorage.setItem("resultado-cocina", `Pedido #${numero}: ${estado.toLowerCase()}.`);
            window.location.reload();
        } catch (error) {
            mensajeCocina.textContent = `${error.message} Actualiza los pedidos para comprobar su estado.`;
            mensajeCocina.classList.add("caja-error");
            mensajeCocina.hidden = false;
            mensajeCocina.scrollIntoView({ behavior: "smooth", block: "center" });
            boton.disabled = false;
        }
    });
});
