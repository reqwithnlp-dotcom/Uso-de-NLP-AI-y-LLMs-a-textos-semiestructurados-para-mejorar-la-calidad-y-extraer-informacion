#!/usr/bin/env bash
# ==============================================================================
# Script: instalar_entorno.sh
# Descripción: Script de instalación y configuración automática del entorno
#              para servidor Linux Ubuntu.
# Repositorio: Uso de NLP, AI y LLMs a textos semiestructurados
# ==============================================================================

set -uo pipefail

# ------------------------------------------------------------------------------
# Configuración de Rutas
# ------------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$SCRIPT_DIR/entorno"
VENV_PYTHON="$VENV_DIR/bin/python"
REQ_FILE="$SCRIPT_DIR/requirements.txt"

# ------------------------------------------------------------------------------
# Paleta de Colores ANSI
# ------------------------------------------------------------------------------
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_CYAN="\033[0;36m"
C_GREEN="\033[0;32m"
C_YELLOW="\033[1;33m"
C_RED="\033[0;31m"
C_GRAY="\033[0;90m"

# ------------------------------------------------------------------------------
# Opciones de Ejecución
# ------------------------------------------------------------------------------
RECREATE_VENV=false
START_SERVICES=false

for arg in "$@"; do
    case "$arg" in
        --recreate-venv|-r)
            RECREATE_VENV=true
            ;;
        --start-services|-s)
            START_SERVICES=true
            ;;
        --help|-h)
            echo -e "${C_CYAN}Uso:${C_RESET} ./instalar_entorno.sh [OPCIONES]"
            echo ""
            echo "Opciones:"
            echo "  --recreate-venv, -r    Elimina el entorno virtual previo y lo crea desde cero"
            echo "  --start-services, -s   Inicia todos los servicios automáticamente al finalizar"
            echo "  --help, -h             Muestra esta ayuda"
            exit 0
            ;;
        *)
            echo -e "${C_YELLOW}[!] Argumento no reconocido: $arg${C_RESET}"
            ;;
    esac
done

write_section() {
    echo -e "\n${C_CYAN}==========================================================================================${C_RESET}"
    echo -e "${C_CYAN}  $1${C_RESET}"
    echo -e "${C_CYAN}==========================================================================================${C_RESET}"
}

write_success() {
    echo -e "  ${C_GREEN}[OK] $1${C_RESET}"
}

write_warning() {
    echo -e "  ${C_YELLOW}[!] $1${C_RESET}"
}

write_error() {
    echo -e "  ${C_RED}[ERROR] $1${C_RESET}"
}

# =============================================================================
# PASO 1: DETECCIÓN DE PYTHON BASE EN UBUNTU
# =============================================================================
write_section "PASO 1: Verificando instalación de Python en el sistema Linux (Ubuntu)"

BASE_PYTHON=""
if command -v python3 >/dev/null 2>&1; then
    BASE_PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
    BASE_PYTHON="$(command -v python)"
fi

if [ -z "$BASE_PYTHON" ]; then
    write_error "No se encontró Python instalado en este servidor Ubuntu."
    echo -e "\nPuedes instalarlo ejecutando:"
    echo -e "  ${C_BOLD}sudo apt update && sudo apt install -y python3 python3-venv python3-pip python3-dev build-essential${C_RESET}\n"
    exit 1
fi

PY_VER="$("$BASE_PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')" 2>/dev/null || echo "Desconocida")"
write_success "Python base detectado: $BASE_PYTHON (Versión: $PY_VER)"

# Verificar si el módulo 'venv' de Python está instalado (paquete python3-venv en Ubuntu)
if ! "$BASE_PYTHON" -m venv --help >/dev/null 2>&1; then
    write_error "El módulo venv de Python no está disponible."
    echo -e "\nEn Ubuntu debes instalar el paquete correspondiente ejecutando:"
    echo -e "  ${C_BOLD}sudo apt update && sudo apt install -y python3-venv python3-dev build-essential${C_RESET}\n"
    exit 1
fi

# =============================================================================
# PASO 2: CREACIÓN O VALIDACIÓN DEL ENTORNO VIRTUAL
# =============================================================================
write_section "PASO 2: Preparando entorno virtual ('entorno')"

if [ "$RECREATE_VENV" = true ] && [ -d "$VENV_DIR" ]; then
    echo -e "  -> Eliminando entorno existente por parámetro --recreate-venv..."
    rm -rf "$VENV_DIR"
fi

if [ ! -x "$VENV_PYTHON" ]; then
    echo -e "  -> Creando nuevo entorno virtual en: $VENV_DIR ..."
    "$BASE_PYTHON" -m venv "$VENV_DIR"

    if [ ! -x "$VENV_PYTHON" ]; then
        write_error "No se pudo crear el entorno virtual. Verifica permisos en el directorio."
        exit 1
    fi
    write_success "Entorno virtual creado exitosamente."
else
    write_success "Entorno virtual existente encontrado en: $VENV_DIR"
fi

# =============================================================================
# PASO 3: ACTUALIZACIÓN DE PIP, SETUPTOOLS Y WHEEL
# =============================================================================
write_section "PASO 3: Actualizando pip, setuptools y wheel"
echo -e "  -> Actualizando gestor de paquetes pip..."
"$VENV_PYTHON" -m pip install --upgrade pip setuptools wheel --quiet
write_success "Gestor de paquetes pip actualizado."

# =============================================================================
# PASO 4: INSTALACIÓN DE DEPENDENCIAS (requirements.txt)
# =============================================================================
write_section "PASO 4: Instalando dependencias del proyecto (requirements.txt)"

if [ ! -f "$REQ_FILE" ]; then
    write_error "No se encontró el archivo requirements.txt en: $REQ_FILE"
    exit 1
fi

echo -e "  -> Instalando librerías (FastAPI, spaCy, PyTorch, Transformers, Scikit-Learn, Django, etc.)..."
echo -e "     (Esto puede tardar unos minutos dependiendo de la conexión a internet)..."

if ! "$VENV_PYTHON" -m pip install --no-input --disable-pip-version-check -r "$REQ_FILE"; then
    write_error "Hubo un error al instalar los paquetes de requirements.txt."
    echo -e "\nAsegúrate de tener herramientas de compilación en Ubuntu:"
    echo -e "  ${C_BOLD}sudo apt update && sudo apt install -y build-essential python3-dev libffi-dev libssl-dev${C_RESET}\n"
    exit 1
fi
write_success "Todas las dependencias de requirements.txt han sido instaladas."

# =============================================================================
# PASO 5: DESCARGA DE MODELOS DE SPACY
# =============================================================================
write_section "PASO 5: Descargando modelos de lenguaje de spaCy"

echo -e "  -> Descargando modelo spaCy ligero: en_core_web_sm..."
if "$VENV_PYTHON" -m spacy download en_core_web_sm; then
    write_success "Modelo 'en_core_web_sm' instalado correctamente."
else
    write_error "Falló la descarga de 'en_core_web_sm'."
fi

echo -e "\n  -> Descargando modelo spaCy basado en Transformers: en_core_web_trf..."
if "$VENV_PYTHON" -m spacy download en_core_web_trf; then
    write_success "Modelo 'en_core_web_trf' instalado correctamente."
else
    write_error "Falló la descarga de 'en_core_web_trf'."
fi

echo -e "\n  -> Descargando modelo spaCy mediano: en_core_web_md..."
if "$VENV_PYTHON" -m spacy download en_core_web_md; then
    write_success "Modelo 'en_core_web_md' instalado correctamente."
else
    write_error "Falló la descarga de 'en_core_web_md'."
fi

# =============================================================================
# PASO 6: PRE-DESCARGA DEL MODELO SBERT (SENTENCE TRANSFORMERS)
# =============================================================================
write_section "PASO 6: Descargando y guardando en caché el modelo SBERT"

echo -e "  -> Descargando 'paraphrase-MiniLM-L6-v2' para detección de clichés..."
"$VENV_PYTHON" -c "
try:
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    print('OK_SBERT')
except Exception as e:
    print(f'ERROR: {e}')
" || true

write_success "Modelo Sentence-Transformers precargado en caché local."

# =============================================================================
# PASO 7: ENTRENAMIENTO DEL MODELO DE PALABRAS ABSTRACTAS (ABSTRACT_WORDS)
# =============================================================================
write_section "PASO 7: Verificando modelo de clasificación de palabras abstractas"

ABSTRACT_MODEL="$SCRIPT_DIR/abstract_words/models/spacy_rf.joblib"
ABSTRACT_DATASET="$SCRIPT_DIR/abstract_words/datasets/Concreteness_ratings_Brysbaert_et_al_BRM.txt"
ABSTRACT_DIR="$SCRIPT_DIR/abstract_words"

if [ ! -f "$ABSTRACT_MODEL" ]; then
    if [ -f "$ABSTRACT_DATASET" ]; then
        echo -e "  -> Entrenando modelo (spaCy + Random Forest) a partir del dataset de concreción..."
        echo -e "     (Esto toma aproximadamente 1 a 2 minutos en una instalación limpia)..."
        (
            cd "$ABSTRACT_DIR" || exit 1
            if [ ! -f "datasets/train.csv" ]; then
                "$VENV_PYTHON" split_dataset.py
            fi
            "$VENV_PYTHON" train_model.py
        )
        if [ -f "$ABSTRACT_MODEL" ]; then
            write_success "Modelo de palabras abstractas entrenado y guardado correctamente."
        else
            write_warning "No se pudo generar 'spacy_rf.joblib'. El servicio usará el estimador de contingencia."
        fi
    else
        write_warning "Dataset de concreción no encontrado. El servicio usará modelo de contingencia."
    fi
else
    write_success "Modelo 'spacy_rf.joblib' listo (detectado en abstract_words/models)."
fi

# =============================================================================
# PASO 8: MIGRACIONES DE BASE DE DATOS DJANGO (APPWEB)
# =============================================================================
write_section "PASO 8: Inicializando base de datos Django (AppWeb)"

APPWEB_DIR="$SCRIPT_DIR/AppWeb"
if [ -f "$APPWEB_DIR/manage.py" ]; then
    echo -e "  -> Aplicando migraciones de SQLite..."
    (
        cd "$APPWEB_DIR" || exit 1
        "$VENV_PYTHON" manage.py migrate --noinput
    )
    write_success "Base de datos de Django inicializada."
fi

# =============================================================================
# PASO 9: COMPROBACIÓN DE INTEGRIDAD DE TODOS LOS MICROSERVICIOS
# =============================================================================
write_section "PASO 9: Comprobando que todos los microservicios inicializan bien"

SERVICES_CHECKS=(
    "servicio-deteccion-cliches:main"
    "servicio-repeticion-palabras:main"
    "deteccion_conectores_logicos:main"
    "detector_doble_negacion:main"
    "deteccion_puntuacion_inusual:main"
    "deteccion_verbos_modales:main"
    "detector_adverbios:main"
    "metricas-de-legibilidad:main"
    "oraciones-impersonales:main"
    "verbos_percepcion_opinion:app.main"
    "weak_verbs:app.main"
    "voz_pasiva:main"
    "abstract_words:api"
    "povshift:main"
    "verb_tense_inconsistencies:api"
)

ALL_PASSED=true
for item in "${SERVICES_CHECKS[@]}"; do
    svc_dir="${item%%:*}"
    svc_mod="${item##*:}"
    full_path="$SCRIPT_DIR/$svc_dir"

    if [ ! -d "$full_path" ]; then
        write_warning "$svc_dir no encontrado."
        continue
    fi

    res="$(cd "$full_path" && "$VENV_PYTHON" -c "import $svc_mod; print('IMPORT_OK')" 2>&1 || true)"
    if echo "$res" | grep -q "IMPORT_OK"; then
        write_success "$svc_dir"
    else
        ALL_PASSED=false
        write_error "Fallo al inicializar $svc_dir: $res"
    fi
done

# =============================================================================
# RESUMEN FINAL
# =============================================================================
write_section "INSTALACIÓN COMPLETADA"

# Dar permisos de ejecución a los scripts creados
chmod +x "$SCRIPT_DIR/start_services.sh" "$SCRIPT_DIR/iniciar_servicios.sh" "$SCRIPT_DIR/instalar_entorno.sh" 2>/dev/null || true

if [ "$ALL_PASSED" = true ]; then
    echo -e "\n  ${C_GREEN}${C_BOLD}¡EL ENTORNO HA SIDO CONFIGURADO EXITOSAMENTE EN UBUNTU LINUX!${C_RESET}"
    echo -e "\n  Para levantar todos los servicios en 0.0.0.0, ejecuta:"
    echo -e "    ${C_YELLOW}./iniciar_servicios.sh${C_RESET}\n"
    echo -e "  Para verificar el estado de los puertos y servicios:"
    echo -e "    ${C_YELLOW}./iniciar_servicios.sh --status${C_RESET}\n"
    echo -e "  Para detener los servicios:"
    echo -e "    ${C_YELLOW}./iniciar_servicios.sh --stop${C_RESET}\n"

    if [ "$START_SERVICES" = true ]; then
        echo -e "  ${C_CYAN}-> Parámetro --start-services detectado. Levantando servicios...${C_RESET}"
        exec "$SCRIPT_DIR/start_services.sh"
    fi
else
    echo -e "\n  ${C_YELLOW}Algunos microservicios presentaron advertencias. Revisa los mensajes anteriores.${C_RESET}"
fi
