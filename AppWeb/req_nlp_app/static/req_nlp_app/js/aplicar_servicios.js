async function mostrarResultado() {
    const textarea = document.getElementById("editor-texto");
    const texto = textarea.value;
    
    if (!texto.trim()) {
        alert("Por favor, ingresa algún texto para analizar.");
        return;
    }

    // Obtener estados de los checkboxes
    const invertir = document.getElementById("invertir-texto")?.checked || false;
    const voz_pasiva = document.getElementById("voz-pasiva")?.checked || false;
    const word_repetition = document.getElementById("word-repetition")?.checked || false;
    const impersonal_sentences = document.getElementById("impersonal-sentences")?.checked || false;
    const negative_phrases = document.getElementById("negative-phrase")?.checked || false;
    const opinion_perception = document.getElementById("opinion-perception")?.checked || false;
    const unusual_punctuation = document.getElementById("unusual-punctuation")?.checked || false;
    const abstract_words = document.getElementById("abstract-words")?.checked || false;
    const logical_connectors = document.getElementById("logical-connectors")?.checked || false;
    const readability_metric = document.getElementById("readability-metric")?.checked || false;
    const tenses = document.getElementById("tenses")?.checked || false;
    const cliches = document.getElementById("cliches")?.checked || false;
    const weakverbs = document.getElementById("weak-verbs")?.checked || false;

    const resultados = [];
    const promesas = [];

    // Helper para agregar resultados de forma consistente
    const agregarResultado = (tipo, mensaje) => {
        resultados.push({ tipo, mensaje });
    };

    if (invertir) {
        const p = fetch(`${API_INVERTIR_TEXTO_URL}/invertir_texto/?texto=${encodeURIComponent(texto)}`)
            .then(response => response.json())
            .then(data => agregarResultado("Texto Invertido", data.respuesta))
            .catch(error => agregarResultado("Error", "Error al invertir: " + error.message));
        promesas.push(p);
    }

    if (voz_pasiva) {
        const p = fetch(`${API_VOZ_PASIVA_URL}/convertir`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => agregarResultado("Voz Pasiva", "Voz activa: " + data.activa))
        .catch(err => agregarResultado("Error", "Error en voz pasiva: " + err.message));
        promesas.push(p);
    }

    if (weakverbs) {
        const p = fetch(`http://163.10.5.49:8001/weak_verbs`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            console.log("Weak verbs response:", data);
            if (data && Object.keys(data).length > 0) {
                Object.entries(data).forEach(([verbo, info]) => {
                    agregarResultado("Verbos Débiles", `${verbo}: ${JSON.stringify(info)}`);
                });
            } else {
                agregarResultado("Verbos Débiles", "No se detectaron verbos débiles");
            }
        })
        .catch(err => agregarResultado("Error", "Error en verbos débiles: " + err.message));
        promesas.push(p);
    }

    if (word_repetition) {
        const p = fetch(`${API_WORD_REPETITION_URL}/repeticiones`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                texto: texto,
                sin_palabras_frecuentes: true,
                con_sustantivos_en_singular: false
            })
        })
        .then(response => response.json())
        .then(data => {
            const repeticiones = Object.entries(data)
                .map(([palabra, cantidad]) => `${palabra}: ${cantidad}`)
                .join(", ");
            agregarResultado("Repeticiones", repeticiones || "No se encontraron repeticiones");
        })
        .catch(err => agregarResultado("Error", "Error en repeticiones: " + err.message));
        promesas.push(p);
    }

    if (impersonal_sentences) {
        const p = fetch(`http://163.10.5.49:8002/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            // Verificamos que exista el array results
            if (Array.isArray(data.results) && data.results.length > 0) {
                
                data.results.forEach(item => {
                    // 1. Obtenemos el texto real usando la propiedad correcta: 'sentence'
                    const textoOracion = item.sentence || "Texto no disponible";
                    let mensaje = "";

                    // 2. Lógica para armar el mensaje según el tipo
                    if (item.type === "WEATHER_IT") {
                        mensaje = `Impersonal (Clima): "${textoOracion}"`;
                    } 
                    else if (item.personal === true) {
                        // Si es personal, mostramos el subtipo (ej: PRONOUN_SUBJECT)
                        const subtipo = item.personal_type ? ` (${item.personal_type})` : "";
                        mensaje = `Personal${subtipo}: "${textoOracion}"`;
                    } 
                    else if (item.ambiguous === true) {
                        mensaje = `Ambigua: "${textoOracion}"`;
                    } 
                    else {
                        // Fallback por si hay otro tipo no contemplado
                        mensaje = `${item.type || "Desconocido"}: "${textoOracion}"`;
                    }

                    agregarResultado("Oraciones Impersonales", mensaje);
                });

            } else {
                agregarResultado("Oraciones Impersonales", "No se detectaron patrones impersonales.");
            }
        })
        .catch(err => {
            console.error("Error en impersonal sentences:", err);
            agregarResultado("Error", "Error al analizar oraciones: " + err.message);
        });
        promesas.push(p);
    }

    if (negative_phrases) {
        const p = fetch(`${API_NEGATIVE_PHRASE_URL}/negativaCompleja`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta frases negativas:", data);
            const resultado = Array.isArray(data) ? data[0] : data;
            agregarResultado("Frases Negativas", resultado ? "Sí" : "No");
        })
        .catch(err => agregarResultado("Error", "Error en frases negativas: " + err.message));
        promesas.push(p);
    }

    if (opinion_perception) {
        const p = fetch(`http://163.10.5.49:8000/perception-opinion`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Respuesta opinion perception:", data);
            if (data.opinion_perception && data.opinion_perception.length > 0) {
                data.opinion_perception.forEach(item => {
                    agregarResultado("Opinión/Percepción", `Verbo detectado: ${item}`);
                });
            } else {
                agregarResultado("Opinión/Percepción", "No se detectaron verbos de opinión o percepción");
            }
        })
        .catch(err => {
            console.error("Error en opinion perception:", err);
            agregarResultado("Error", "Error en opinión/percepción: " + err.message);
        });
        promesas.push(p);
    }

    if (unusual_punctuation) {
        const p = fetch(`${API_UNUSUAL_PUNCTUATION_URL}/detectar-puntuacion`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sentence: texto })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta puntuación:", data);
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(error => {
                    const posiciones = Array.isArray(error.posición) ? error.posición.join("-") : "N/A";
                    agregarResultado("Puntuación", 
                        `Error: ${error.descripción}, Texto: "${error.texto}", Posición: ${posiciones}`
                    );
                });
            } else {
                agregarResultado("Puntuación", "No se detectaron errores de puntuación");
            }
        })
        .catch(err => {
            console.error("Error en puntuación:", err);
            agregarResultado("Error", "Error en análisis de puntuación: " + err.message);
        });
        promesas.push(p);
    }

    if (abstract_words) {
        const params = new URLSearchParams({ texto: texto });
        const p = fetch(`${API_ABSTRACT_WORDS_URL}/abstractas/?${params.toString()}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.respuesta && Array.isArray(data.respuesta) && data.respuesta.length > 0) {
                agregarResultado("Palabras Abstractas", data.respuesta.join(", "));
            } else {
                agregarResultado("Palabras Abstractas", "No se encontraron palabras abstractas");
            }
        })
        .catch(err => agregarResultado("Error", "Error en palabras abstractas: " + err.message));
        promesas.push(p);
    }

    if (logical_connectors) {
        const p = fetch(`${API_LOGICAL_CONNECTORS_URL}/conectores-logicos/?texto=${encodeURIComponent(texto)}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data.conectores) && data.conectores.length > 0) {
                agregarResultado("Conectores Lógicos", data.conectores.join(", "));
            } else {
                agregarResultado("Conectores Lógicos", "No se encontraron conectores lógicos");
            }
        })
        .catch(err => agregarResultado("Error", "Error en conectores lógicos: " + err.message));
        promesas.push(p);
    }

    if (readability_metric) {
        const p = fetch(`${API_READABILITY_METRIC_URL}/metrica-legibilidad/?texto=${encodeURIComponent(texto)}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            agregarResultado("Legibilidad", 
                `Puntaje: ${data["Puntaje"]?.toFixed(2) || 'N/A'}, Nivel: ${data["Nivel de legibilidad"] || 'N/A'}`
            );
        })
        .catch(err => agregarResultado("Error", "Error en legibilidad: " + err.message));
        promesas.push(p);
    }

    if (tenses) {
        const p = fetch(`${API_TENSES_URL}/deteccion_de_verbos/?texto=${encodeURIComponent(texto)}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                const resultadosTiempos = data.map(([verbo, tiempo]) => `${verbo}: ${tiempo}`).join("; ");
                agregarResultado("Tiempos Verbales", resultadosTiempos);
            } else {
                agregarResultado("Tiempos Verbales", "No se detectaron tiempos verbales");
            }
        })
        .catch(err => agregarResultado("Error", "Error en tiempos verbales: " + err.message));
        promesas.push(p);
    }

    if (cliches) {
        const p = fetch(`${API_CLICHES_URL}/detectar_cliches/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data.cliches_encontrados) && data.cliches_encontrados.length > 0) {
                agregarResultado("Clichés", data.cliches_encontrados.join(", "));
            } else {
                agregarResultado("Clichés", "No se detectaron clichés");
            }
        })
        .catch(err => agregarResultado("Error", "Error en clichés: " + err.message));
        promesas.push(p);
    }

    if (promesas.length === 0) {
        agregarResultado("Info", "No se seleccionó ninguna opción de análisis");
    }

    // Esperar a que todas las promesas se completen
    try {
        await Promise.all(promesas);
    } catch (error) {
        console.error("Error general:", error);
        agregarResultado("Error", "Ocurrió un error inesperado: " + error.message);
    }

    // Mostrar resultados
    const contenedor = document.getElementById('resultados-items');
    const estadoVacio = document.getElementById('estado-vacio');

    if (!contenedor) {
        console.error("Elemento 'resultados-items' no encontrado");
        return;
    }

    if (resultados.length === 0) {
        if (estadoVacio) estadoVacio.style.display = 'block';
        contenedor.innerHTML = '';
    } else {
        if (estadoVacio) estadoVacio.style.display = 'none';
        
        // Agrupar por tipo de indicador
        const grupos = {};
        resultados.forEach(resultado => {
            const tipo = resultado.tipo || 'General';
            if (!grupos[tipo]) grupos[tipo] = [];
            grupos[tipo].push(resultado.mensaje);
        });
        
        let html = '';
        Object.entries(grupos).forEach(([tipo, items]) => {
            html += `
                <div class="mb-3">
                    <h4 style="font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-secondary);">
                        ${tipo} <span class="badge bg-secondary">${items.length}</span>
                    </h4>
                    ${items.map(item => `
                        <div class="result-card">
                            <div class="result-icon warning">
                                <i class="bi bi-exclamation-triangle"></i>
                            </div>
                            <div class="result-content">
                                <p class="result-desc">${item}</p>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        });
        
        contenedor.innerHTML = html;
    }
}