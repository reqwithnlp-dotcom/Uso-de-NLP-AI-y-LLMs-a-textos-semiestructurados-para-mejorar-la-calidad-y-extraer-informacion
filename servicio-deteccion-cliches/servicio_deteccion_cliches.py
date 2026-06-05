from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import spacy

# ============================================================
# Configuración
# ============================================================

_CLICHES_FILE = Path(__file__).parent / "cliches.txt"
_SBERT_MODEL_NAME = "paraphrase-MiniLM-L6-v2"
_DEFAULT_UMBRAL_STS = 0.75

# Pronombres posesivos que se normalizan a "one's" para matching flexible
_POSESIVOS = frozenset({"your", "my", "his", "her", "their", "its", "our"})

# ============================================================
# Carga del modelo spaCy
# ============================================================

_nlp = spacy.load("en_core_web_sm")

# ============================================================
# Normalización de tokens
# ============================================================

def _normalizar_tokens(texto: str) -> list[str]:
    """
    Aplica al texto: lowercase → eliminar puntuación/espacios →
    reemplazar posesivos por 'one's' → lematizar.
    Retorna lista de tokens normalizados.
    """
    doc = _nlp(texto)
    tokens: list[str] = []
    for token in doc:
        if token.is_punct or token.is_space:
            continue
        t = token.text.lower()
        if t in _POSESIVOS:
            tokens.append("one's")
        else:
            tokens.append(token.lemma_.lower())
    return tokens


# ============================================================
# Carga del corpus (al importar el módulo)
# ============================================================

def _cargar_corpus(ruta: Path) -> dict[str, str]:
    """
    Lee cliches.txt y retorna:
    { forma_normalizada_unida: cliché_canónico_en_minúsculas }
    """
    corpus: dict[str, str] = {}
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            cliche = linea.strip()
            if not cliche:
                continue
            canonico = cliche.lower()
            tokens = _normalizar_tokens(cliche)
            if tokens:
                clave = " ".join(tokens)
                corpus[clave] = canonico
    return corpus


_CORPUS_NORM: dict[str, str] = _cargar_corpus(_CLICHES_FILE)
_MAX_N: int = max(len(k.split()) for k in _CORPUS_NORM)

# ============================================================
# SBERT — carga diferida (lazy)
# ============================================================

_sbert_model = None
_corpus_embeddings: Optional[np.ndarray] = None
_corpus_canonicals: list[str] = []


def _get_sbert():
    """Carga el modelo SBERT y pre-vectoriza el corpus (solo la primera vez)."""
    global _sbert_model, _corpus_embeddings, _corpus_canonicals
    if _sbert_model is not None:
        return _sbert_model, _corpus_embeddings

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise ImportError(
            "El análisis profundo requiere 'sentence-transformers'. "
            "Instalalo con: pip install sentence-transformers"
        ) from exc

    _sbert_model = SentenceTransformer(_SBERT_MODEL_NAME)
    _corpus_canonicals = list(_CORPUS_NORM.values())
    _corpus_embeddings = _sbert_model.encode(
        _corpus_canonicals,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    return _sbert_model, _corpus_embeddings


# ============================================================
# Utilidades compartidas
# ============================================================

def _get_word_spans(texto: str) -> list[tuple[str, str, int, int]]:
    """
    Tokeniza el texto con spaCy y retorna, para cada token que no sea
    puntuación ni espacio:
      (token_normalizado, texto_original, char_start, char_end)
    """
    doc = _nlp(texto)
    resultado: list[tuple[str, str, int, int]] = []
    for token in doc:
        if token.is_punct or token.is_space:
            continue
        t = token.text.lower()
        norm = "one's" if t in _POSESIVOS else token.lemma_.lower()
        resultado.append((norm, token.text, token.idx, token.idx + len(token.text)))
    return resultado


def _eliminar_solapamientos(
    matches: list[tuple[int, int, str]],
) -> list[tuple[int, int, str]]:
    """
    Dado [(char_start, char_end, frase), ...], elimina solapamientos
    priorizando el span más largo. Retorna ordenado por posición.
    """
    # Priorizar spans más largos
    ordenados = sorted(matches, key=lambda m: -(m[1] - m[0]))
    seleccionados: list[tuple[int, int, str]] = []
    ocupado: list[tuple[int, int]] = []

    for start, end, frase in ordenados:
        if any(start < e and end > s for s, e in ocupado):
            continue
        seleccionados.append((start, end, frase))
        ocupado.append((start, end))

    seleccionados.sort(key=lambda m: m[0])
    return seleccionados


# ============================================================
# Fase 1 — Filtrado inicial (n-gramas)
# ============================================================

def _fase1_filtrado(texto: str) -> list[tuple[int, int, str]]:
    """
    Compara n-gramas normalizados del texto contra _CORPUS_NORM.
    Retorna lista de (char_start, char_end, frase_original_en_minúsculas).
    """
    spans = _get_word_spans(texto)
    if not spans:
        return []

    n_tokens = len(spans)
    candidatos: list[tuple[int, int, str]] = []

    # Iterar de mayor a menor n para dar prioridad a matches más largos
    for n in range(min(_MAX_N, n_tokens), 1, -1):
        for i in range(n_tokens - n + 1):
            ventana = spans[i: i + n]
            clave = " ".join(norm for norm, _, _, _ in ventana)
            if clave in _CORPUS_NORM:
                char_start = ventana[0][2]
                char_end = ventana[-1][3]
                frase = texto[char_start:char_end].lower()
                candidatos.append((char_start, char_end, frase))

    return _eliminar_solapamientos(candidatos)


# ============================================================
# Fase 2 — Análisis semántico profundo (SBERT)
# ============================================================

def _eliminar_solapamientos_por_score(
    matches: list[tuple[int, int, str, float]],
) -> list[tuple[int, int, str]]:
    """
    Dado [(char_start, char_end, frase, score), ...], elimina solapamientos
    priorizando el mayor score (no el span más largo).
    Retorna [(char_start, char_end, frase)] ordenado por posición.
    """
    ordenados = sorted(matches, key=lambda m: -m[3])
    seleccionados: list[tuple[int, int, str]] = []
    ocupado: list[tuple[int, int]] = []

    for start, end, frase, _score in ordenados:
        if any(start < e and end > s for s, e in ocupado):
            continue
        seleccionados.append((start, end, frase))
        ocupado.append((start, end))

    seleccionados.sort(key=lambda m: m[0])
    return seleccionados


def _fase2_semantico(
    texto: str,
    excluir_spans: list[tuple[int, int]],
    umbral: float,
) -> list[tuple[int, int, str]]:
    """
    Ventana deslizante sobre el texto con vectorización SBERT.
    Omite ventanas ya cubiertas por la Fase 1.
    Retorna lista de (char_start, char_end, frase_en_minúsculas).
    """
    modelo, corpus_embs = _get_sbert()

    spans = _get_word_spans(texto)
    if len(spans) < 2:
        return []

    n_tokens = len(spans)

    # Construir todas las ventanas
    ventanas_info: list[tuple[int, int]] = []

    for n in range(2, min(_MAX_N + 1, n_tokens + 1)):
        for i in range(n_tokens - n + 1):
            ventana = spans[i: i + n]
            char_start = ventana[0][2]
            char_end = ventana[-1][3]

            # Omitir ventanas ya detectadas por Fase 1
            ya_cubierta = any(char_start >= s and char_end <= e for s, e in excluir_spans)
            if ya_cubierta:
                continue

            ventanas_info.append((char_start, char_end))

    if not ventanas_info:
        return []

    # Vectorizar en batch y calcular similitud coseno con SBERT
    textos_ventana = [texto[s:e] for s, e in ventanas_info]
    ventana_embs = modelo.encode(
        textos_ventana,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )
    # Ambas matrices están normalizadas → producto punto = similitud coseno
    similitudes = ventana_embs @ corpus_embs.T  # (n_ventanas, n_cliches)
    max_sims = similitudes.max(axis=1)

    candidatos: list[tuple[int, int, str, float]] = []
    for sim, (char_start, char_end) in zip(max_sims, ventanas_info):
        if sim >= umbral:
            frase = texto[char_start:char_end].lower()
            candidatos.append((char_start, char_end, frase, float(sim)))

    return _eliminar_solapamientos_por_score(candidatos)


# ============================================================
# Función pública
# ============================================================

def detectar_cliches(
    texto: str,
    filtrado_inicial: bool = True,
    analisis_profundo: bool = True,
    umbral_semantico: float = _DEFAULT_UMBRAL_STS,
) -> list[str]:
    """
    Detecta clichés en un texto en inglés.

    Parámetros
    ----------
    texto : str
        La oración o párrafo a analizar.
    filtrado_inicial : bool (default=True)
        Si es True, ejecuta la Fase 1: n-gramas normalizados contra el corpus
        cliche500 usando spaCy (rápido, coincidencia exacta de lemas).
    analisis_profundo : bool (default=True)
        Si es True, ejecuta la Fase 2: similitud semántica SBERT con ventana
        deslizante (captura variaciones y paráfrasis no exactas).
        Requiere 'sentence-transformers' instalado.
    umbral_semantico : float (default=0.75)
        Umbral de similitud coseno para la Fase 2. Rango [0, 1].

    Retorna
    -------
    list[str]
        Frases exactas (en minúsculas, tal como aparecen en el texto)
        identificadas como clichés, ordenadas por posición de aparición.
        Lista vacía si no se detectan clichés.
    """
    if not texto or not texto.strip():
        return []

    matches: list[tuple[int, int, str]] = []

    if filtrado_inicial:
        matches.extend(_fase1_filtrado(texto))

    if analisis_profundo:
        excluir = [(s, e) for s, e, _ in matches]
        matches_fase2 = _fase2_semantico(texto, excluir, umbral_semantico)
        matches.extend(matches_fase2)

    # Deduplicación global y ordenamiento por posición
    matches = _eliminar_solapamientos(matches)

    return [frase for _, _, frase in matches]
