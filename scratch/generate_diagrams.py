import spacy
from spacy import displacy
import os

nlp = spacy.load("en_core_web_sm")

content_base = os.path.abspath("WebDocumentacion/public/content")

povshift_dir = os.path.join(content_base, "povshift")
os.makedirs(povshift_dir, exist_ok=True)

tenses_dir = os.path.join(content_base, "verb_tense_inconsistencies")
os.makedirs(tenses_dir, exist_ok=True)

options = {
    "compact": False,
    "color": "#17201d",
    "bg": "#ffffff",
    "font": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    "distance": 105
}

# 1. POV Shift 1
doc1 = nlp("John wondered where Mary was.")
svg1 = displacy.render(doc1, style="dep", options=options)
with open(os.path.join(povshift_dir, "diagrama_povshift_1.svg"), "w", encoding="utf-8") as f:
    f.write(svg1)

# 2. POV Shift 2
doc2 = nlp("Mary knew he was waiting.")
svg2 = displacy.render(doc2, style="dep", options=options)
with open(os.path.join(povshift_dir, "diagrama_povshift_2.svg"), "w", encoding="utf-8") as f:
    f.write(svg2)

# 3. Verb Tense 1: Discordancia entre clausulas coordinadas
doc3 = nlp("The system received the request and processes the payment.")
svg3 = displacy.render(doc3, style="dep", options=options)
with open(os.path.join(tenses_dir, "diagrama_tiempos_verbales_1.svg"), "w", encoding="utf-8") as f:
    f.write(svg3)

# 4. Verb Tense 2: Inconsistencia con adverbio temporal
doc4 = nlp("Yesterday the system processes the batch request.")
svg4 = displacy.render(doc4, style="dep", options=options)
with open(os.path.join(tenses_dir, "diagrama_tiempos_verbales_2.svg"), "w", encoding="utf-8") as f:
    f.write(svg4)

print("SVGs generated successfully.")
