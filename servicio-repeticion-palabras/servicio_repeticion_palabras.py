from collections import defaultdict
import spacy

# Cargamos el modelo en inglés
nlp = spacy.load("en_core_web_sm")

def detectar_repeticiones(texto: str, ignorar_stopwords: bool = True, lematizacion: bool = True):
    """
    Detecta palabras repetidas en un texto usando procesamiento de lenguaje natural.

    Parámetros:
    -----------
    texto : str
        El texto de entrada a analizar.
    ignorar_stopwords : bool (default=True)
        Si es True, ignora palabras vacías (stopwords) como "the", "is", "a", etc.
    lematizacion : bool (default=True)
        Si es True, agrupa palabras por su lema (forma base). Por ejemplo,
        "running" y "runs" se agrupan bajo "run".
        Si es False, compara las palabras en su forma literal (en minúsculas).

    Retorna:
    --------
    list[dict]
        Lista de diccionarios, ordenada de mayor a menor repetición. Cada elemento tiene:
        - "word"    : str   -> la palabra (o lema) repetida
        - "count"   : int   -> cantidad de veces que aparece
        - "indices" : list  -> lista de {"start": int, "end": int} con las posiciones
                               en el string original donde aparece cada ocurrencia
    """
    doc = nlp(texto)
    agrupador = defaultdict(list)

    for token in doc:
        # 1. Ignorar signos de puntuación y espacios
        if token.is_punct or token.is_space:
            continue

        # 2. Filtro de Stop Words
        if ignorar_stopwords and token.is_stop:
            continue

        # 3. Definir la clave (siempre en minúsculas)
        if lematizacion:
            clave_palabra = token.lemma_.lower()
        else:
            clave_palabra = token.text.lower()

        # 4. Cálculo correcto de índices en el string original
        inicio = token.idx
        fin = inicio + len(token.text)

        agrupador[clave_palabra].append({
            "start": inicio,
            "end": fin
        })

    # 5. Filtrar solo las palabras que aparecieron más de una vez
    resultado = []
    for palabra, indices in agrupador.items():
        if len(indices) > 1:
            resultado.append({
                "word": palabra,
                "count": len(indices),
                "indices": indices
            })

    # Ordenamos por cantidad de repeticiones (de mayor a menor)
    return sorted(resultado, key=lambda x: x["count"], reverse=True)
