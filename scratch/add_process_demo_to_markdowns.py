import os

content_dir = os.path.abspath("WebDocumentacion/public/content")

services = [
    'deteccion_conectores_logicos',
    'weak_verbs',
    'abstract_words',
    'voz_pasiva',
    'oraciones-impersonales',
    'servicio-repeticion-palabras',
    'verbos_percepcion_opinion',
    'metricas-de-legibilidad',
    'servicio-deteccion-cliches',
    'detector_adverbios',
    'detector_doble_negacion',
    'deteccion_verbos_modales',
    'deteccion_puntuacion_inusual',
    'povshift',
    'verb_tense_inconsistencies',
]

snippet = "\n## Simulación interactiva del proceso\n\n```process-demo\n```\n\n"

for s in services:
    readme_path = os.path.join(content_dir, s, "README.md")
    if not os.path.exists(readme_path):
        print(f"Skipping {s}: README.md does not exist")
        continue

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "```process-demo" in content:
        print(f"Already present in {s}")
        continue

    # Insert before ## Ejemplos Visuales if present, else append
    target = "## Ejemplos Visuales"
    if target in content:
        parts = content.split(target, 1)
        new_content = parts[0] + snippet + target + parts[1]
    else:
        new_content = content + snippet

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"Updated {s}")

print("Done updating markdowns.")
