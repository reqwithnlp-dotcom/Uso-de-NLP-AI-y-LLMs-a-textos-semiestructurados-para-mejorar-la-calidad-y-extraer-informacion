#!/usr/bin/env bash
# ==============================================================================
# Script: start_services.sh
# Descripción: Orquestador para iniciar, detener y monitorear todos los
#              microservicios y aplicaciones en un servidor Linux (Ubuntu).
# Configuración: Todos los servicios enlazados a 0.0.0.0
# ==============================================================================

set -uo pipefail

# ------------------------------------------------------------------------------
# Configuración de Rutas y Archivos
# ------------------------------------------------------------------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOGS_DIR="$SCRIPT_DIR/logs"
HIDDEN_LOGS_DIR="$SCRIPT_DIR/.logs"
STATE_FILE="$SCRIPT_DIR/.services_state.json"

# Asegurar que el directorio de logs sea visible con 'ls' y mantener compatibilidad con .logs
mkdir -p "$LOGS_DIR"
ln -sfn "$LOGS_DIR" "$HIDDEN_LOGS_DIR" 2>/dev/null || true

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
C_BLUE="\033[0;34m"

# ------------------------------------------------------------------------------
# Opciones de Ejecución
# ------------------------------------------------------------------------------
OPT_STOP=false
OPT_STATUS=false
OPT_INCLUDE_WEBDOC=false

for arg in "$@"; do
    case "$arg" in
        --stop|-stop|-s|stop)
            OPT_STOP=true
            ;;
        --status|-status|status)
            OPT_STATUS=true
            ;;
        --include-webdoc|-include-webdoc|-webdoc)
            OPT_INCLUDE_WEBDOC=true
            ;;
        --help|-h|help)
            echo -e "${C_CYAN}Uso:${C_RESET} ./start_services.sh [OPCIONES]"
            echo ""
            echo "Opciones:"
            echo "  (sin args)          Inicia todos los servicios en segundo plano (0.0.0.0)"
            echo "  --status, status    Muestra el estado actual de cada servicio y puerto"
            echo "  --stop, stop        Detiene todos los servicios y libera los puertos"
            echo "  --include-webdoc    Incluye el servidor frontend Vite de WebDocumentacion"
            echo "  --help, -h          Muestra este mensaje de ayuda"
            exit 0
            ;;
        *)
            echo -e "${C_YELLOW}[!] Argumento no reconocido: $arg${C_RESET}"
            ;;
    esac
done

# ------------------------------------------------------------------------------
# Definición de Microservicios (Formato: ID|NOMBRE|DIR|TIPO|PORT|URL_DOCS|ARGS)
# Todos los servicios configurados en 0.0.0.0
# ------------------------------------------------------------------------------
SERVICES_DEF=(
    "appweb|AppWeb (Portal Django)|AppWeb|django|8000|http://0.0.0.0:8000|manage.py runserver 0.0.0.0:8000 --noreload"
    "cliches|Deteccion de Cliches|servicio-deteccion-cliches|uvicorn|8001|http://0.0.0.0:8001/docs|-m uvicorn main:app --host 0.0.0.0 --port 8001"
    "repeticion|Repeticion de Palabras|servicio-repeticion-palabras|uvicorn|8002|http://0.0.0.0:8002/docs|-m uvicorn main:app --host 0.0.0.0 --port 8002"
    "conectores_logicos|Conectores Logicos|deteccion_conectores_logicos|uvicorn|8003|http://0.0.0.0:8003/docs|-m uvicorn main:app --host 0.0.0.0 --port 8003"
    "doble_negacion|Doble Negacion|detector_doble_negacion|uvicorn|8004|http://0.0.0.0:8004/docs|-m uvicorn main:app --host 0.0.0.0 --port 8004"
    "puntuacion_inusual|Puntuacion Inusual|deteccion_puntuacion_inusual|uvicorn|8005|http://0.0.0.0:8005/docs|-m uvicorn main:app --host 0.0.0.0 --port 8005"
    "verbos_modales|Verbos Modales|deteccion_verbos_modales|uvicorn|8006|http://0.0.0.0:8006/docs|-m uvicorn main:app --host 0.0.0.0 --port 8006"
    "detector_adverbios|Detector de Adverbios|detector_adverbios|uvicorn|8007|http://0.0.0.0:8007/docs|-m uvicorn main:app --host 0.0.0.0 --port 8007"
    "metricas_legibilidad|Metricas de Legibilidad|metricas-de-legibilidad|uvicorn|8008|http://0.0.0.0:8008/docs|-m uvicorn main:app --host 0.0.0.0 --port 8008"
    "oraciones_impersonales|Oraciones Impersonales|oraciones-impersonales|uvicorn|8009|http://0.0.0.0:8009/docs|-m uvicorn main:app --host 0.0.0.0 --port 8009"
    "verbos_percepcion_opinion|Verbos Percepcion / Opinion|verbos_percepcion_opinion|uvicorn|8010|http://0.0.0.0:8010/docs|-m uvicorn app.main:app --host 0.0.0.0 --port 8010"
    "voz_pasiva|Voz Pasiva|voz_pasiva|uvicorn|8011|http://0.0.0.0:8011/docs|-m uvicorn main:app --host 0.0.0.0 --port 8011"
    "weak_verbs|Verbos Debiles (Weak Verbs)|weak_verbs|uvicorn|8012|http://0.0.0.0:8012/docs|-m uvicorn app.main:app --host 0.0.0.0 --port 8012"
    "abstract_words|Palabras Abstractas|abstract_words|uvicorn|8013|http://0.0.0.0:8013/docs|-m uvicorn api:app --host 0.0.0.0 --port 8013"
    "povshift|Cambio Punto de Vista (POV Shift)|povshift|uvicorn|8014|http://0.0.0.0:8014/docs|-m uvicorn main:app --host 0.0.0.0 --port 8014"
    "verb_tense_inconsistencies|Inconsistencias Tiempos Verbales|verb_tense_inconsistencies|uvicorn|8015|http://0.0.0.0:8015/docs|-m uvicorn api:app --host 0.0.0.0 --port 8015"
)

if [ "$OPT_INCLUDE_WEBDOC" = true ]; then
    SERVICES_DEF+=("web_documentacion|Web Documentacion (Vite/React)|WebDocumentacion|npm|5173|http://0.0.0.0:5173|run dev -- --host 0.0.0.0 --port 5173")
fi

# ------------------------------------------------------------------------------
# Funciones Auxiliares
# ------------------------------------------------------------------------------

# Detectar intérprete de Python funcional (priorizando el entorno virtual)
find_python_executable() {
    # 1. Entorno virtual activo en shell
    if [ -n "${VIRTUAL_ENV:-}" ] && [ -x "$VIRTUAL_ENV/bin/python" ]; then
        echo "$VIRTUAL_ENV/bin/python"
        return 0
    fi

    # 2. Entorno virtual estándar del repo 'entorno'
    if [ -x "$SCRIPT_DIR/entorno/bin/python" ]; then
        echo "$SCRIPT_DIR/entorno/bin/python"
        return 0
    fi

    # 3. Otros entornos virtuales comunes (.venv, venv)
    for v in ".venv" "venv"; do
        if [ -x "$SCRIPT_DIR/$v/bin/python" ]; then
            echo "$SCRIPT_DIR/$v/bin/python"
            return 0
        fi
    done

    # 4. python3 en PATH del sistema
    if command -v python3 >/dev/null 2>&1; then
        command -v python3
        return 0
    fi

    if command -v python >/dev/null 2>&1; then
        command -v python
        return 0
    fi

    return 1
}

# Obtener el PID del proceso escuchando en un puerto dado
get_port_process_id() {
    local port="$1"
    local pid=""

    if command -v lsof >/dev/null 2>&1; then
        pid=$(lsof -ti ":$port" -sTCP:LISTEN 2>/dev/null | head -n 1 || true)
    fi

    if [ -z "$pid" ] && command -v fuser >/dev/null 2>&1; then
        pid=$(fuser "$port/tcp" 2>/dev/null | tr -s ' ' '\n' | grep -v '^$' | head -n 1 || true)
    fi

    if [ -z "$pid" ] && command -v ss >/dev/null 2>&1; then
        pid=$(ss -lptn "sport = :$port" 2>/dev/null | grep -o 'pid=[0-9]*' | head -n 1 | cut -d= -f2 || true)
    fi

    if [ -z "$pid" ] && command -v netstat >/dev/null 2>&1; then
        pid=$(netstat -tulpn 2>/dev/null | grep -E ":${port}\s+" | awk '{print $7}' | cut -d/ -f1 | head -n 1 || true)
    fi

    echo "$pid"
}

# Detener todos los servicios activos
stop_all_services() {
    echo -e "\n${C_YELLOW}=================================================================${C_RESET}"
    echo -e "${C_YELLOW}                DETENIENDO SERVICIOS ACTIVOS                     ${C_RESET}"
    echo -e "${C_YELLOW}=================================================================\n${C_RESET}"

    # Detener por archivo de estado previo si existe
    if [ -f "$STATE_FILE" ]; then
        while IFS="|" read -r id name port pid url; do
            if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
                echo -e "  -> Deteniendo proceso ${C_BOLD}$name${C_RESET} (PID $pid)..."
                kill "$pid" 2>/dev/null || true
                sleep 0.2
                if kill -0 "$pid" 2>/dev/null; then
                    kill -9 "$pid" 2>/dev/null || true
                fi
            fi
        done < <(python3 -c "
import json, sys
try:
    with open('$STATE_FILE') as f:
        data = json.load(f)
        for item in data:
            print(f\"{item.get('Id','')}|{item.get('Name','')}|{item.get('Port','')}|{item.get('PID','')}|{item.get('Url','')}\")
except Exception:
    pass
" 2>/dev/null || true)
        rm -f "$STATE_FILE" 2>/dev/null || true
    fi

    # Asegurar liberación de puertos asignados
    for s_def in "${SERVICES_DEF[@]}"; do
        IFS="|" read -r s_id s_name s_dir s_type s_port s_url s_args <<< "$s_def"
        local p_pid
        p_pid="$(get_port_process_id "$s_port")"
        if [ -n "$p_pid" ]; then
            echo -e "  -> Liberando puerto $s_port (${C_BOLD}$s_name${C_RESET}, PID $p_pid)..."
            kill "$p_pid" 2>/dev/null || true
            sleep 0.2
            if kill -0 "$p_pid" 2>/dev/null; then
                kill -9 "$p_pid" 2>/dev/null || true
            fi
        fi
    done

    echo -e "\n${C_GREEN}[OK] Todos los servicios han sido detenidos y los puertos liberados.${C_RESET}\n"
}

# Mostrar tabla de estado detallada
show_status_table() {
    echo -e "\n${C_CYAN}======================================================================================================${C_RESET}"
    echo -e "${C_CYAN}                               ESTADO DE LOS SERVICIOS (0.0.0.0)                                      ${C_RESET}"
    echo -e "${C_CYAN}======================================================================================================${C_RESET}"

    printf "${C_BOLD}%-35s %-8s %-14s %-8s %-32s${C_RESET}\n" "Servicio" "Puerto" "Estado" "PID" "URL / Documentacion"
    echo "------------------------------------------------------------------------------------------------------"

    for s_def in "${SERVICES_DEF[@]}"; do
        IFS="|" read -r s_id s_name s_dir s_type s_port s_url s_args <<< "$s_def"

        local p_pid status status_color
        p_pid="$(get_port_process_id "$s_port")"

        if [ -n "$p_pid" ]; then
            status="ACTIVO"
            status_color="$C_GREEN"
        else
            status="DETENIDO"
            status_color="$C_RED"
            p_pid="-"
        fi

        printf "%-35s %-8s ${status_color}%-14s${C_RESET} %-8s %-32s\n" \
            "$s_name" "$s_port" "$status" "$p_pid" "$s_url"
    done
    echo "------------------------------------------------------------------------------------------------------"
    echo ""

    # Inspeccionar errores de servicios caídos
    local stopped_count=0
    local error_lines=()
    for s_def in "${SERVICES_DEF[@]}"; do
        IFS="|" read -r s_id s_name s_dir s_type s_port s_url s_args <<< "$s_def"
        local p_pid
        p_pid="$(get_port_process_id "$s_port")"
        if [ -z "$p_pid" ]; then
            stopped_count=$((stopped_count + 1))
            local err_f="$LOGS_DIR/${s_id}_err.log"
            if [ -f "$err_f" ] && [ -s "$err_f" ]; then
                local last_line
                last_line="$(grep -v '^$' "$err_f" | tail -n 1 | tr -d '\r')"
                if [ -n "$last_line" ]; then
                    error_lines+=("  -> ${C_BOLD}$s_name${C_RESET} (puerto $s_port): $last_line")
                fi
            fi
        fi
    done

    if [ "$stopped_count" -gt 0 ]; then
        echo -e "${C_YELLOW}[!] ATENCIÓN: Hay $stopped_count servicio(s) detenido(s).${C_RESET}"
        if [ "${#error_lines[@]}" -gt 0 ]; then
            echo -e "${C_RED}Último error registrado en logs/ de los servicios caídos:${C_RESET}"
            for err_msg in "${error_lines[@]}"; do
                echo -e "$err_msg"
            done
            echo ""
        fi
        echo -e "${C_CYAN}Causa más frecuente en servidores nuevos:${C_RESET}"
        echo -e "  Faltan modelos NLP de spaCy (en_core_web_sm, etc.) o dependencias en el entorno virtual."
        echo -e "  Ejecuta el script de instalación automática para solucionarlo:"
        echo -e "    ${C_YELLOW}${C_BOLD}./instalar_entorno.sh${C_RESET}\n"
    fi
}

# ------------------------------------------------------------------------------
# Ejecutar acciones: Stop o Status
# ------------------------------------------------------------------------------
if [ "$OPT_STOP" = true ]; then
    stop_all_services
    exit 0
fi

if [ "$OPT_STATUS" = true ]; then
    show_status_table
    exit 0
fi

# ------------------------------------------------------------------------------
# Inicialización y Detección de Entorno
# ------------------------------------------------------------------------------
echo -e "${C_CYAN}======================================================================================================${C_RESET}"
echo -e "${C_CYAN}                   LEVANTANDO TODOS LOS SERVICIOS (NLP & LLMs) EN LINUX                              ${C_RESET}"
echo -e "${C_CYAN}======================================================================================================${C_RESET}"

PYTHON_EXE="$(find_python_executable || true)"

if [ -z "$PYTHON_EXE" ]; then
    echo -e "\n${C_RED}[ERROR] No se encontró un intérprete de Python válido.${C_RESET}"
    echo -e "${C_YELLOW}Ejecuta primero ./instalar_entorno.sh para configurar el entorno virtual.${C_RESET}\n"
    exit 1
fi

echo -e "\n${C_GRAY}Intérprete de Python detectado:${C_RESET}"
echo -e "  ${C_CYAN}$PYTHON_EXE${C_RESET}\n"

# Verificación de librerías esenciales
CHECK_FASTAPI="$("$PYTHON_EXE" -c "import fastapi, uvicorn; print('OK')" 2>/dev/null || true)"
if [ "$CHECK_FASTAPI" != "OK" ]; then
    echo -e "${C_YELLOW}[!] ADVERTENCIA: 'fastapi' o 'uvicorn' no están instalados en este entorno.${C_RESET}"
    echo -e "${C_YELLOW}    Para instalar dependencias, ejecuta primero: ./instalar_entorno.sh${C_RESET}\n"
fi

# Verificación de spaCy y modelos
CHECK_SPACY="$("$PYTHON_EXE" -c "
try:
    import spacy
    import importlib.util
    sm = bool(importlib.util.find_spec('en_core_web_sm'))
    trf = bool(importlib.util.find_spec('en_core_web_trf'))
    md = bool(importlib.util.find_spec('en_core_web_md'))
    print(f'OK:{sm},{trf},{md}')
except ImportError as e:
    print(f'MISSING:{e}')
except Exception as e:
    print(f'ERROR:{e}')
" 2>/dev/null || echo "EXEC_FAIL")"

if [[ "$CHECK_SPACY" == MISSING* ]]; then
    echo -e "${C_RED}[!] ADVERTENCIA: Falta spaCy u otra librería NLP (${CHECK_SPACY#MISSING:}).${C_RESET}"
    echo -e "${C_YELLOW}    Ejecuta ./instalar_entorno.sh para configurar todas las dependencias.${C_RESET}\n"
elif [[ "$CHECK_SPACY" == OK:* ]]; then
    SPACY_FLAGS="${CHECK_SPACY#OK:}"
    IFS="," read -r sm_ok trf_ok md_ok <<< "$SPACY_FLAGS"
    if [ "$sm_ok" != "True" ] || [ "$trf_ok" != "True" ] || [ "$md_ok" != "True" ]; then
        echo -e "${C_YELLOW}[!] ATENCIÓN: Se detectaron modelos de spaCy faltantes en este Python:${C_RESET}"
        [ "$sm_ok" != "True" ] && echo -e "    * Falta 'en_core_web_sm'"
        [ "$trf_ok" != "True" ] && echo -e "    * Falta 'en_core_web_trf'"
        [ "$md_ok" != "True" ] && echo -e "    * Falta 'en_core_web_md'"
        echo -e "${C_CYAN}    Los microservicios que usen estos modelos fallarán a menos que ejecutes:${C_RESET}"
        echo -e "    ${C_BOLD}./instalar_entorno.sh${C_RESET}\n"
    fi
fi

# Crear directorio de logs
mkdir -p "$LOGS_DIR"
ln -sfn "$LOGS_DIR" "$HIDDEN_LOGS_DIR" 2>/dev/null || true

# ------------------------------------------------------------------------------
# Lanzamiento de Servicios
# ------------------------------------------------------------------------------
STATE_JSON="["
FIRST_ITEM=true

for s_def in "${SERVICES_DEF[@]}"; do
    IFS="|" read -r s_id s_name s_dir s_type s_port s_url s_args <<< "$s_def"
    FULL_DIR="$SCRIPT_DIR/$s_dir"

    if [ ! -d "$FULL_DIR" ]; then
        echo -e "${C_YELLOW}[SALTADO] Carpeta no encontrada: $s_dir${C_RESET}"
        continue
    fi

    # Verificar si el puerto ya está ocupado mediante socket y liberar procesos zombies
    python3 -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(('0.0.0.0', int('$s_port')))
    s.close()
    sys.exit(0)
except OSError:
    sys.exit(1)
" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo -e "${C_YELLOW}[AVISO] Puerto $s_port ocupado. Liberando proceso previo para evitar Errno 98...${C_RESET}"
        command -v fuser >/dev/null 2>&1 && fuser -k -9 "${s_port}/tcp" 2>/dev/null || true
        command -v lsof >/dev/null 2>&1 && lsof -ti ":${s_port}" 2>/dev/null | xargs -r kill -9 2>/dev/null || true
        pkill -9 -f "uvicorn.*--port $s_port" 2>/dev/null || true
        sleep 0.3
    fi

    # Caso especial abstract_words: advertir si falta modelo
    if [ "$s_id" = "abstract_words" ]; then
        if [ ! -f "$FULL_DIR/models/spacy_rf.joblib" ]; then
            echo -e "${C_YELLOW}[AVISO] 'abstract_words': Requiere entrenar el modelo antes del primer uso (python train_model.py).${C_RESET}"
        fi
    fi

    LOG_OUT="$LOGS_DIR/${s_id}.log"
    LOG_ERR="$LOGS_DIR/${s_id}_err.log"

    EXEC_CMD=""
    if [ "$s_type" = "npm" ]; then
        if ! command -v npm >/dev/null 2>&1; then
            echo -e "${C_YELLOW}[AVISO] Node/npm no encontrado para $s_name.${C_RESET}"
            continue
        fi
        EXEC_CMD="npm $s_args"
    else
        EXEC_CMD="\"$PYTHON_EXE\" $s_args"
    fi

    # Iniciar proceso en background redirigiendo stdout y stderr
    (
        cd "$FULL_DIR" || exit 1
        eval nohup $EXEC_CMD > "$LOG_OUT" 2> "$LOG_ERR" < /dev/null &
        echo $! > "$LOGS_DIR/${s_id}.pid"
    )

    PROC_PID="$(cat "$LOGS_DIR/${s_id}.pid" 2>/dev/null || true)"

    [ "$FIRST_ITEM" = false ] && STATE_JSON+=","
    STATE_JSON+="{\"Id\":\"$s_id\",\"Name\":\"$s_name\",\"Port\":$s_port,\"PID\":${PROC_PID:-0},\"Url\":\"$s_url\"}"
    FIRST_ITEM=false
done

STATE_JSON+="]"
echo "$STATE_JSON" > "$STATE_FILE"

# ------------------------------------------------------------------------------
# Espera Activa para Inicialización de Modelos y Apertura de Sockets
# ------------------------------------------------------------------------------
echo -e "${C_GRAY}Esperando a que los servicios completen su inicio (cargando modelos NLP)...${C_RESET}"
MAX_WAIT=25
ELAPSED=0
TOTAL_SERVICES=${#SERVICES_DEF[@]}

while [ "$ELAPSED" -lt "$MAX_WAIT" ]; do
    ACTIVE=0
    for s_def in "${SERVICES_DEF[@]}"; do
        IFS="|" read -r s_id s_name s_dir s_type s_port s_url s_args <<< "$s_def"
        [ "$s_type" = "npm" ] && continue
        p_pid="$(get_port_process_id "$s_port")"
        if [ -n "$p_pid" ]; then
            ACTIVE=$((ACTIVE + 1))
        fi
    done

    # Si todos los microservicios python ya responden, podemos continuar
    if [ "$ACTIVE" -ge $((TOTAL_SERVICES - 1)) ]; then
        break
    fi

    sleep 2
    ELAPSED=$((ELAPSED + 2))
done

# ------------------------------------------------------------------------------
# Tabla Final de Estado e Instrucciones
# ------------------------------------------------------------------------------
show_status_table

echo -e "${C_CYAN}Instrucciones de uso en el servidor:${C_RESET}"
echo -e "  * Para verificar el estado de los servicios:   ${C_BOLD}./iniciar_servicios.sh --status${C_RESET}"
echo -e "  * Para detener todos los servicios:           ${C_BOLD}./iniciar_servicios.sh --stop${C_RESET}"
echo -e "  * Registros (logs) de cada servicio en:       ${C_BOLD}logs/${C_RESET} (o .logs/)\n"
