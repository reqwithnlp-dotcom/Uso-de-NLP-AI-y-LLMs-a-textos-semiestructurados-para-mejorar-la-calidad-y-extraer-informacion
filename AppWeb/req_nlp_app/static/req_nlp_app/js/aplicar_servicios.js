async function mostrarResultado() {
    const textarea = document.getElementById("editor-texto");
    const texto = textarea.value;
    //const invertir = document.getElementById("invertir-texto").checked;
    invertir=false;
    const voz_pasiva = document.getElementById("voz-pasiva").checked;
    const word_repetition = document.getElementById("word-repetition").checked;
    const impersonal_sentences = document.getElementById("impersonal-sentences").checked;
    const negative_phrases = document.getElementById("negative-phrase").checked;
    const opinion_perception = document.getElementById("opinion-perception").checked;
    const unusual_punctuation = document.getElementById("unusual-punctuation").checked;
    const abstract_words = document.getElementById("abstract-words").checked;
    const logical_connectors = document.getElementById("logical-connectors").checked;
    const readability_metric = document.getElementById("readability-metric").checked;
    const tenses = document.getElementById("tenses").checked;
    const cliches = document.getElementById("cliches").checked;


    const resultados = [];
    const promesas = [];

    if (invertir) {
        const url_invertir_texto = `${API_INVERTIR_TEXTO_URL}/invertir_texto/?texto=${encodeURIComponent(texto)}`;
        const p = fetch(url_invertir_texto)
            .then(response => response.json())
            .then(data => resultados.push("Texto Invertido: " + data.respuesta))
            .catch(error => resultados.push("Error al invertir: " + error));
        promesas.push(p);
    }

    if (voz_pasiva) {
        const p = fetch(`${API_VOZ_PASIVA_URL}/convertir`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => resultados.push("Voz activa: " + data.activa))
        .catch(err => resultados.push("Error en voz pasiva: " + err));
        promesas.push(p);
    }
    if (word_repetition) {
        const p = fetch(`${API_WORD_REPETITION_URL}/repeticiones`,     {
            method: "POST",
            headers: {"Content-Type": "application/json" },
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
            resultados.push("Repeticiones: " + repeticiones);
        })
        .catch(err => resultados.push("Repeticiones: " + err));
        promesas.push(p);
    }
    if (impersonal_sentences) {
        const p = fetch(`${API_IMPERSONAL_SENTENCES_URL}/detectar`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => {
            resultados.push("Impersonal Sentences: " + data.motivo);
        })
        .catch(err => resultados.push("Impersonal Sentences: " + err));
        promesas.push(p);
    }

    if (negative_phrases){
        const p = fetch(`${API_NEGATIVE_PHRASE_URL}/negativaCompleja`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ texto: texto })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta del backend:", data);
            const resultado = data[0]; 
            resultados.push("Frase negativa: " + (resultado ? "Sí" : "No"));
            
        })
        .catch(err => resultados.push("Error en detección de frases negativas: " + err));
        promesas.push(p);
    }
    if (opinion_perception){
        const p = fetch(`${API_OPINION_PERCEPTION_URL}/opinion-percepcion?texto=${encodeURIComponent(texto)}`, {
            method: "GET",
            headers: {"Content-Type": "application/json"}
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta del opinion perception:", data);
            if (data.resultado.length > 0) {
                data.resultado.forEach(item => {
                    resultados.push(
                    `Frase detectada -> Verbo: ${item.verbo}, Tipo: ${item.tipo}, Lema: ${item.lema}`
                    );
                });
            } else {
                console.log("No se detectaron verbos de opinión o percepción.");
            }
        })
        .catch(err => {
            console.error("Error en fetch:", err);
        });
        promesas.push(p);
    }

    if (unusual_punctuation){
        const p = fetch(`${API_UNUSUAL_PUNCTUATION_URL}/detectar-puntuacion`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sentence: texto })
        })
        .then(response => response.json())
        .then(data => {
            console.log("Respuesta del backend:", data);
            if (Array.isArray(data) && data.length > 0) {
                data.forEach(error => {
                    const posiciones = Array.isArray(error.posición) ? error.posición.join("-") : "N/A";
                    resultados.push(`Error: ${error.descripción}, Texto: "${error.texto}", Posición: ${posiciones}`);
                });
            } else {
                resultados.push("No se detectaron errores de puntuación.");
            }
        })
        .catch(err => {
            console.error("Error al analizar puntuación:", err);
            resultados.push("Error en el análisis de puntuación: " + err);
        });
        promesas.push(p);
    }
    if (abstract_words){
        const params = new URLSearchParams({ texto: texto });
        const p = fetch(`${API_ABSTRACT_WORDS_URL}/abstractas/?${params.toString()}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (data.respuesta && Array.isArray(data.respuesta)) {
                resultados.push("Palabras abstractas: " + data.respuesta.join(", "));
            } else {
                resultados.push("Error en palabras abstractas: no se recibieron resultados");
                console.log("Respuesta del backend:", data);
            }
        })
        .catch(err => resultados.push("Error en palabras abstractas: " + err));
        promesas.push(p);
    }
    
    if (logical_connectors){
        const p = fetch(`${API_LOGICAL_CONNECTORS_URL}/conectores-logicos/?texto=${encodeURIComponent(texto)}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data.conectores) && data.conectores.length > 0) {
                resultados.push("Conectores lógicos encontrados: " + data.conectores.join(", "));
            } else {
                resultados.push("No se encontraron conectores lógicos.");
            }
        })
        .catch(err => resultados.push("Error al detectar conectores lógicos: " + err));
        
        promesas.push(p);
    }


    if (readability_metric){
        const p = fetch(`${API_READABILITY_METRIC_URL}/metrica-legibilidad/?texto=${encodeURIComponent(texto)}`, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        })
        .then(response => response.json())
        .then(data => {
            resultados.push(
                `Legibilidad -> Puntaje: ${data["Puntaje"].toFixed(2)}, Nivel: ${data["Nivel de legibilidad"]}`
            );
        })
        .catch(err => resultados.push("Error al calcular legibilidad: " + err));
        
        promesas.push(p);
    }
    if (tenses){
        const p = fetch(`${API_TENSES_URL}/deteccion_de_verbos/?texto=${encodeURIComponent(texto)}`)
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data) && data.length > 0) {
                const resultadosTiempos = data.map(([verbo, tiempo]) => `${verbo}: ${tiempo}`).join("; ");
                resultados.push(`Tiempos verbales detectados -> ${resultadosTiempos}`);
            } else {
                resultados.push("No se detectaron tiempos verbales.");
            }
        })
        .catch(err => resultados.push("Error al detectar tiempos verbales: " + err));
        
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
                resultados.push("Clichés detectados: " + data.cliches_encontrados.join(", "));
            } else {
                resultados.push("No se detectaron clichés en el texto.");
            }
        })
        .catch(err => resultados.push("Error al detectar clichés: " + err));

        promesas.push(p);
    }


    if (promesas.length === 0) {
        resultados.push("No se seleccionó ninguna opción.");
    }

    await Promise.all(promesas);
    document.getElementById("resultados").innerText = resultados.join("\n");
}