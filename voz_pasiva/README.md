# Detección de voz pasiva en inglés

Servicio y librería en Python para analizar oraciones en inglés y detectar el uso de voz pasiva, identificando tanto la presencia de la estructura pasiva como las posiciones donde se encuentran los auxiliares pasivos y verbos en participio.

La idea de fondo: La voz pasiva se utiliza habitualmente en textos formales o académicos, pero su uso excesivo o inadecuado puede restar claridad y dinamismo a la redacción. Este servicio permite automatizar la detección de estas estructuras para auditorías de estilo o análisis gramatical.

# Estructura del Proyecto


├── detector.py      # Lógica principal del analizador lingüístico utilizando spaCy

├── main.py          # Script interactivo de consola para probar oraciones en tiempo real

└── test.py          # Suite de pruebas unitarias basadas en asserts

# Requisitos Previos

- Python 3.8 o superior
- Modelo de procesamiento de lenguaje natural de spaCy en inglés (`en_core_web_sm`)

## Instalación

1. Ubicarse en la carpeta del proyecto:
   cd deteccion_voz_pasiva

2. (Opcional pero recomendado) Creá y activá un entorno virtual:
   python -m venv venv
   source venv/bin/activate   En Windows: venv\Scripts\activate

3. Instalá spaCy y descargá el modelo de inglés:
   pip install spacy
   python -m spacy download en_core_web_sm

## Ejecución

Modo Interactivo (CLI)

Ejecutá el script principal para ingresar oraciones de manera interactiva desde la consola:
python main.py

Ejemplo de uso en consola:
   Ingrese una oración en inglés: The letter was written by Juan.
   ✅ La oración está en voz pasiva
   Posiciones detectadas:
   [(11, 22)]

Pruebas Unitarias

Ejecutá la suite de pruebas para verificar el correcto funcionamiento del detector:
python test.py

Salida esperada:
   ✅ TODOS LOS TESTS PASARON

Uso como Módulo / Librería

Podés importar la lógica de detección directamente en otros scripts de Python:

from detector import is_passive, passive_positions

oracion = "A bridge was built over the river."

# 1. Verificación booleana
if is_passive(oracion):
    print("Se detectó voz pasiva")

# 2. Obtención de ubicaciones (tuplas con caracteres de inicio y fin)
posiciones = passive_positions(oracion)
print("Rangos de caracteres:", posiciones)  # Output: [(11, 20)]

Cómo funciona (Resumen Técnico)

El servicio utiliza el modelo spaCy (`en_core_web_sm`) para realizar análisis sintáctico y etiquetado gramatical (POS tagging) sobre el texto:

- is_passive(sentence): Convierte la oración en un objeto `Doc` de spaCy y recorre sus tokens buscando dependencias sintácticas marcadas como `auxpass` (auxiliar pasivo, ej. *was*, *were*, *is*, *been*). Si encuentra al menos una, retorna `True`.
- passive_positions(sentence): Identifica la posición inicial (`idx`) del token `auxpass` y busca extender el rango hasta el verbo principal en participio pasado (`tag_ == "VBN"`). Devuelve una lista de tuplas `(inicio, fin)` con los índices de caracteres en la cadena original.
