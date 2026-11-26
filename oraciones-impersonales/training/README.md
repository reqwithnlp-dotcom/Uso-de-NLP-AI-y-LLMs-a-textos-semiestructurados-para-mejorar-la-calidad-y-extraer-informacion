# Entrenamiento de la capa 2 (clasificador spaCy)

Corpus y scripts para entrenar el clasificador **PERSONAL / IMPERSONAL** que
desambigua las oraciones que la capa 1 (reglas) deja como `ambiguous`.

Esta carpeta es **solo de entrenamiento**: no se importa en tiempo de
ejecución. El servicio únicamente *carga* el modelo ya entrenado
(`model/classifier.py`).

## Estructura

```
training/
  config.cfg          <- config de spaCy (se versiona)
  data/raw/           <- corpus etiquetado, fuente de verdad (se versiona)
    personales.txt  impersonales.txt  unclear.txt
  data/external/      <- treebanks UD descargados        (NO se versiona)
  data/review/        <- CSV de candidatas a revisar     (NO se versiona)
  data/corpus/        <- train/dev/test .spacy + .jsonl  (NO se versiona)
  output/             <- modelos entrenados              (NO se versiona)
  scripts/
    mine_candidates.py   UD/texto libre -> CSV con etiqueta propuesta
    import_reviewed.py   CSV revisado   -> data/raw/*.txt
    build_corpus.py      data/raw/*.txt -> data/corpus/*.spacy
    evaluate.py          capa 1 vs capa 2 vs combinado
```

Todos los comandos se corren **desde la raíz del servicio** (la carpeta que
contiene `main.py`) y con el venv activado.

## Flujo completo

```
mine_candidates -> (revisión humana) -> import_reviewed -> build_corpus
     -> spacy train -> evaluate (dev) -> evaluate (test, una vez) -> copiar a model/textcat
```

### 1. Descargar los treebanks UD (una sola vez)

Se usan UD English-EWT (web) y GUM (géneros variados). UD anota el "it" y el
"there" vacíos como `expl`, lo que da una etiqueta *silver* hecha por humanos.

```bash
mkdir -p training/data/external && cd training/data/external
for s in train dev test; do
  curl -sSfLO https://raw.githubusercontent.com/UniversalDependencies/UD_English-EWT/master/en_ewt-ud-$s.conllu
  curl -sSfLO https://raw.githubusercontent.com/UniversalDependencies/UD_English-GUM/master/en_gum-ud-$s.conllu
done
cd ../../..
```

### 2. Minar candidatas

```bash
python training/scripts/mine_candidates.py
python training/scripts/mine_candidates.py --extra otro_texto.txt   # opcional
```

Genera `training/data/review/candidates.csv` (separado por `;`, abre bien en
Excel en español). Por cada oración trae:

| columna | qué es |
|---|---|
| `ud_signal` | `EXPL_ROOT` (sujeto vacío en la principal), `EXPL_SUB` (solo en subordinada), `EXPL_OTHER` (expletivo objeto o modismo), `IT_REF` ("it" referencial), `SUBJ` (otro sujeto), `NONE` (texto libre) |
| `l1_*` | lo que dijo la capa 1 |
| `proposed_label` | UD si hay señal; si no, la capa 1 si no fue ambigua |
| `conflict` | UD y capa 1 no coinciden: **revisar primero** |
| `final_label` | **lo completás vos** |

Las filas vienen ordenadas así: primero los conflictos, después las ambiguas y al final el resto.
Los topes por grupo están en `DEFAULT_CAPS`, o se escalan con `--scale`.

### 3. Revisar

Completá `final_label` con `PERSONAL`, `IMPERSONAL` o `UNCLEAR`. También se aceptan `P`, `I` y `U`.
Si dejás la celda vacía, la oración se descarta.

**Criterio de etiquetado (importante, mantenelo consistente):**

- Se etiqueta por la **cláusula principal**. "I think there is a problem." es
  PERSONAL: el sujeto de la principal es "I". "There is a problem, so I left." es
  un caso mixto, así que va a UNCLEAR o se descarta.
- IMPERSONAL es un sujeto vacío ("it"/"there" sin referente): extraposición,
  existencial, clima ("It gets dark early"), pasiva de reporte.
- Desconfiá de las etiquetas silver: UD a veces marca `nsubj` en "It is not
  clear whether…" (que es impersonal), y los textos web tienen typos ("its easy").
- Si dudás, ponela en UNCLEAR. Una etiqueta forzada mete ruido.

### 4. Importar lo revisado

```bash
python training/scripts/import_reviewed.py --dry-run   # ver qué haría
python training/scripts/import_reviewed.py
```

Agrega las oraciones al final de `data/raw/*.txt`, bajo un comentario con la fecha, y saltea
las que ya están. `--accept-proposed` usa `proposed_label` donde
`final_label` está vacío, pero solo en filas sin conflicto. Es útil para pilotos rápidos,
pero arrastra el ruido de las etiquetas silver.

**Completá a mano lo que UD no trae.** Los treebanks casi no tienen oraciones de
**clima** ("It is snowing", "It gets dark early in winter") ni muchas
**pasivas de reporte** ("It is said that…"). Escribilas directamente en
`data/raw/impersonales.txt`, junto con sus *hard negatives* en
`personales.txt` ("It gets cheaper every year." con un antecedente claro).

### 5. Construir el corpus

```bash
python training/scripts/build_corpus.py
```

Avisa de duplicados y desbalances, hace un split estratificado 80/10/10 y escribe
`.spacy` y `.jsonl`. Apuntá a una relación cercana a 1:1 entre clases, ajustando los
topes de `mine_candidates.py` (`SUBJ` frente a `EXPL_ROOT_*`).

### 6. Entrenar

```bash
python -m spacy train training/config.cfg --paths.train training/data/corpus/train.spacy --paths.dev training/data/corpus/dev.spacy --output training/output
```

`config.cfg` parte de `spacy init config --pipeline textcat_multilabel
--optimize efficiency` con estos cambios:

- **`TextCatEnsemble`** (una CNN sobre tokens más un BOW de bigramas) en lugar del BOW
  unigrama del preset. El orden importa: "It is X **to**…" frente a "It is X.".
- `seed = 42`, `max_steps = 6000` y `patience = 1200` para un corpus chico.

Se usa `textcat_multilabel` y **no** `textcat` porque el multilabel da una
probabilidad **independiente** por etiqueta. Eso permite que ambas queden
altas (contradictorio) o ambas bajas (sin evidencia), y el servicio lo
traduce en `UNDECIDED` (ver `decide()` en `model/classifier.py`).

Para comparar en el informe, se puede usar `--optimize accuracy` (transformer, requiere
`spacy-transformers` y conviene GPU).

### 7. Evaluar

```bash
# Ajuste de umbral/margen: SOLO en dev
python training/scripts/evaluate.py --split dev --sweep

# Medición final: test, UNA vez, con los valores elegidos en dev
python training/scripts/evaluate.py --split test --threshold 0.5 --margin 0.2 --json training/output/metrics_test.json
```

Compara sobre las mismas oraciones:

1. **Capa 1 sola**, que es el baseline. Las ambiguas cuentan como error y la cobertura se informa aparte.
2. **Capa 2 sola**, con argmax.
3. **Combinado**, que es lo que hace el servicio.

La métrica clave es la exactitud de la capa 2 **dentro del subconjunto
ambiguo** de la capa 1, porque es exactamente el trabajo que se le delega.
Si el combinado no le gana a la capa 1 sola, no vale la pena.

### 8. Desplegar en el servicio

```bash
cp -r training/output/model-best model/textcat
```

Otra opción es apuntar la variable `IMPERSONAL_TEXTCAT_PATH` a la carpeta del modelo.
El umbral y el margen se ajustan con `IMPERSONAL_L2_THRESHOLD` y `IMPERSONAL_L2_MARGIN`.
`GET /health` devuelve `layer2_loaded: true` cuando el modelo cargó.
