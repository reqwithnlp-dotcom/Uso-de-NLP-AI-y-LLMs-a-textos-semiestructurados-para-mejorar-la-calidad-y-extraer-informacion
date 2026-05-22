let BACKEND_URL = null;

async function cargarConfiguracion() {
    try {
        const response = await fetch("/config/");
        const config = await response.json();
        BACKEND_URL = config.backend_url;
        console.log("[DEBUG] BACKEND_URL cargada:", BACKEND_URL);
    } catch (error) {
        console.error("[ERROR] No se pudo cargar la configuración:", error);
    }
}

document.addEventListener("DOMContentLoaded", cargarConfiguracion);


function getBaseUrl() {
    if (BACKEND_URL) return BACKEND_URL;

   
}
