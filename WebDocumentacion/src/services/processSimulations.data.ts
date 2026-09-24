export interface ProcessToken {
  text: string
  tag?: string
  dep?: string
  status?: 'default' | 'active' | 'match' | 'dimmed' | 'warning'
  detail?: string
}

export interface ProcessStep {
  stepNumber: number
  title: string
  badge: string
  description: string
  tokens?: ProcessToken[]
  annotation?: string
  metrics?: { label: string; value: string | number }[]
  resultPreview?: Record<string, any> | Array<any>
}

export interface ServiceSimulation {
  id: string
  sampleText: string
  steps: ProcessStep[]
}

export const serviceSimulations: Record<string, ServiceSimulation> = {
  deteccion_conectores_logicos: {
    id: 'deteccion_conectores_logicos',
    sampleText: 'It rained heavily; therefore, we stayed home.',
    steps: [
      {
        stepNumber: 1,
        title: 'Recepción y Normalización',
        badge: 'ENTRADA',
        description: 'Se recibe el texto y se normaliza en minúsculas preservando la estructura de delimitadores.',
        tokens: [
          { text: 'It', status: 'default' },
          { text: 'rained', status: 'default' },
          { text: 'heavily', status: 'default' },
          { text: ';', status: 'default' },
          { text: 'therefore', status: 'default' },
          { text: ',', status: 'default' },
          { text: 'we', status: 'default' },
          { text: 'stayed', status: 'default' },
          { text: 'home', status: 'default' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Tokenización y Análisis Léxico',
        badge: 'SPACY POS',
        description: 'El pipeline etiqueta morfosintácticamente las palabras e identifica adverbios y conjunciones.',
        tokens: [
          { text: 'It', tag: 'PRON', dep: 'nsubj', status: 'dimmed' },
          { text: 'rained', tag: 'VERB', dep: 'ROOT', status: 'dimmed' },
          { text: 'heavily', tag: 'ADV', dep: 'advmod', status: 'dimmed' },
          { text: 'therefore', tag: 'ADV', dep: 'advmod', status: 'active', detail: 'Conector candidato' },
          { text: 'we', tag: 'PRON', dep: 'nsubj', status: 'dimmed' },
          { text: 'stayed', tag: 'VERB', dep: 'ROOT', status: 'dimmed' },
          { text: 'home', tag: 'NOUN', dep: 'advmod', status: 'dimmed' },
        ],
        annotation: 'Candidato identificado: "therefore" con rol de modificador adverbial conectivo.',
      },
      {
        stepNumber: 3,
        title: 'Clasificación de Conectores',
        badge: 'REGLAS',
        description: 'Se coteja el término con la base taxonómica de conectores lógicos y se asigna su categoría.',
        tokens: [
          { text: 'It rained heavily', status: 'dimmed' },
          { text: 'therefore', tag: 'CONCLUSION', status: 'match', detail: 'Tipo: conclusion' },
          { text: 'we stayed home', status: 'dimmed' },
        ],
        annotation: 'Conector de relación causal/conclusiva confirmado.',
      },
      {
        stepNumber: 4,
        title: 'Generación de Respuesta',
        badge: 'JSON SALIDA',
        description: 'Se consolida el conteo total, conectores clasificados y palabras no conectivas.',
        resultPreview: {
          original_text: 'It rained heavily; therefore, we stayed home.',
          connectors_found: [{ connector: 'therefore', type: 'conclusion' }],
          total: 1,
        },
      },
    ],
  },

  weak_verbs: {
    id: 'weak_verbs',
    sampleText: 'She made a decision to have lunch and do the work.',
    steps: [
      {
        stepNumber: 1,
        title: 'Texto de Entrada',
        badge: 'INPUT',
        description: 'Se ingresa la oración para detectar verbos débiles (make, do, have, get, etc.).',
        tokens: [
          { text: 'She', status: 'default' },
          { text: 'made', status: 'default' },
          { text: 'a', status: 'default' },
          { text: 'decision', status: 'default' },
          { text: 'to', status: 'default' },
          { text: 'have', status: 'default' },
          { text: 'lunch', status: 'default' },
          { text: 'and', status: 'default' },
          { text: 'do', status: 'default' },
          { text: 'the', status: 'default' },
          { text: 'work', status: 'default' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Extracción y Lematización',
        badge: 'LEMATIZADOR',
        description: 'Se filtran todos los verbos y se extrae su lema base.',
        tokens: [
          { text: 'She', status: 'dimmed' },
          { text: 'made', tag: 'VERB (make)', status: 'active' },
          { text: 'a decision to', status: 'dimmed' },
          { text: 'have', tag: 'VERB (have)', status: 'active' },
          { text: 'lunch and', status: 'dimmed' },
          { text: 'do', tag: 'VERB (do)', status: 'active' },
          { text: 'the work', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 3,
        title: 'Detección de Verbos Débiles',
        badge: 'FILTRADO',
        description: 'Se comparan los lemas contra la lista de verbos con baja carga semántica.',
        tokens: [
          { text: 'made', tag: 'DÉBIL → decide', status: 'warning', detail: 'make a decision' },
          { text: 'have', tag: 'DÉBIL → eat', status: 'warning', detail: 'have lunch' },
          { text: 'do', tag: 'DÉBIL → execute/complete', status: 'warning', detail: 'do the work' },
        ],
        annotation: '3 verbos débiles detectados con sugerencias de verbos de acción directa.',
      },
      {
        stepNumber: 4,
        title: 'Resultado Estructurado',
        badge: 'RESPUESTA',
        description: 'Se devuelven las ubicaciones y los verbos detectados.',
        resultPreview: {
          weak_verbs: ['made', 'have', 'do'],
          total: 3,
          suggestions: {
            made: 'decided',
            have: 'eaten',
            do: 'completed',
          },
        },
      },
    ],
  },

  abstract_words: {
    id: 'abstract_words',
    sampleText: 'Love and freedom are important concepts in philosophy.',
    steps: [
      {
        stepNumber: 1,
        title: 'Tokenización y Filtrado de Stopwords',
        badge: 'TOKENIZACIÓN',
        description: 'Se eliminan tokens puramente funcionales (and, are, in) para aislar palabras con significado léxico.',
        tokens: [
          { text: 'Love', tag: 'NOUN', status: 'active' },
          { text: 'and', tag: 'STOPWORD', status: 'dimmed' },
          { text: 'freedom', tag: 'NOUN', status: 'active' },
          { text: 'are', tag: 'STOPWORD', status: 'dimmed' },
          { text: 'important', tag: 'ADJ', status: 'active' },
          { text: 'concepts', tag: 'NOUN', status: 'active' },
          { text: 'in', tag: 'STOPWORD', status: 'dimmed' },
          { text: 'philosophy', tag: 'NOUN', status: 'active' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Inferencia de Embeddings FastText',
        badge: 'EMBEDDINGS',
        description: 'Se vectoriza cada palabra con el modelo de representación semántica.',
        tokens: [
          { text: 'Love', detail: 'vec[300]', status: 'active' },
          { text: 'freedom', detail: 'vec[300]', status: 'active' },
          { text: 'important', detail: 'vec[300]', status: 'active' },
          { text: 'concepts', detail: 'vec[300]', status: 'active' },
          { text: 'philosophy', detail: 'vec[300]', status: 'active' },
        ],
      },
      {
        stepNumber: 3,
        title: 'Predicción XGBoost y Abstracción',
        badge: 'XGBOOST ML',
        description: 'El regresor estima la concreción y calcula abstractness = 6 - concreteness (umbral >= 3.0).',
        tokens: [
          { text: 'Love', tag: 'Abstr: 4.8', status: 'match' },
          { text: 'freedom', tag: 'Abstr: 4.6', status: 'match' },
          { text: 'important', tag: 'Abstr: 3.9', status: 'match' },
          { text: 'concepts', tag: 'Abstr: 4.2', status: 'match' },
          { text: 'philosophy', tag: 'Abstr: 4.5', status: 'match' },
        ],
        annotation: 'Todos los términos superan el umbral de abstracción de 3.0.',
      },
      {
        stepNumber: 4,
        title: 'Resultado Final',
        badge: 'JSON SALIDA',
        description: 'Lista de palabras abstractas sin duplicados.',
        resultPreview: {
          results: ['love', 'freedom', 'important', 'concepts', 'philosophy'],
        },
      },
    ],
  },

  voz_pasiva: {
    id: 'voz_pasiva',
    sampleText: 'The letter was written by Juan yesterday.',
    steps: [
      {
        stepNumber: 1,
        title: 'Análisis Sintáctico spaCy',
        badge: 'DEPENDENCIAS',
        description: 'Se procesa la oración y se identifican las relaciones de dependencia gramatical.',
        tokens: [
          { text: 'The', tag: 'DET', dep: 'det', status: 'dimmed' },
          { text: 'letter', tag: 'NOUN', dep: 'nsubjpass', status: 'active', detail: 'Sujeto paciente' },
          { text: 'was', tag: 'AUX', dep: 'auxpass', status: 'active', detail: 'Auxiliar pasivo' },
          { text: 'written', tag: 'VERB', dep: 'ROOT (VBN)', status: 'active', detail: 'Participio' },
          { text: 'by', tag: 'ADP', dep: 'agent', status: 'dimmed' },
          { text: 'Juan', tag: 'PROPN', dep: 'pobj', status: 'dimmed', detail: 'Agente ejecutor' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Detección de Patrón Pasivo',
        badge: 'PATRÓN AUXPASS',
        description: 'Se valida la presencia de dependencia auxpass conectada a verbo en participio pasado (VBN).',
        tokens: [
          { text: 'The letter', status: 'dimmed' },
          { text: 'was written', tag: 'VOZ PASIVA', status: 'match', detail: 'Rango [11, 22]' },
          { text: 'by Juan yesterday', status: 'dimmed' },
        ],
        annotation: 'Construcción pasiva confirmada: "was written". Sujeto "letter" recibe la acción.',
      },
      {
        stepNumber: 3,
        title: 'Cálculo de Coordenadas de Texto',
        badge: 'SPANS',
        description: 'Se calculan las posiciones de inicio y fin en caracteres para resaltado.',
        metrics: [
          { label: 'Es Pasiva', value: 'True' },
          { label: 'Inicio', value: '11' },
          { label: 'Fin', value: '22' },
          { label: 'Construcción', value: 'was written' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta de la API',
        badge: 'RESPUESTA',
        description: 'Objeto de respuesta con indicador booleano y lista de posiciones.',
        resultPreview: {
          is_passive: true,
          positions: [[11, 22]],
        },
      },
    ],
  },

  'oraciones-impersonales': {
    id: 'oraciones-impersonales',
    sampleText: 'It is necessary to review the system logs.',
    steps: [
      {
        stepNumber: 1,
        title: 'Análisis Estructural',
        badge: 'ESTRUCTURA',
        description: 'Detección de sujeto ficticio o pronombre expletivo ("dummy it").',
        tokens: [
          { text: 'It', tag: 'PRON', dep: 'nsubj', status: 'active', detail: 'Pronombre expletivo' },
          { text: 'is', tag: 'AUX', dep: 'ROOT', status: 'dimmed' },
          { text: 'necessary', tag: 'ADJ', dep: 'acomp', status: 'active', detail: 'Adjetivo evaluativo' },
          { text: 'to review', tag: 'VERB', dep: 'xcomp', status: 'dimmed' },
          { text: 'the system logs', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Evaluación de Agente Referencial',
        badge: 'SEMÁNTICA',
        description: 'Se constata la ausencia de un agente humano o entidad ejecutor directo.',
        tokens: [
          { text: 'It is necessary to review...', tag: 'IMPERSONAL', status: 'warning', detail: 'Sin agente explícito' },
        ],
        annotation: 'Construcción impersonal identificada: la acción carece de sujeto responsable definido.',
      },
      {
        stepNumber: 3,
        title: 'Clasificación de Oración',
        badge: 'CLASIFICADOR',
        description: 'Asignación de categoría entre personal, impersonal o ambigua con grado de certeza.',
        metrics: [
          { label: 'Tipo', value: 'Impersonal' },
          { label: 'Certeza', value: '96%' },
          { label: 'Estructura', value: 'It-Cleft / Evaluative' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta Final',
        badge: 'JSON SALIDA',
        description: 'Clasificación y análisis de la oración.',
        resultPreview: {
          sentence: 'It is necessary to review the system logs.',
          category: 'impersonal',
          confidence: 0.96,
        },
      },
    ],
  },

  'servicio-repeticion-palabras': {
    id: 'servicio-repeticion-palabras',
    sampleText: 'The user requested the file and the user downloaded it.',
    steps: [
      {
        stepNumber: 1,
        title: 'Filtrado y Lematización',
        badge: 'LEMATIZACIÓN',
        description: 'Se eliminan stopwords y se agrupan palabras por su forma lematizada.',
        tokens: [
          { text: 'user', tag: 'LEMMA: user', status: 'active' },
          { text: 'requested', tag: 'LEMMA: request', status: 'dimmed' },
          { text: 'file', tag: 'LEMMA: file', status: 'dimmed' },
          { text: 'user', tag: 'LEMMA: user', status: 'active' },
          { text: 'downloaded', tag: 'LEMMA: download', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Cálculo de Frecuencia y Proximidad',
        badge: 'CONTEO',
        description: 'Se calcula la densidad de aparición en la misma ventana de texto.',
        metrics: [
          { label: 'Término', value: 'user' },
          { label: 'Apariciones', value: '2' },
          { label: 'Distancia', value: '6 tokens' },
        ],
        annotation: 'Alerta: palabra "user" reiterada a corta distancia.',
      },
      {
        stepNumber: 3,
        title: 'Mapeo de Posiciones',
        badge: 'SPANS',
        description: 'Se ubican los rangos de caracteres de cada ocurrencia en el texto original.',
        tokens: [
          { text: 'The', status: 'dimmed' },
          { text: 'user', status: 'match', detail: '[4, 8]' },
          { text: 'requested the file and the', status: 'dimmed' },
          { text: 'user', status: 'match', detail: '[36, 40]' },
          { text: 'downloaded it.', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Resultado Estructurado',
        badge: 'RESPUESTA',
        description: 'Diccionario con palabras repetidas y sus coordenadas.',
        resultPreview: {
          repeated_words: [
            {
              word: 'user',
              count: 2,
              positions: [[4, 8], [36, 40]],
            },
          ],
        },
      },
    ],
  },

  verbos_percepcion_opinion: {
    id: 'verbos_percepcion_opinion',
    sampleText: 'I think that they noticed the sudden alteration in the database.',
    steps: [
      {
        stepNumber: 1,
        title: 'Extracción de Verbos y Dependencias',
        badge: 'POS TAGGING',
        description: 'Se extraen los predicados verbales de la oración principal y subordinada.',
        tokens: [
          { text: 'I', status: 'dimmed' },
          { text: 'think', tag: 'VERB (ROOT)', status: 'active', detail: 'Verbo de opinión' },
          { text: 'that they', status: 'dimmed' },
          { text: 'noticed', tag: 'VERB (ccomp)', status: 'active', detail: 'Verbo de percepción' },
          { text: 'the alteration...', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Clasificación Léxico-Semántica',
        badge: 'TAXONOMÍA',
        description: 'Se mapean los verbos con las categorías de opinión/creencia y percepción sensorial.',
        tokens: [
          { text: 'think', tag: 'OPINIÓN / JUICIO', status: 'match', detail: 'Pensamiento subjetivo' },
          { text: 'noticed', tag: 'PERCEPCIÓN', status: 'match', detail: 'Observación sensorial' },
        ],
        annotation: 'Dos verbos con carga epistémica y sensorial detectados.',
      },
      {
        stepNumber: 3,
        title: 'Análisis de Subjetividad',
        badge: 'ANÁLISIS',
        description: 'La presencia de estos verbos indica enunciados de juicio subjetivo en vez de hechos fácticos.',
        metrics: [
          { label: 'Opinión', value: 'think' },
          { label: 'Percepción', value: 'noticed' },
          { label: 'Subjetividad', value: 'Alta' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta de la API',
        badge: 'JSON SALIDA',
        description: 'Lista de verbos clasificados por categoría.',
        resultPreview: {
          opinion_verbs: [{ verb: 'think', position: [2, 7] }],
          perception_verbs: [{ verb: 'noticed', position: [18, 25] }],
        },
      },
    ],
  },

  'metricas-de-legibilidad': {
    id: 'metricas-de-legibilidad',
    sampleText: 'The multi-layered architectural configuration facilitates algorithmic optimization.',
    steps: [
      {
        stepNumber: 1,
        title: 'Conteo y Métricas de Superficie',
        badge: 'MÉTRICAS BASE',
        description: 'Se cuentan oraciones, palabras totales y caracteres del texto.',
        metrics: [
          { label: 'Oraciones', value: '1' },
          { label: 'Palabras', value: '8' },
          { label: 'Caracteres', value: '83' },
          { label: 'Longitud Media', value: '10.3 car/palabra' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Conteo Silábico y Palabras Complejas',
        badge: 'SÍLABAS',
        description: 'Se identifican palabras polisilábicas (3 o más sílabas) excluyendo sufijos comunes.',
        tokens: [
          { text: 'multi-layered', tag: '4 sílabas', status: 'warning' },
          { text: 'architectural', tag: '5 sílabas', status: 'warning' },
          { text: 'configuration', tag: '5 sílabas', status: 'warning' },
          { text: 'facilitates', tag: '4 sílabas', status: 'warning' },
          { text: 'algorithmic', tag: '4 sílabas', status: 'warning' },
          { text: 'optimization', tag: '5 sílabas', status: 'warning' },
        ],
        annotation: '75% de las palabras del texto son complejas/polisilábicas.',
      },
      {
        stepNumber: 3,
        title: 'Cálculo de Fórmulas de Legibilidad',
        badge: 'FÓRMULAS',
        description: 'Se calculan índices Gunning Fog, Flesch Reading Ease y Coleman-Liau.',
        metrics: [
          { label: 'Gunning Fog', value: '33.2 (Muy Difícil)' },
          { label: 'Flesch Ease', value: '8.4 (Postgrado)' },
          { label: 'Nivel Escolar', value: 'Especialista' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Reporte Consolidado',
        badge: 'REPORTE',
        description: 'Resumen completo de índices de legibilidad.',
        resultPreview: {
          word_count: 8,
          complex_words: 6,
          gunning_fog: 33.2,
          flesch_reading_ease: 8.4,
          reading_level: 'Very Difficult (Academic/Technical)',
        },
      },
    ],
  },

  'servicio-deteccion-cliches': {
    id: 'servicio-deteccion-cliches',
    sampleText: 'At the end of the day, we must think outside the box.',
    steps: [
      {
        stepNumber: 1,
        title: 'Extracción de N-Gramas',
        badge: 'N-GRAMAS',
        description: 'Se segmenta el texto en secuencias de 3 a 6 palabras continuas.',
        tokens: [
          { text: 'At the end of the day', status: 'active', detail: 'N-grama 1' },
          { text: ', we must', status: 'dimmed' },
          { text: 'think outside the box', status: 'active', detail: 'N-grama 2' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Comparación Léxica y SBERT',
        badge: 'SBERT MODEL',
        description: 'Se compara contra base de clichés con cálculo de similitud semántica por cosenos.',
        tokens: [
          { text: 'At the end of the day', tag: 'CLICHÉ (100%)', status: 'match' },
          { text: 'think outside the box', tag: 'CLICHÉ (98%)', status: 'match' },
        ],
        annotation: 'Dos expresiones trilladas detectadas con alta similitud.',
      },
      {
        stepNumber: 3,
        title: 'Generación de Sugerencias',
        badge: 'REEMPLAZOS',
        description: 'El servicio propone alternativas directas y concisas.',
        metrics: [
          { label: 'At the end of the day', value: 'Ultimately / In conclusion' },
          { label: 'Think outside the box', value: 'Innovate / Think creatively' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Resultado de la API',
        badge: 'SALIDA JSON',
        description: 'Lista de clichés detectados y sus métricas.',
        resultPreview: {
          cliches_detected: [
            { text: 'at the end of the day', confidence: 1.0, suggestion: 'ultimately' },
            { text: 'think outside the box', confidence: 0.98, suggestion: 'be creative' },
          ],
        },
      },
    ],
  },

  detector_adverbios: {
    id: 'detector_adverbios',
    sampleText: 'The team quickly reviewed the completely new guidelines yesterday.',
    steps: [
      {
        stepNumber: 1,
        title: 'Análisis Morfosintáctico con Transformer',
        badge: 'SPACY TRF',
        description: 'El modelo basado en RoBERTa identifica todos los adverbios sintácticos (ADV).',
        tokens: [
          { text: 'The team', status: 'dimmed' },
          { text: 'quickly', tag: 'ADV (advmod)', status: 'active' },
          { text: 'reviewed the', status: 'dimmed' },
          { text: 'completely', tag: 'ADV (advmod)', status: 'active' },
          { text: 'new guidelines', status: 'dimmed' },
          { text: 'yesterday', tag: 'ADV (advmod)', status: 'active' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Clasificación Semántica de Adverbios',
        badge: 'CATEGORIZACIÓN',
        description: 'Se agrupan los adverbios según expresen modo, grado, tiempo o frecuencia.',
        tokens: [
          { text: 'quickly', tag: 'MODO', status: 'match', detail: 'Cómo se realiza' },
          { text: 'completely', tag: 'GRADO', status: 'match', detail: 'Intensidad' },
          { text: 'yesterday', tag: 'TIEMPO', status: 'match', detail: 'Cuándo ocurrió' },
        ],
        annotation: '3 adverbios clasificados en 3 categorías diferentes.',
      },
      {
        stepNumber: 3,
        title: 'Cálculo de Densidad Adverbial',
        badge: 'DENSIDAD',
        description: 'Se calcula la proporción de adverbios respecto al total de palabras.',
        metrics: [
          { label: 'Total Palabras', value: '8' },
          { label: 'Adverbios', value: '3' },
          { label: 'Densidad', value: '37.5% (Elevada)' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta de la API',
        badge: 'JSON SALIDA',
        description: 'Desglose detallado de los adverbios encontrados.',
        resultPreview: {
          adverbs: [
            { word: 'quickly', category: 'manner' },
            { word: 'completely', category: 'degree' },
            { word: 'yesterday', category: 'time' },
          ],
          total: 3,
        },
      },
    ],
  },

  detector_doble_negacion: {
    id: 'detector_doble_negacion',
    sampleText: "The developer didn't say nothing about the server failure.",
    steps: [
      {
        stepNumber: 1,
        title: 'Localización de Partículas Negativas',
        badge: 'NEG DETECT',
        description: 'Se identifican partículas adverbiales de negación (not, n\'t) y palabras negativas (no, nothing, never).',
        tokens: [
          { text: 'The developer', status: 'dimmed' },
          { text: "didn't", tag: "PART: n't (neg)", status: 'active', detail: 'Negación 1' },
          { text: 'say', status: 'dimmed' },
          { text: 'nothing', tag: 'PRON: neg', status: 'active', detail: 'Negación 2' },
          { text: 'about the failure.', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Análisis de Ámbito Oracional (Scope)',
        badge: 'ÁMBITO CLÁUSULA',
        description: 'Se evalúa si ambas negaciones afectan al mismo predicado verbal ("didn\'t say nothing").',
        tokens: [
          { text: "didn't say nothing", tag: 'DOBLE NEGACIÓN', status: 'warning', detail: 'Mismo predicado' },
        ],
        annotation: 'Alerta: conflicto de doble negación informal en una misma cláusula.',
      },
      {
        stepNumber: 3,
        title: 'Generación de Corrección Gramatical',
        badge: 'CORRECCIÓN',
        description: 'Se propone la transformación formal a polaridad estándar afirmativa/negativa única.',
        metrics: [
          { label: 'Expresión Original', value: "didn't say nothing" },
          { label: 'Opción 1', value: "didn't say anything" },
          { label: 'Opción 2', value: 'said nothing' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta de la API',
        badge: 'RESPUESTA',
        description: 'Reporte de la doble negación con posiciones de caracteres.',
        resultPreview: {
          double_negation: true,
          elements: ["didn't", 'nothing'],
          positions: [[14, 21], [26, 33]],
        },
      },
    ],
  },

  deteccion_verbos_modales: {
    id: 'deteccion_verbos_modales',
    sampleText: 'You can submit the report today, but you must submit the report before Friday.',
    steps: [
      {
        stepNumber: 1,
        title: 'Detección de Cláusulas y Modales',
        badge: 'MODAL DETECT',
        description: 'Se extraen los verbos modales auxiliares y sus acciones dependientes.',
        tokens: [
          { text: 'You', status: 'dimmed' },
          { text: 'can', tag: 'MODAL: permiso', status: 'active' },
          { text: 'submit the report', tag: 'ACCIÓN 1', status: 'match' },
          { text: 'today, but you', status: 'dimmed' },
          { text: 'must', tag: 'MODAL: obligación', status: 'active' },
          { text: 'submit the report', tag: 'ACCIÓN 2', status: 'match' },
          { text: 'before Friday.', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Comparación de Acciones Compartidas',
        badge: 'COINCIDENCIA',
        description: 'Se calculan las palabras clave compartidas entre ambas acciones ("submit", "report").',
        metrics: [
          { label: 'Acción 1', value: 'submit the report' },
          { label: 'Acción 2', value: 'submit the report' },
          { label: 'Similitud', value: '100% de coincidencia léxica' },
        ],
      },
      {
        stepNumber: 3,
        title: 'Detección de Inconsistencia Categorial',
        badge: 'INCONSISTENCIA',
        description: 'Se detecta contradicción entre categoría "posibilidad/permiso" (can) y "obligación" (must).',
        tokens: [
          { text: 'can (permiso)', status: 'warning' },
          { text: '≠', status: 'default' },
          { text: 'must (obligación estricta)', status: 'warning' },
        ],
        annotation: 'Inconsistencia identificada: una misma acción se presenta simultáneamente como optativa y obligatoria.',
      },
      {
        stepNumber: 4,
        title: 'Resultado Estructurado',
        badge: 'JSON SALIDA',
        description: 'Par modal inconsistente devuelto por el servicio.',
        resultPreview: {
          inconsistencies: [
            {
              shared_action: 'submit report',
              case_1: { modal: 'can', category: 'posibilidad/permiso', action: 'submit the report' },
              case_2: { modal: 'must', category: 'obligacion', action: 'submit the report' },
            },
          ],
        },
      },
    ],
  },

  deteccion_puntuacion_inusual: {
    id: 'deteccion_puntuacion_inusual',
    sampleText: 'Hi!.., are you ready (for the demo ?',
    steps: [
      {
        stepNumber: 1,
        title: 'Escaneo de Caracteres y Signos',
        badge: 'ESCANEO',
        description: 'Se analiza la cadena carácter a carácter identificando signos de puntuación.',
        tokens: [
          { text: 'Hi', status: 'dimmed' },
          { text: '!', tag: 'SIGNO', status: 'active' },
          { text: '..', tag: 'SIGNO', status: 'active' },
          { text: ',', tag: 'SIGNO', status: 'active' },
          { text: 'are you ready', status: 'dimmed' },
          { text: '(', tag: 'DELIMITADOR', status: 'active' },
          { text: 'for the demo', status: 'dimmed' },
          { text: '?', tag: 'SIGNO', status: 'active' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Evaluación de Reglas de Puntuación',
        badge: 'REGLAS',
        description: 'Se aplican las reglas: signos consecutivos prohibidos y delimitadores desbalanceados.',
        tokens: [
          { text: '!..,', tag: 'SECUENCIA INVÁLIDA', status: 'warning', detail: 'Signos pegados no permitidos' },
          { text: '(', tag: 'DESBALANCEADO', status: 'warning', detail: 'Paréntesis sin cerrar' },
        ],
        annotation: 'Dos irregularidades detectadas: secuencia "!..," y paréntesis "(" desbalanceado.',
      },
      {
        stepNumber: 3,
        title: 'Consolidación de Posiciones',
        badge: 'COORDENADAS',
        description: 'Se extraen los signos problemáticos para reportar al usuario.',
        metrics: [
          { label: 'Signos Consecutivos', value: '!, .' },
          { label: 'Delimitadores Abiertos', value: '(' },
          { label: 'Puntuación Inusual', value: 'True' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta de la API',
        badge: 'SALIDA JSON',
        description: 'Respuesta con booleano y caracteres detectados.',
        resultPreview: {
          unusual_punctuation: true,
          positions: ['!', ',', '('],
        },
      },
    ],
  },

  povshift: {
    id: 'povshift',
    sampleText: 'John wondered where Mary was. Mary knew he was waiting.',
    steps: [
      {
        stepNumber: 1,
        title: 'Segmentación y Extracción de Cláusulas',
        badge: 'ORACIONES',
        description: 'Se divide el texto en oraciones y se identifican sujetos y núcleos verbales.',
        tokens: [
          { text: '[Oración 1]', status: 'dimmed' },
          { text: 'John', tag: 'SUJETO (PROPN)', status: 'active' },
          { text: 'wondered', tag: 'VERBO (ROOT)', status: 'active' },
          { text: 'where Mary was.', status: 'dimmed' },
          { text: '[Oración 2]', status: 'dimmed' },
          { text: 'Mary', tag: 'SUJETO (PROPN)', status: 'active' },
          { text: 'knew', tag: 'VERBO (ROOT)', status: 'active' },
          { text: 'he was waiting.', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Detección de Estados Internos',
        badge: 'ESTADOS INTERNOS',
        description: 'Se clasifican verbos cognitivos, emocionales y perceptivos que revelan pensamientos privados.',
        tokens: [
          { text: 'John wondered', tag: 'COG: Interioridad en John', status: 'match' },
          { text: 'Mary knew', tag: 'COG: Interioridad en Mary', status: 'match' },
        ],
        annotation: 'Ambas oraciones penetran en la mente subjetiva de personajes distintos.',
      },
      {
        stepNumber: 3,
        title: 'Seguimiento del Foco y POV Shift',
        badge: 'POV SHIFT',
        description: 'Se detecta salto de focalización narrativa interna entre oraciones contiguas.',
        tokens: [
          { text: 'John (Foco 1)', status: 'warning' },
          { text: '➔ Salto Injustificado ➔', status: 'default' },
          { text: 'Mary (Foco 2)', status: 'warning' },
        ],
        metrics: [
          { label: 'Origen', value: 'John (oración 0)' },
          { label: 'Destino', value: 'Mary (oración 1)' },
          { label: 'Confianza', value: '0.85' },
        ],
      },
      {
        stepNumber: 4,
        title: 'Respuesta de la API',
        badge: 'JSON SALIDA',
        description: 'Objeto de salto de perspectiva detectado.',
        resultPreview: [
          {
            from_character: { id: 1, canonical_name: 'John', mentions: ['John'] },
            to_character: { id: 7, canonical_name: 'Mary', mentions: ['Mary'] },
            sentence_index: 1,
            confidence: 0.85,
            evidence: ['previous focus on John', 'new focalization on Mary'],
          },
        ],
      },
    ],
  },

  verb_tense_inconsistencies: {
    id: 'verb_tense_inconsistencies',
    sampleText: 'The system received the request and processes the payment.',
    steps: [
      {
        stepNumber: 1,
        title: 'Identificación de Sintagmas Verbales',
        badge: 'TAGS VERBALES',
        description: 'Se etiquetan los verbos y sus tiempos mediante análisis morfológico de spaCy.',
        tokens: [
          { text: 'The system', status: 'dimmed' },
          { text: 'received', tag: 'VERB (VBD) · Pasado', status: 'active' },
          { text: 'the request and', status: 'dimmed' },
          { text: 'processes', tag: 'VERB (VBZ) · Presente', status: 'active' },
          { text: 'the payment.', status: 'dimmed' },
        ],
      },
      {
        stepNumber: 2,
        title: 'Asignación a Familias Temporales',
        badge: 'FAMILIAS',
        description: 'Se agrupan los verbos en categorías temporales canónicas.',
        metrics: [
          { label: 'received', value: 'Familia PAST' },
          { label: 'processes', value: 'Familia PRES' },
          { label: 'Conexión', value: 'Coordinación directa ("and")' },
        ],
      },
      {
        stepNumber: 3,
        title: 'Ejecución de Regla TenseMismatchRule',
        badge: 'EVALUACIÓN REGLAS',
        description: 'Se detecta la alternancia discordante entre pasado y presente sin justificación contextual.',
        tokens: [
          { text: 'received (past)', status: 'warning' },
          { text: '≠', status: 'default' },
          { text: 'processes (present)', status: 'warning' },
        ],
        annotation: 'Inconsistencia temporal detectada: coexistencia de tiempos pasado y presente en predicados coordinados.',
      },
      {
        stepNumber: 4,
        title: 'Generación de Incidencias',
        badge: 'RESPUESTA',
        description: 'Respuesta con la lista de problemas, código de error y posición.',
        resultPreview: {
          normalized_text: 'The system received the request and processes the payment.',
          issues: [
            {
              fragment: 'processes, received',
              position: 11,
              explanation: 'The sentence contains both present and past verb tenses.',
              error_code: 'TENSE_MISMATCH',
            },
          ],
        },
      },
    ],
  },
}
