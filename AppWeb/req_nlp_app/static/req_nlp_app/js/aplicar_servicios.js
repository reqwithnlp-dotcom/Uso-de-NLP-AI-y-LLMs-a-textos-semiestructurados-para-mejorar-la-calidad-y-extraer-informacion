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
    const povshift = document.getElementById("povshift")?.checked || false;
    const logical_connectors = document.getElementById("logical-connectors")?.checked || false;
    const readability_metric = document.getElementById("readability-metric")?.checked || false;

    const resultados = [];
    const promesas = [];

    // Helper para agregar resultados
    const agregarResultado = (tipo, mensaje) => {
        resultados.push({ tipo, mensaje });
    };

    // Helper para validar URLs inyectadas por Django con fallback local seguro
    const getApiUrl = (urlVar, fallback) => {
        return (typeof urlVar !== 'undefined' && urlVar && urlVar !== 'None' && urlVar !== '{{' + urlVar + '}}') 
            ? urlVar 
            : fallback;
    };

    // ==========================================
    // 1. Calidad del texto
    // ==========================================

    // Voz Pasiva (Puerto 8011)
    if (voz_pasiva) {
        const url = getApiUrl(typeof API_VOZ_PASIVA_URL !== 'undefined' ? API_VOZ_PASIVA_URL : null, "http://127.0.0.1:8011");
        if (url) {
            const p = fetch(`${url}/detectar_voz_pasiva`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ texto: texto })
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                const mensaje = data.is_passive ? "Se detectó voz pasiva" : "No se detectó voz pasiva";
                agregarResultado("Voz Pasiva", mensaje);
            })
            .catch(err => agregarResultado("Error", "Error en voz pasiva: " + err.message));
            promesas.push(p);
        }
    }

    // Repetición de Palabras (Puerto 8002)
    if (word_repetition) {
        const url = getApiUrl(typeof API_WORD_REPETITION_URL !== 'undefined' ? API_WORD_REPETITION_URL : null, "http://127.0.0.1:8002");
        if (url) {
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
    }

    // Adverbios (Puerto 8007)
    if (adverbs) {
        const url = getApiUrl(typeof API_ADVERBS_URL !== 'undefined' ? API_ADVERBS_URL : null, "http://127.0.0.1:8007");
        if (url) {
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
                        agregarResultado("Adverbios", `"${item.word}" (Categoría: ${item.category})`);
                    });
                } else {
                    agregarResultado("Adverbios", "No se detectaron adverbios");
                }
            })
            .catch(err => agregarResultado("Error", "Error en Adverbios: " + err.message));
            promesas.push(p);
        }
    }

    // Verbos Modales (Puerto 8006)
    if (modales) {
        const url = getApiUrl(typeof API_MODAL_VERBS_URL !== 'undefined' ? API_MODAL_VERBS_URL : null, "http://127.0.0.1:8006");
        if (url) {
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
                        agregarResultado("Verbos Modales", `Inconsistencia ${index + 1}: acción compartida "${item.shared_action}"`);
                    });
                } else {
                    agregarResultado("Verbos Modales", "No se detectaron inconsistencias de verbos modales");
                }
            })
            .catch(err => agregarResultado("Error", "Error en Verbos Modales: " + err.message));
            promesas.push(p);
        }
    }

    // Clichés (Puerto 8001)
    if (cliches) {
        const url = getApiUrl(typeof API_CLICHES_URL !== 'undefined' ? API_CLICHES_URL : null, "http://127.0.0.1:8001");
        if (url) {
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
    }

    // Palabras Abstractas (Puerto 8013)
    if (abstract_words) {
        const url = getApiUrl(typeof API_ABSTRACT_WORDS_URL !== 'undefined' ? API_ABSTRACT_WORDS_URL : null, "http://127.0.0.1:8013");
        if (url) {
            const p = fetch(`${url}/predict`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text: texto })
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                const items = data.results || [];
                if (Array.isArray(items) && items.length > 0) {
                    agregarResultado("Palabras Abstractas", items.join(", "));
                } else {
                    agregarResultado("Palabras Abstractas", "No se encontraron palabras abstractas");
                }
            })
            .catch(err => agregarResultado("Error", "Error en palabras abstractas: " + err.message));
            promesas.push(p);
        }
    }

    // Verbos Débiles (Puerto 8012)
    if (weakverbs) {
        const urlWeak = typeof API_WEAK_VERBS_URL !== 'undefined' ? API_WEAK_VERBS_URL : (typeof API_WEAK_VERBS__URL !== 'undefined' ? API_WEAK_VERBS__URL : null);
        const url = getApiUrl(urlWeak, "http://127.0.0.1:8012");
        if (url) {
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
                if (Array.isArray(data)) {
                    if (data.length > 0) {
                        agregarResultado("Verbos Débiles", `Detectados: ${data.join(", ")}`);
                    } else {
                        agregarResultado("Verbos Débiles", "No se detectaron verbos débiles");
                    }
                } else if (data && typeof data === 'object') {
                    const entries = Object.entries(data);
                    if (entries.length > 0) {
                        entries.forEach(([verbo, info]) => {
                            agregarResultado("Verbos Débiles", `${verbo}: ${typeof info === 'object' ? JSON.stringify(info) : info}`);
                        });
                    } else {
                        agregarResultado("Verbos Débiles", "No se detectaron verbos débiles");
                    }
                } else {
                    agregarResultado("Verbos Débiles", "No se detectaron verbos débiles");
                }
            })
            .catch(err => agregarResultado("Error", "Error en verbos débiles: " + err.message));
            promesas.push(p);
        }
    }

    // ==========================================
    // 2. Estructura y Gramática
    // ==========================================

    // Oraciones Impersonales (Puerto 8009)
    if (impersonal_sentences) {
        const url = getApiUrl(typeof API_IMPERSONAL_SENTENCES_URL !== 'undefined' ? API_IMPERSONAL_SENTENCES_URL : null, "http://127.0.0.1:8009");
        if (url) {
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
                    agregarResultado("Oraciones Impersonales", "No se detectaron patrones impersonales");
                }
            })
            .catch(err => agregarResultado("Error", "Error en oraciones impersonales: " + err.message));
            promesas.push(p);
        }
    }

    // Frases Negativas / Doble Negación (Puerto 8004)
    if (negative_phrases) {
        const url = getApiUrl(typeof API_NEGATIVE_PHRASE_URL !== 'undefined' ? API_NEGATIVE_PHRASE_URL : null, "http://127.0.0.1:8004");
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
                const tieneDoble = typeof data.has_double_negation === 'boolean'
                    ? data.has_double_negation
                    : (Array.isArray(data) ? Boolean(data[1]) : Boolean(data.detected || data.result));
                agregarResultado("Frases Negativas", tieneDoble ? "Doble negación detectada" : "No se detectó doble negación");
            })
            .catch(err => agregarResultado("Error", "Error en frases negativas: " + err.message));
            promesas.push(p);
        }
    }

    // Opinión o Percepción (Puerto 8010)
    if (opinion_perception) {
        const url = getApiUrl(typeof API_OPINION_PERCEPTION_URL !== 'undefined' ? API_OPINION_PERCEPTION_URL : null, "http://127.0.0.1:8010");
        if (url) {
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
    }

    // Puntuación Inusual (Puerto 8005)
    if (unusual_punctuation) {
        const urlPunct = typeof API_UNUSUAL_PUNCTUATION_URL !== 'undefined' 
            ? API_UNUSUAL_PUNCTUATION_URL 
            : (typeof API_UNUSUAL_PUNCT_URL !== 'undefined' ? API_UNUSUAL_PUNCT_URL : null);
        const url = getApiUrl(urlPunct, "http://127.0.0.1:8005");

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
                    agregarResultado("Puntuación Inusual", `Detectada en posiciones: ${posiciones}`);
                } else {
                    agregarResultado("Puntuación Inusual", "No se detectaron errores de puntuación");
                }
            })
            .catch(err => agregarResultado("Error", "Error en puntuación inusual: " + err.message));
            promesas.push(p);
        }
    }

    // Inconsistencias en Tiempos Verbales (Puerto 8015)
    if (tenses) {
        const url = getApiUrl(typeof API_TENSES_URL !== 'undefined' ? API_TENSES_URL : null, "http://127.0.0.1:8015");
        if (url) {
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
                const issues = data.issues || [];
                if (Array.isArray(issues) && issues.length > 0) {
                    issues.forEach(item => {
                        const expl = item.explanation || item.error_code || "Inconsistencia";
                        const frag = item.fragment ? ` (en "${item.fragment}")` : "";
                        agregarResultado("Tiempos Verbales", `${expl}${frag}`);
                    });
                } else {
                    agregarResultado("Tiempos Verbales", "No se detectaron inconsistencias de tiempos verbales");
                }
            })
            .catch(err => agregarResultado("Error", "Error en tiempos verbales: " + err.message));
            promesas.push(p);
        }
    }

    // Cambio de Punto de Vista - POV Shift (Puerto 8014)
    if (povshift) {
        const url = getApiUrl(typeof API_POVSHIFT_URL !== 'undefined' ? API_POVSHIFT_URL : null, "http://127.0.0.1:8014");
        if (url) {
            const p = fetch(`${url}/detect`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ texto: texto })
            })
            .then(response => {
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                return response.json();
            })
            .then(data => {
                const shifts = Array.isArray(data) ? data : (data.shifts || []);
                if (shifts.length > 0) {
                    shifts.forEach(shift => {
                        const de = shift.from_character?.canonical_name || "personaje previo";
                        const a = shift.to_character?.canonical_name || "nuevo personaje";
                        const conf = typeof shift.confidence === "number" ? ` (${Math.round(shift.confidence * 100)}% conf.)` : "";
                        const evidencia = shift.evidence ? `: "${shift.evidence}"` : "";
                        agregarResultado("Punto de Vista (POV)", `Cambio de ${de} a ${a}${conf}${evidencia}`);
                    });
                } else {
                    agregarResultado("Punto de Vista (POV)", "No se detectaron cambios de punto de vista");
                }
            })
            .catch(err => agregarResultado("Error", "Error en punto de vista (POV): " + err.message));
            promesas.push(p);
        }
    }

    // Conectores Lógicos (Puerto 8003)
    if (logical_connectors) {
        const url = getApiUrl(typeof API_LOGICAL_CONNECTORS_URL !== 'undefined' ? API_LOGICAL_CONNECTORS_URL : null, "http://127.0.0.1:8003");
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
    }

    // ==========================================
    // 3. Legibilidad
    // ==========================================

    // Métricas de Legibilidad (Puerto 8008)
    if (readability_metric) {
        const url = getApiUrl(typeof API_READABILITY_METRIC_URL !== 'undefined' ? API_READABILITY_METRIC_URL : null, "http://127.0.0.1:8008");
        if (url) {
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
                const score = typeof data.score === "number" ? data.score.toFixed(2) : "N/A";
                const gunningFog = typeof data.gunning_fog === "number" ? data.gunning_fog.toFixed(2) : "N/A";
                agregarResultado("Legibilidad", `Puntaje: ${score}, Gunning Fog: ${gunningFog}`);
            })
            .catch(err => agregarResultado("Error", "Error en legibilidad: " + err.message));
            promesas.push(p);
        }
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

// ==========================================
// 4. Catálogo de Ejemplos de Prueba
// ==========================================
const EJEMPLOS_PRUEBA = {
    "completo": {
        texto: "At the end of the day, the system was created by the developer very quickly. The user shall configure the portal, but the user may configure the portal later. We believe that the application feels extremely responsive, although it cannot not fail under heavy load?? John started the process, and suddenly Mary felt that the decision was necessary. Yesterday the system crashed and today it runs smoothly.",
        indicators: "all"
    },
    "voz-pasiva": {
        texto: "The security report was generated by the automated server yesterday.",
        indicators: ["voz-pasiva"]
    },
    "word-repetition": {
        texto: "The user must enter the user password into the user portal so the user account is verified.",
        indicators: ["word-repetition"]
    },
    "adv": {
        texto: "The background process runs extremely quickly, completely silently, and updates the database continuously.",
        indicators: ["adv"]
    },
    "modal": {
        texto: "The client shall submit the request within ten days, but the client may submit the request next month.",
        indicators: ["modal"]
    },
    "cliches": {
        texto: "At the end of the day, thinking outside the box will result in a win-win situation.",
        indicators: ["cliches"]
    },
    "abstract-words": {
        texto: "The platform must ensure absolute justice, digital freedom, algorithmic truth, and total happiness.",
        indicators: ["abstract-words"]
    },
    "weak-verbs": {
        texto: "The operator will make a decision, have a meeting, and do the necessary work tomorrow.",
        indicators: ["weak-verbs"]
    },
    "impersonal-sentences": {
        texto: "It is believed that the server is operational. It is necessary to restart the background daemon.",
        indicators: ["impersonal-sentences"]
    },
    "negative-phrase": {
        texto: "The administrator cannot not allow unauthorized access to the database.",
        indicators: ["negative-phrase"]
    },
    "opinion-perception": {
        texto: "We feel that the new design seems intuitive and I believe that the team prefers this layout.",
        indicators: ["opinion-perception"]
    },
    "unusual-punctuation": {
        texto: "Is the new deployment ready to go live now?!?! Please verify the production logs..., immediately!!",
        indicators: ["unusual-punctuation"]
    },
    "tenses": {
        texto: "The system processes transactions in real time, but yesterday the cluster crashed unexpectedly and will fail again.",
        indicators: ["tenses"]
    },
    "povshift": {
        texto: "John examined the source code and committed the hotfix. Mary felt a wave of relief as she watched the server recover.",
        indicators: ["povshift"]
    },
    "logical-connectors": {
        texto: "Furthermore, the distributed cache was purged; consequently, overall performance degraded significantly, although memory usage stabilized.",
        indicators: ["logical-connectors"]
    },
    "readability-metric": {
        texto: "The incomprehensibility of multidimensional conceptualizations significantly deteriorates the architectural sustainability and operational reliability of modular infrastructures.",
        indicators: ["readability-metric"]
    }
};

function cargarEjemplo(clave) {
    const ejemplo = EJEMPLOS_PRUEBA[clave];
    if (!ejemplo) return;

    const textarea = document.getElementById("editor-texto");
    if (textarea) {
        textarea.value = ejemplo.texto;
        textarea.dispatchEvent(new Event("input"));
    }

    const checkboxes = document.querySelectorAll('#form-indicadores input[type="checkbox"]');
    if (ejemplo.indicators === "all") {
        checkboxes.forEach(cb => cb.checked = true);
    } else {
        checkboxes.forEach(cb => {
            cb.checked = ejemplo.indicators.includes(cb.id);
        });
    }

    const sel = document.getElementById("select-ejemplos");
    if (sel) sel.value = "";
}

// Exponer funciones al ámbito global
window.mostrarResultado = mostrarResultado;
window.cargarEjemplo = cargarEjemplo;

// Enlazar automáticamente al botón por clase o selector al cargar el DOM
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.querySelector('.btn-analyze') || document.getElementById('btn-analizar');
    if (btn) {
        btn.addEventListener('click', mostrarResultado);
    }
});
