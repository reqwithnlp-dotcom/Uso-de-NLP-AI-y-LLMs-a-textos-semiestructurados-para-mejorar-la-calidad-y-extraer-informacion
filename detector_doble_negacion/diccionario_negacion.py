"""
Diccionario de negación para el detector de doble negación.

Contiene:
- PALABRAS_NEGATIVAS: set exhaustivo de palabras con carga semántica negativa en inglés.
- PREFIJOS_NEGATIVOS: tupla de prefijos que confieren sentido negativo a una palabra.

Este archivo centraliza todo el vocabulario negativo para facilitar
su mantenimiento y extensión.
"""

# =============================================================================
# PALABRAS NEGATIVAS
# =============================================================================
# Organizadas por categoría semántica para facilitar revisión y extensión.

# --- Pronombres y determinantes negativos ---
_PRONOMBRES_NEGATIVOS = {
    "no",          
    "nothing",     
    "nobody",       
    "no one",       
    "none",         
    "neither",     
    "nor",         
}

# --- Adverbios negativos de lugar, tiempo y modo ---
_ADVERBIOS_NEGATIVOS = {
    "nowhere",     
    "never",        
    "nevermore",   
    "nowise",       
    "noway",       
    "noways",       
    "nohow",        
    "nowhither",  
    "nowt",         
}

# --- Adverbios restrictivos / de mínima (near-negatives) ---
_ADVERBIOS_RESTRICTIVOS = {
    "hardly",      
    "barely",       
    "scarcely",    
    "seldom",       
    "rarely",      
    "little",       
}

# --- Otras palabras con carga negativa fuerte ---
_OTROS_NEGATIVOS = {
    "without",     
    "lack",       
    "lacking",      
    "absent",     
    "devoid",      
    "void",         
    "deny",       
    "denial",      
    "refuse",       
    "refusal",      
    "reject",       
    "rejection",   
    "fail",        
    "failure",      
    "unable",      
    "impossible",  
    "unnecessary",  
    "unlikely",     
}

# --- Contracciones negativas ---
# spacy generalmente las separa en token + "n't", pero por robustez
# las incluimos por si algún tokenizador las mantiene juntas.
_CONTRACCIONES_NEGATIVAS = {
    "not",         
    "n't",          
    "cannot",     
    "can't",       
    "don't",      
    "doesn't",      
    "didn't",      
    "won't",       
    "wouldn't",  
    "shouldn't", 
    "couldn't",    
    "isn't",        
    "aren't",      
    "wasn't",       
    "weren't",      
    "hasn't",      
    "haven't",      
    "hadn't",       
    "mustn't",     
    "needn't",    
    "shan't",      
    "mightn't",    
    "oughtn't",    
}

# --- Conjunto unificado ---
PALABRAS_NEGATIVAS: set[str] = (
    _PRONOMBRES_NEGATIVOS
    | _ADVERBIOS_NEGATIVOS
    | _ADVERBIOS_RESTRICTIVOS
    | _OTROS_NEGATIVOS
    | _CONTRACCIONES_NEGATIVAS
)


# =============================================================================
# PREFIJOS NEGATIVOS
# =============================================================================
# Tupla de prefijos que, al anteponerse a una raíz, invierten o niegan
# su significado. Se usa con str.startswith().
#
# NOTA: El orden importa para str.startswith() — los prefijos más largos
# deben ir primero para evitar falsos positivos (ej: "counter" antes que "co").

PREFIJOS_NEGATIVOS: tuple[str, ...] = (
    "counter",  
    "contra",  
    "anti",     
    "dis",      
    "mis",     
    "non",     
    "un",       
    "in",     
    "im",     
    "il",       
    "ir",      
    "de",   
)
