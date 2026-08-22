import spacy
from spacy import displacy
import os

nlp = spacy.load("en_core_web_trf")
archivo_html = "arbol_sintactico.html"

print("Escribí 'salir' para terminar el programa.")
print(f"Para visualizar: Abrí el archivo '{archivo_html}' en tu navegador y tocá F5 cada vez que ingreses una frase.\n")

while True:
    texto = input("\nIngresá una frase: ")
    
    if texto.lower() == 'salir':
        break
    if not texto.strip():
        continue

    doc = nlp(texto)

    print(f"\nAnálisis de: '{doc.text}'")
    print(f"{'TOKEN':<12} | {'DEPENDENCIA':<12} | {'NODO PADRE':<12} | {'HIJOS DEL NODO'}")
    print("-" * 65)

    for token in doc:
        hijos = [hijo.text for hijo in token.children]
        print(f"{token.text:<12} | {token.dep_:<12} | {token.head.text:<12} | {hijos}")

    # Renderiza y guarda en un archivo estático en lugar de levantar el servidor
    html = displacy.render(doc, style="dep", page=True)
    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(html)
        
    print(f"\n[+] Árbol gráfico actualizado. Refrescá (F5) tu navegador.")