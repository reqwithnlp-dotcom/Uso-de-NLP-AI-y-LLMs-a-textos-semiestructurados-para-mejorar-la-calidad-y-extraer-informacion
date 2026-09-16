async function mostrarResultado() {
    const textarea = document.getElementById("editor-texto");
    const texto = textarea ? textarea.value : "";

    if (!texto.trim()) {
        alert("Por favor, ingresa algún texto para analizar.");
        return;
    }

    // 1. Obtener estados de los checkboxes del formulario
    const voz_pasiva = document.getElementById("voz-pasiva")?.checked || false;
    const word_repetition = document.getElementById("word-repetition")?.checked || false;
    const adverbs = document.getElementById("adv")?.checked || false;
    const modales = document.getElementById("modal")?.checked || false;
    const cliches = document.getElementById("cliches")?.checked || false;
    const abstract_words = document.getElementById("abstract-words")?.checked || false;
    const weakverbs = document.getElementById("weak-verbs")?.checked || false;
    const impersonal_sentences = document.getElementById("impersonal-sentences")?.checked || false;
    const negative_phrases = document.getElementById("negative-phrase")?.checked || false;
    const opinion_perception = document.getElementById("opinion-perception")?.checked || false;
    const unusual_punctuation = document.getElementById("unusual-punctuation")?.checked || false;
    const tenses = document.getElementById("tenses")?.checked || false;
    const logical_connectors = document.getElementById("logical-connectors")?.checked || false;
    const readability_metric = document.getElementById("readability-metric")?.checked || false;

    const resultados = [];
    const promesas = [];

    // Helper para agregar resultados
    const agregarResultado = (tipo, mensaje) => {
        resultados.push({ tipo, mensaje });
    };

    // Helper para validar URLs inyectadas por Django
    const getApiUrl = (urlVar, fallback) => {
        return (typeof urlVar !== 'undefined' && urlVar && urlVar !== 'None' && urlVar !== '{{' + urlVar + '}}') 
            ? urlVar 
            : fallback;
    };

    // --- Calidad del texto ---

  // Voz Pasiva
if (voz_pasiva) {
    const url = getApiUrl(
        typeof API_VOZ_PASIVA_URL !== 'undefined'
        ? API_VOZ_PASIVA_URL
        : null,
    "http://163.10.5.49:8009"
    );

    if (url) {
        const p = fetch(`${url}/detectar_voz_pasiva`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                texto: texto
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const mensaje = data.is_passive
                ? "Se detect� voz pasiva"
                : "No se detect� voz pasiva";

            agregarResultado("Voz Pasiva", mensaje);
        })
        .catch(err => {
            agregarResultado(
                "Error",
                "Error en voz pasiva: " + err.message
            );
        });

        promesas.push(p);
    }
}
    if (word_repetition) {
    const url = getApiUrl(typeof API_WORD_REPETITION_URL !== 'undefined' ? API_WORD_REPETITION_URL : null, "http://163.10.5.49:8011");
    
    const p = fetch(`${url}/repeticiones`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            texto: texto,
            sin_palabras_frecuentes: true,
            con_sustantivos_en_singular: false
        })
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    })
    .then(data => {
        const repeticiones = Object.entries(data)
            .map(([palabra, cantidad]) => `${palabra}: ${cantidad}`)
            .join(", ");
        agregarResultado("Repeticiones", repeticiones || "No se encontraron repeticiones");
    })
    .catch(err => agregarResultado("Error", "Error en repeticiones: " + err.message));
    
    promesas.push(p);
}
    // Adverbios
    if (adverbs) {
        const url = getApiUrl(typeof API_ADVERBS_URL !== 'undefined' ? API_ADVERBS_URL : null, "http://163.10.5.49:8005");
        const p = fetch(`${url}/analizar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const listaAdverbios = data.adverbs || (Array.isArray(data) ? data : []);
            if (listaAdverbios.length > 0) {
                listaAdverbios.forEach(item => {
                    agregarResultado("Adverbios", `"Word": ${item.word} | "Category": ${item.category}`);
                });
            } else {
                agregarResultado("Adverbios", "No se detectaron adverbios");
            }
        })
        .catch(err => agregarResultado("Error", "Error en Adverbios: " + err.message));
        promesas.push(p);
    }

    // Verbos Modales
    if (modales) {
        const url = getApiUrl(typeof API_MODAL_VERBS_URL !== 'undefined' ? API_MODAL_VERBS_URL : null, "http://163.10.5.49:8006");
        const p = fetch(`${url}/analizar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const lista = data.inconsistencies || [];
            if (lista.length > 0) {
                lista.forEach((item, index) => {
                    agregarResultado("Verbos Modales", `Inconsistencia ${index + 1} Modal: "${item.shared_action}"`);
                });
            } else {
                agregarResultado("Verbos Modales", "No se detectaron inconsistencias");
            }
        })
        .catch(err => agregarResultado("Error", "Error en Verbos Modales: " + err.message));
        promesas.push(p);
    }

    // Clichés
    if (cliches) {
        const url = getApiUrl(typeof API_CLICHES_URL !== 'undefined' ? API_CLICHES_URL : null, "http://163.10.5.49:8004");
        const p = fetch(`${url}/detectar_cliches/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const lista = data.cliches_encontrados || [];
            if (Array.isArray(lista) && lista.length > 0) {
                agregarResultado("Clichés", lista.join(", "));
            } else {
                agregarResultado("Clichés", "No se detectaron clichés");
            }
        })
        .catch(err => agregarResultado("Error", "Error en clichés: " + err.message));
        promesas.push(p);
    }

    // Palabras Abstractas
if (abstract_words) {
    const url = getApiUrl(
        typeof API_ABSTRACT_WORDS_URL !== 'undefined'
            ? API_ABSTRACT_WORDS_URL
            : null,
            "http://163.10.5.49:8010"
    );

    if (url) {
        const p = fetch(`${url}/predict`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: texto
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const resultados = data.results || [];

            if (Array.isArray(resultados) && resultados.length > 0) {
                agregarResultado(
                    "Palabras Abstractas",
                    resultados.join(", ")
                );
            } else {
                agregarResultado(
                    "Palabras Abstractas",
                    "No se encontraron palabras abstractas"
                );
            }
        })
        .catch(err => {
            agregarResultado(
                "Error",
                "Error en palabras abstractas: " + err.message
            );
        });

        promesas.push(p);
    }
}

    // Verbos Débiles
    if (weakverbs) {
        const urlWeak = typeof API_WEAK_VERBS__URL !== 'undefined' ? API_WEAK_VERBS__URL : (typeof API_WEAK_VERBS_URL !== 'undefined' ? API_WEAK_VERBS_URL : null);
        const url = getApiUrl(urlWeak, "http://163.10.5.49:8001");
        const p = fetch(`${url}/weak_verbs`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data && Object.keys(data).length > 0) {
                Object.entries(data).forEach(([verbo, info]) => {
                    agregarResultado("Verbos Débiles", `${verbo}: ${typeof info === 'object' ? JSON.stringify(info) : info}`);
                });
            } else {
                agregarResultado("Verbos Débiles", "No se detectaron verbos débiles");
            }
        })
        .catch(err => agregarResultado("Error", "Error en verbos débiles: " + err.message));
        promesas.push(p);
    }

    // --- Estructura y Gramática ---

    // Oraciones Impersonales
    if (impersonal_sentences) {
        const url = getApiUrl(typeof API_IMPERSONAL_SENTENCES_URL !== 'undefined' ? API_IMPERSONAL_SENTENCES_URL : null, "http://163.10.5.49:8002");
        const p = fetch(`${url}/analyze`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (Array.isArray(data.results) && data.results.length > 0) {
                data.results.forEach(item => {
                    const textoOracion = item.sentence || "Texto no disponible";
                    let mensaje = "";

                    if (item.type === "WEATHER_IT") {
                        mensaje = `Impersonal (Clima): "${textoOracion}"`;
                    } else if (item.personal === true) {
                        const subtipo = item.personal_type ? ` (${item.personal_type})` : "";
                        mensaje = `Personal${subtipo}: "${textoOracion}"`;
                    } else if (item.ambiguous === true) {
                        mensaje = `Ambigua: "${textoOracion}"`;
                    } else {
                        mensaje = `${item.type || "Desconocido"}: "${textoOracion}"`;
                    }

                    agregarResultado("Oraciones Impersonales", mensaje);
                });
            } else {
                agregarResultado("Oraciones Impersonales", "No se detectaron patrones impersonales.");
            }
        })
        .catch(err => agregarResultado("Error", "Error en oraciones impersonales: " + err.message));
        promesas.push(p);
    }

    // Frases Negativas
    if (negative_phrases) {
        const url = getApiUrl(typeof API_NEGATIVE_PHRASE_URL !== 'undefined' ? API_NEGATIVE_PHRASE_URL : null, "http://163.10.5.49:8003");
        const p = fetch(`${url}/detect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const resultado = Array.isArray(data) ? data[1] : data;
            agregarResultado("Frases Negativas", resultado ? "Detectadas" : "No detectadas");
        })
        .catch(err => agregarResultado("Error", "Error en frases negativas: " + err.message));
        promesas.push(p);
    }

    // Opinión o Percepción
    if (opinion_perception) {
        const url = getApiUrl(typeof API_OPINION_PERCEPTION_URL !== 'undefined' ? API_OPINION_PERCEPTION_URL : null, "http://163.10.5.49:8000");
        const p = fetch(`${url}/perception-opinion`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data.opinion_perception && data.opinion_perception.length > 0) {
                data.opinion_perception.forEach(item => {
                    agregarResultado("Opinión/Percepción", `Verbo detectado: ${item}`);
                });
            } else {
                agregarResultado("Opinión/Percepción", "No se detectaron verbos de opinión o percepción");
            }
        })
        .catch(err => agregarResultado("Error", "Error en opinión/percepción: " + err.message));
        promesas.push(p);
    }

    // Puntuación Inusual
    if (unusual_punctuation) {
    const url = getApiUrl(
        typeof API_UNUSUAL_PUNCT_URL !== 'undefined' ? API_UNUSUAL_PUNCT_URL : null,
        "http://163.10.5.49:8012"
    );

    if (url) {
        const p = fetch(`${url}/detect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            if (data && data.unusual_punctuation) {
                const posiciones = Array.isArray(data.positions) 
                    ? data.positions.join(", ") 
                    : data.positions;

                agregarResultado("Puntuaci�n", `Se detect� puntuaci�n inusual: ${posiciones}`);
            } else {
                agregarResultado("Puntuaci�n", "No se detectaron errores de puntuaci�n");
            }
        })
        .catch(err => agregarResultado("Error", "Error en puntuaci�n: " + err.message));

        promesas.push(p);
    }
}
    // Tiempos Verbales
    if (tenses) {
        const url = getApiUrl(typeof API_TENSES_URL !== 'undefined' ? API_TENSES_URL : null, null);
        if (url) {
            const p = fetch(`${url}/deteccion_de_verbos/?texto=${encodeURIComponent(texto)}`)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
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
    }

    // Conectores Lógicos
    if (logical_connectors) {
        const url = getApiUrl(typeof API_LOGICAL_CONNECTORS_URL !== 'undefined' ? API_LOGICAL_CONNECTORS_URL : null, "http://163.10.5.49:8007");
        const p = fetch(`${url}/detect`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: texto })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            const conectores = data.connectors_found || [];
            if (conectores.length > 0) {
                conectores.forEach(item => {
                    const conectorTexto = typeof item === "object"
                        ? (item.connector || item.word || item.text || JSON.stringify(item))
                        : item;
                    agregarResultado("Conectores Lógicos", `Conector detectado: ${conectorTexto}`);
                });
            } else {
                agregarResultado("Conectores Lógicos", "No se detectaron conectores lógicos");
            }
        })
        .catch(err => agregarResultado("Error", "Error en conectores lógicos: " + err.message));
        promesas.push(p);
    }

    // --- Legibilidad ---
   if (readability_metric) {
    const url = getApiUrl(
        typeof API_READABILITY_METRIC_URL !== 'undefined'
            ? API_READABILITY_METRIC_URL
            : null,
        "http://163.10.5.49:8008"
    );

    const p = fetch(`${url}/analizar`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            texto: texto
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return response.json();
    })
    .then(data => {
        console.log("Respuesta Legibilidad:", data);

        const score = typeof data.score === "number"
            ? data.score.toFixed(2)
            : "N/A";

        const gunningFog = typeof data.gunning_fog === "number"
            ? data.gunning_fog.toFixed(2)
            : "N/A";

        agregarResultado(
            "Legibilidad",
            `Puntaje: ${score}, Gunning Fog: ${gunningFog}`
        );
    })
    .catch(err => {
        console.error("Error en legibilidad:", err);
        agregarResultado(
            "Error",
            "Error en legibilidad: " + err.message
        );
    });

    promesas.push(p);
}
    // Renderizar estado de carga en la UI
    const contenedor = document.getElementById('resultados-items');
    const estadoVacio = document.getElementById('estado-vacio');

    if (contenedor) {
        if (estadoVacio) estadoVacio.style.display = 'none';
        contenedor.innerHTML = '<div class="text-center py-3 text-secondary"><div class="spinner-border spinner-border-sm me-2" role="status"></div>Analizando texto...</div>';
    }

    // Esperar todas las peticiones concurrentes
    await Promise.all(promesas);

    if (!contenedor) return;

    if (resultados.length === 0) {
        if (estadoVacio) estadoVacio.style.display = 'block';
        contenedor.innerHTML = '';
        return;
    }

    // Agrupar por categoría
    const grupos = {};
    resultados.forEach(resultado => {
        const tipo = resultado.tipo || 'General';
        if (!grupos[tipo]) grupos[tipo] = [];
        grupos[tipo].push(resultado.mensaje);
    });

    // Renderizar HTML final
    let html = '';
    Object.entries(grupos).forEach(([tipo, items]) => {
        const esError = tipo.toLowerCase() === 'error';
        const iconoClase = esError ? 'danger' : 'warning';
        const icono = esError ? 'bi-x-circle' : 'bi-exclamation-triangle';

        html += `
            <div class="mb-3">
                <h4 style="font-size: 0.875rem; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-secondary);">
                    ${tipo} <span class="badge ${esError ? 'bg-danger' : 'bg-secondary'}">${items.length}</span>
                </h4>
                ${items.map(item => `
                    <div class="result-card">
                        <div class="result-icon ${iconoClase}">
                            <i class="bi ${icono}"></i>
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

// 1. Exponer al ámbito global para el onclick del HTML
window.mostrarResultado = mostrarResultado;

// 2. Enlazar automáticamente al botón por clase o selector al cargar el DOM
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.btn-analyze');
    if (btn) {
        btn.addEventListener('click', mostrarResultado);
    }
});