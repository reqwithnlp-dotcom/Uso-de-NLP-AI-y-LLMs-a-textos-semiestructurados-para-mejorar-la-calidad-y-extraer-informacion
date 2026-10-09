# Detección de voz pasiva en inglés

Servicio y librería en Python para analizar oraciones en inglés y detectar el uso de voz pasiva, identificando tanto la presencia de la estructura pasiva como las posiciones donde se encuentran los auxiliares pasivos y verbos en participio.

La idea de fondo: La voz pasiva se utiliza habitualmente en textos formales o académicos, pero su uso excesivo o inadecuado puede restar claridad y dinamismo a la redacción. Este servicio permite automatizar la detección de estas estructuras para auditorías de estilo o análisis gramatical.

# Estructura del Proyecto


├── detector.py      # Lógica principal del analizador lingüístico utilizando spaCy (detección y conversión a voz activa)
├── main.py          # API FastAPI y servidor de endpoints REST
└── test_detector.py # Suite de pruebas unitarias

# Requisitos Previos

- Python 3.8 o superior
- Modelo de procesamiento de lenguaje natural de spaCy en inglés (`en_core_web_sm`)

## Instalación

1. Ubicarse en la carpeta del proyecto:
   cd voz_pasiva

2. (Opcional pero recomendado) Creá y activá un entorno virtual:
   python -m venv venv
   source venv/bin/activate   En Windows: venv\Scripts\activate

3. Instalá dependencias y descargá el modelo de inglés:
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm

## Ejecución

Servicio API (FastAPI / Uvicorn)

Ejecutá el servidor API en el puerto 8011:
uvicorn main:app --host 0.0.0.0 --port 8011

Pruebas Unitarias

Ejecutá la suite de pruebas para verificar el correcto funcionamiento del detector:
python test_detector.py

Salida esperada:
   [OK] TODOS LOS TESTS PASARON EXITOSAMENTE

Uso como Módulo / Librería

Podés importar la lógica de detección y conversión directamente en otros scripts de Python:

from detector import is_passive, passive_positions, to_active_voice

oracion = "The letter was written by Juan."

# 1. Verificación booleana
if is_passive(oracion):
    print("Se detectó voz pasiva")

# 2. Obtención de ubicaciones (tuplas con caracteres de inicio y fin)
posiciones = passive_positions(oracion)
print("Rangos de caracteres:", posiciones)  # Output: [(11, 22)]

# 3. Conversión a voz activa
activa = to_active_voice(oracion)
print("Voz activa:", activa)  # Output: "Juan wrote the letter."

Cómo funciona (Resumen Técnico)

El servicio utiliza el modelo spaCy (`en_core_web_sm`) para realizar análisis sintáctico y etiquetado gramatical (POS tagging) sobre el texto:

- is_passive(sentence): Convierte la oración en un objeto `Doc` de spaCy y recorre sus tokens buscando dependencias sintácticas marcadas como `auxpass` (auxiliar pasivo, ej. *was*, *were*, *is*, *been*). Si encuentra al menos una, retorna `True`.
- passive_positions(sentence): Identifica la posición inicial (`idx`) del token `auxpass` y busca extender el rango hasta el verbo principal en participio pasado (`tag_ == "VBN"`). Devuelve una lista de tuplas `(inicio, fin)` con los índices de caracteres en la cadena original.
- to_active_voice(sentence): Identifica el agente ejecutor (`agent` / `by`), el sujeto paciente (`nsubjpass`), los tiempos y modales auxiliares, y reconstituye sintácticamente la oración en voz activa.