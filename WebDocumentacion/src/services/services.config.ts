export interface ServiceConfig {
  id: string
  name: string
  shortDescription: string
  markdownPath: string
}

export const services: ServiceConfig[] = [
  {
    id: 'deteccion_conectores_logicos',
    name: 'API Detección de Conectores Lógicos',
    shortDescription: 'Detecta y clasifica conectores lógicos en textos en inglés.',
    markdownPath: '/content/deteccion_conectores_logicos/README.md',
  },
  {
    id: 'weak_verbs',
    name: 'API Detección de Verbos Débiles',
    shortDescription: 'Identifica verbos débiles en textos en inglés.',
    markdownPath: '/content/weak_verbs/README.md',
  },
  {
    id: 'abstract_words',
    name: 'API Detección de Palabras Abstractas',
    shortDescription: 'Detecta palabras con un nivel alto de abstracción.',
    markdownPath: '/content/abstract_words/README.md',
  },
  {
    id: 'voz_pasiva',
    name: 'API Detección de Voz Pasiva',
    shortDescription: 'Identifica construcciones pasivas en oraciones en inglés.',
    markdownPath: '/content/voz_pasiva/README.md',
  },
  {
    id: 'oraciones-impersonales',
    name: 'API Detección de Oraciones Impersonales',
    shortDescription: 'Clasifica oraciones en inglés como personales, impersonales o ambiguas.',
    markdownPath: '/content/oraciones-impersonales/README.md',
  },
  {
    id: 'servicio-repeticion-palabras',
    name: 'API Detección de Repetición de Palabras',
    shortDescription: 'Encuentra palabras repetidas y cuenta sus apariciones.',
    markdownPath: '/content/servicio-repeticion-palabras/README.md',
  },
  {
    id: 'verbos_percepcion_opinion',
    name: 'API Detección de Verbos de Percepción y Opinión',
    shortDescription: 'Detecta verbos de percepción y opinión en textos en inglés.',
    markdownPath: '/content/verbos_percepcion_opinion/README.md',
  },
  {
    id: 'metricas-de-legibilidad',
    name: 'API de Métricas de Legibilidad',
    shortDescription: 'Calcula la dificultad de comprensión de un texto.',
    markdownPath: '/content/metricas-de-legibilidad/README.md',
  },
  {
    id: 'servicio-deteccion-cliches',
    name: 'API Detección de Clichés',
    shortDescription: 'Detecta clichés y expresiones semánticamente similares.',
    markdownPath: '/content/servicio-deteccion-cliches/README.md',
  },
  {
    id: 'detector_adverbios',
    name: 'API Detección y Clasificación de Adverbios',
    shortDescription: 'Identifica y clasifica adverbios en textos en inglés.',
    markdownPath: '/content/detector_adverbios/README.md',
  },
  {
    id: 'detector_doble_negacion',
    name: 'API Detección de Doble Negación',
    shortDescription: 'Identifica la presencia de doble negación en textos en inglés.',
    markdownPath: '/content/detector_doble_negacion/README.md',
  },
  {
    id: 'deteccion_verbos_modales',
    name: 'API Detección de Inconsistencias de Verbos Modales',
    shortDescription: 'Detecta acciones asociadas con categorías modales diferentes.',
    markdownPath: '/content/deteccion_verbos_modales/README.md',
  },
]
