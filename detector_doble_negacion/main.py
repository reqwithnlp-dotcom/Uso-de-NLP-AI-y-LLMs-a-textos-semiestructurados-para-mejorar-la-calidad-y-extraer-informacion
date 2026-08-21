import spacy
from spacy import displacy

# Cargar el modelo Transformer 
# (Requiere previa instalación: python -m spacy download en_core_web_trf)
nlp = spacy.load("en_core_web_trf")

# Oraciones para probar diferentes escenarios
oraciones = [
    "The error is not uncommon.",      # Atenuación (Formal)
    "I don't know nothing.",           # Concordancia negativa (Informal)
    "I didn't say that I won't go."    # Negaciones en distintos alcances
]

# Analizar la primera oración como ejemplo
doc = nlp(oraciones[1])

print(f"Análisis de: '{doc.text}'\n")
print(f"{'TOKEN':<12} | {'DEPENDENCIA':<12} | {'NODO PADRE':<12} | {'HIJOS DEL NODO'}")
print("-" * 65)

# 1. Recorrido de los nodos (Consola)
for token in doc:
    hijos = [hijo.text for hijo in token.children]
    print(f"{token.text:<12} | {token.dep_:<12} | {token.head.text:<12} | {hijos}")

# 2. Visualización Gráfica (Navegador)
print("\nLevantando servidor de visualización...")
print("Abrí http://localhost:5000 en tu navegador. (Presioná Ctrl+C para detener)")

# displacy.serve levanta un servidor web para renderizar el árbol interactivo
displacy.serve(doc, style="dep", port=5000)