# Uso de NLP, AI y LLMs a Textos Semiestructurados

Este repositorio contiene un ecosistema de microservicios de Procesamiento de Lenguaje Natural (NLP), Inteligencia Artificial y una aplicación web integrada para el análisis, extracción de información y mejora de la calidad de redacción en textos técnicos y semiestructurados en inglés.

---

## 📋 Catálogo de Servicios y Mapeo de Puertos

Para permitir la ejecución simultánea en desarrollo local sin conflictos ni colisiones, cada microservicio tiene asignado un puerto dedicado y expone su documentación interactiva mediante Swagger UI (`/docs`):

| # | Servicio | Directorio | Puerto | Documentación / URL | Descripción |
|:-:|---|---|:---:|---|---|
| 1 | **AppWeb (Portal Django)** | `AppWeb` | **`8000`** | [http://127.0.0.1:8000](http://127.0.0.1:8000) | Portal web y panel principal de integración. |
| 2 | **Detección de Clichés** | `servicio-deteccion-cliches` | **`8001`** | [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs) | Detecta clichés y expresiones trilladas mediante spaCy y SBERT. |
| 3 | **Repetición de Palabras** | `servicio-repeticion-palabras` | **`8002`** | [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs) | Identifica palabras reiterativas con soporte de lematización. |
| 4 | **Conectores Lógicos** | `deteccion_conectores_logicos` | **`8003`** | [http://127.0.0.1:8003/docs](http://127.0.0.1:8003/docs) | Clasifica conectores lógicos de causa, contraste, adición, etc. |
| 5 | **Doble Negación** | `detector_doble_negacion` | **`8004`** | [http://127.0.0.1:8004/docs](http://127.0.0.1:8004/docs) | Detecta dobles negaciones sintácticas con modelo Transformer. |
| 6 | **Puntuación Inusual** | `deteccion_puntuacion_inusual` | **`8005`** | [http://127.0.0.1:8005/docs](http://127.0.0.1:8005/docs) | Identifica signos desbalanceados, secuencias o apóstrofes dobles. |
| 7 | **Verbos Modales** | `deteccion_verbos_modales` | **`8006`** | [http://127.0.0.1:8006/docs](http://127.0.0.1:8006/docs) | Detecta inconsistencias en el uso de verbos modales. |
| 8 | **Detector de Adverbios** | `detector_adverbios` | **`8007`** | [http://127.0.0.1:8007/docs](http://127.0.0.1:8007/docs) | Detecta y categoriza adverbios (modo, tiempo, frecuencia, etc.). |
| 9 | **Métricas de Legibilidad** | `metricas-de-legibilidad` | **`8008`** | [http://127.0.0.1:8008/docs](http://127.0.0.1:8008/docs) | Calcula métricas de complejidad lectora (Gunning Fog Extendido). |
| 10 | **Oraciones Impersonales** | `oraciones-impersonales` | **`8009`** | [http://127.0.0.1:8009/docs](http://127.0.0.1:8009/docs) | Clasifica oraciones personales, impersonales y ambiguas. |
| 11 | **Verbos Percepción / Opinión** | `verbos_percepcion_opinion` | **`8010`** | [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs) | Extrae verbos de percepción, opinión y pensamiento. |
| 12 | **Voz Pasiva** | `voz_pasiva` | **`8011`** | [http://127.0.0.1:8011/docs](http://127.0.0.1:8011/docs) | Detecta oraciones en voz pasiva y sus posiciones. |
| 13 | **Verbos Débiles (Weak Verbs)** | `weak_verbs` | **`8012`** | [http://127.0.0.1:8012/docs](http://127.0.0.1:8012/docs) | Detecta verbos débiles (make, do, have, get, etc.). |
| 14 | **Palabras Abstractas** | `abstract_words` | **`8013`** | [http://127.0.0.1:8013/docs](http://127.0.0.1:8013/docs) | Estima el grado de abstracción léxica con modelos entrenados. |
| 15 | *(Opcional)* **Web Documentación** | `WebDocumentacion` | **`5173`** | [http://localhost:5173](http://localhost:5173) | Portal interactivo en React + Vite con la documentación del proyecto. |

---

### 🚀 Instalación Rápida Automática (Recomendada)

Para configurar todo el proyecto en una sola orden en cualquier computadora con Windows (detecta Python, crea el entorno virtual, instala dependencias, descarga los modelos de spaCy y SBERT, y aplica migraciones):

**Opción A (PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File .\instalar_entorno.ps1
```

**Opción B (Doble clic en Windows):**
Simplemente haz doble clic sobre el archivo **`instalar_entorno.bat`**.

---

### 🛠️ Instalación Manual Paso a Paso

Si prefieres realizar el proceso manualmente:

#### 1. Requisitos Previos
- **Python:** 3.10, 3.11 o 3.12 (64-bit recomendado).
- **Node.js:** (opcional, solo necesario para ejecutar `WebDocumentacion`).

#### 2. Creación y Activación del Entorno Virtual

En PowerShell:
```powershell
# Crear entorno virtual (si aún no existe)
python -m venv entorno

# Activar el entorno virtual
.\entorno\Scripts\Activate.ps1
```

#### 3. Instalación de Dependencias

Se consolidaron todas las dependencias de todos los microservicios en el archivo `requirements.txt` de la raíz:

```powershell
pip install -r requirements.txt
```

#### 4. Descarga de Modelos de spaCy

Los servicios requieren los modelos de idioma en inglés de spaCy:

```powershell
# Modelo liviano (usado por la mayoría de los microservicios)
python -m spacy download en_core_web_sm

# Modelo Transformer basado en RoBERTa (requerido por doble negación y adverbios)
python -m spacy download en_core_web_trf
```

---

## 🚀 Orquestador de Servicios (PowerShell)

Para evitar tener que abrir 14 consolas individuales y recordar los puertos de cada servicio, dispones de scripts automatizados:

- `start_services.ps1`
- `iniciar_servicios.ps1` (alias en español)

### 1. Levantar todos los servicios
```powershell
.\start_services.ps1
# O bien:
.\iniciar_servicios.ps1
```

**¿Qué hace el script?**
1. Detecta automáticamente el intérprete de Python (entorno virtual activo o local `.\entorno`).
2. Verifica si los puertos están ocupados.
3. Inicia cada servicio en segundo plano sin generar ventanas intrusivas.
4. Redirige la salida y errores de cada servicio a `.logs/<id_servicio>.log`.
5. Muestra una tabla en consola con el nombre del servicio, puerto, estado (`ACTIVO` / `DETENIDO`), PID y enlace a la documentación interactiva Swagger.

> **Tip:** Para levantar además la documentación web de React/Vite, añade el flag `-IncludeWebDoc`:
> ```powershell
> .\start_services.ps1 -IncludeWebDoc
> ```

### 2. Consultar el estado de los servicios
Muestra la tabla del estado actual de todos los puertos sin reiniciar ningún proceso:
```powershell
.\start_services.ps1 -Status
```

### 3. Detener todos los servicios
Finaliza todos los procesos en segundo plano y libera los puertos asignados:
```powershell
.\start_services.ps1 -Stop
```

### 4. Registros y Diagnóstico
Si algún servicio presenta un error al iniciar, puedes consultar sus registros en:
```text
.logs/<nombre_servicio>.log
.logs/<nombre_servicio>_err.log
```

---

## 🛠️ Ejecución Individual Manual

Si prefieres ejecutar un servicio específico de manera aislada en una terminal interactiva:

```powershell
# Activar entorno
.\entorno\Scripts\Activate.ps1

# Ejemplo: Conectores Lógicos
cd deteccion_conectores_logicos
uvicorn main:app --reload --port 8003

# Ejemplo: Voz Pasiva
cd ..\voz_pasiva
uvicorn main:app --reload --port 8011

# Ejemplo: Portal Django AppWeb
cd ..\AppWeb
python manage.py runserver 127.0.0.1:8000
```

---

## 🔍 Resolución de Incompatibilidades en `requirements.txt`

Durante la consolidación de dependencias de todos los servicios se identificaron y resolvieron los siguientes conflictos:

1. **`spacy`**:
   - `detector_adverbios` fijaba `spacy==3.8.14`.
   - `voz_pasiva` fijaba `spacy==3.8.16`.
   - `servicio-deteccion-cliches` y `repeticion-palabras` exigían `spacy>=3.5.0,<4.0.0`.
   - **Solución:** Se definió `spacy>=3.8.14,<4.0.0`, compatible con todos los módulos y pipelines 3.8.x.

2. **`fastapi` y `pydantic`**:
   - `detector_adverbios` fijaba `fastapi==0.111.0` y `pydantic==2.6.1`.
   - `voz_pasiva` fijaba `fastapi==0.141.1` y `pydantic==2.13.5`.
   - Otros servicios requerían `fastapi>=0.111.0` y `pydantic>=2.0.0`.
   - **Solución:** Se unificó en `fastapi>=0.111.0` y `pydantic>=2.6.1,<3.0.0`, garantizando total interoperabilidad con Pydantic V2.

3. **`uvicorn`**:
   - `detector_adverbios` fijaba `uvicorn[standard]==0.27.0`.
   - `deteccion_conectores_logicos` requería `uvicorn[standard]>=0.29.0`.
   - **Solución:** Se unificó en `uvicorn[standard]>=0.29.0`.

4. **`numpy` y `textdescriptives`**:
   - `textdescriptives>=2.0.0` exige obligatoriamente `numpy<2.0.0,>=1.20.0`.
   - Si se instala NumPy 2.x, `textdescriptives` falla.
   - **Solución:** Se fijó `numpy>=1.20.0,<2.0.0` (ej. `numpy 1.26.4`), permitiendo que funcionen juntos `textdescriptives`, `spacy`, `scikit-learn`, `gensim` y `xgboost`.

5. **`spacy-transformers`**:
   - Los servicios `detector_adverbios` y `detector_doble_negacion` utilizan el modelo `en_core_web_trf`.
   - Se añadió explícitamente `spacy-transformers>=1.4.0` en la raíz para permitir el funcionamiento de los modelos Transformer.

---

## 📁 Estructura del Proyecto

```text
.
├── requirements.txt               # Dependencias consolidadas y compatibles de todo el repositorio
├── start_services.ps1             # Script orquestador para iniciar, pausar y monitorear servicios
├── iniciar_servicios.ps1           # Alias en español para start_services.ps1
├── README.md                      # Documentación general del repositorio
├── .logs/                         # Registros generados por los servicios en ejecución
│
├── AppWeb/                        # Aplicación web completa en Django (Frontend / Portal)
├── abstract_words/                # Servicio de detección de palabras abstractas
├── deteccion_conectores_logicos/  # Microservicio de detección de conectores lógicos
├── deteccion_puntuacion_inusual/  # Microservicio de detección de puntuación inusual
├── deteccion_verbos_modales/      # Microservicio de inconsistencias de verbos modales
├── detector_adverbios/            # Microservicio clasificador de adverbios
├── detector_doble_negacion/       # Microservicio de detección de doble negación
├── metricas-de-legibilidad/       # Microservicio de cálculo de legibilidad (Gunning Fog)
├── oraciones-impersonales/        # Microservicio clasificador de oraciones impersonales
├── servicio-deteccion-cliches/    # Microservicio detector de clichés (spaCy + SBERT)
├── servicio-repeticion-palabras/  # Microservicio detector de palabras repetidas
├── verbos_percepcion_opinion/     # Microservicio de verbos de percepción y opinión
├── voz_pasiva/                    # Microservicio detector de construcciones en voz pasiva
├── weak_verbs/                    # Microservicio detector de verbos débiles
└── WebDocumentacion/              # Portal de documentación en Vite + React + TypeScript
```
