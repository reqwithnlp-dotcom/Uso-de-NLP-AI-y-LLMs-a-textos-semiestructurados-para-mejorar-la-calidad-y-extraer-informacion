import os
import re

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

sim_block = "## Simulación interactiva del proceso\n\n```process-demo\n```\n\n"

for s in services:
    readme_path = os.path.join(content_dir, s, "README.md")
    if not os.path.exists(readme_path):
        continue

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove any existing simulation block
    content_clean = re.sub(
        r"\n*## Simulación interactiva del proceso\s*```process-demo\s*```\n*",
        "\n\n",
        content
    )

    # 2. Insert before ## Definición (or ## 1. Definicion)
    def_match = re.search(r"(##\s*(?:1\.\s*)?Definici[oó]n)", content_clean, re.IGNORECASE)
    if def_match:
        idx = def_match.start()
        new_content = content_clean[:idx] + sim_block + content_clean[idx:]
    else:
        # If no definition heading, put it right after first H1
        h1_match = re.search(r"(#[^\n]+\n+)", content_clean)
        if h1_match:
            idx = h1_match.end()
            new_content = content_clean[:idx] + "\n" + sim_block + content_clean[idx:]
        else:
            new_content = sim_block + content_clean

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Moved simulation to top in {s}")

print("All markdowns updated successfully.")
