#!/usr/bin/env bash
# ==============================================================================
# Script: liberar_puertos.sh
# Descripción: Libera de forma forzada los puertos ocupados por los microservicios
#              y mata cualquier proceso zombie o colgado en Linux (Ubuntu).
# Puertos por defecto: 8000 al 8015 y 5173
# ==============================================================================

set -uo pipefail

# Paleta de colores ANSI
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_CYAN="\033[0;36m"
C_GREEN="\033[0;32m"
C_YELLOW="\033[1;33m"
C_RED="\033[0;31m"
C_GRAY="\033[0;90m"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE_FILE="$SCRIPT_DIR/.services_state.json"
LOGS_DIR="$SCRIPT_DIR/logs"

# Si se pasan puertos por argumento, usar solo esos; si no, usar todos los del proyecto
if [ $# -gt 0 ]; then
    TARGET_PORTS=("$@")
else
    TARGET_PORTS=(8000 8001 8002 8003 8004 8005 8006 8007 8008 8009 8010 8011 8012 8013 8014 8015 5173)
fi

echo -e "\n${C_CYAN}================================================================================${C_RESET}"
echo -e "${C_CYAN}                  LIBERADOR DE PUERTOS Y PROCESOS NLP (LINUX)                   ${C_RESET}"
echo -e "${C_CYAN}================================================================================${C_RESET}\n"

# Función para verificar si un puerto realmente puede enlazarse (usando socket Python)
check_port_busy() {
    local port="$1"
    python3 -c "
import socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind(('0.0.0.0', int('$port')))
    s.close()
    sys.exit(0) # Puerto LIBRE
except OSError:
    sys.exit(1) # Puerto OCUPADO
" 2>/dev/null
    return $?
}

# 1. Matar procesos huérfanos de uvicorn y django por línea de comandos
echo -e "${C_GRAY}Buscando y deteniendo procesos uvicorn/django asociados...${C_RESET}"
pkill -9 -f "uvicorn.*main:app" 2>/dev/null || true
pkill -9 -f "uvicorn.*api:app" 2>/dev/null || true
pkill -9 -f "uvicorn.*app.main:app" 2>/dev/null || true
pkill -9 -f "manage.py runserver.*8000" 2>/dev/null || true

# 2. Iterar sobre cada puerto objetivo
OCCUPIED_FOUND=0
FREED_COUNT=0
STILL_BUSY=()

for port in "${TARGET_PORTS[@]}"; do
    # Verificar si está ocupado
    if ! check_port_busy "$port"; then
        OCCUPIED_FOUND=$((OCCUPIED_FOUND + 1))
        echo -e "  -> Puerto ${C_YELLOW}${port}${C_RESET} está ocupado. Liberando..."

        # Método A: fuser (mata directamente el proceso en el socket)
        if command -v fuser >/dev/null 2>&1; then
            fuser -k -9 "${port}/tcp" 2>/dev/null || true
        fi

        # Método B: lsof (extrae PIDs y los termina con SIGKILL)
        if command -v lsof >/dev/null 2>&1; then
            pids=$(lsof -ti ":${port}" 2>/dev/null || true)
            if [ -n "$pids" ]; then
                for p in $pids; do
                    kill -9 "$p" 2>/dev/null || true
                done
            fi
        fi

        # Método C: ss / netstat para encontrar PIDs
        if command -v ss >/dev/null 2>&1; then
            ss_pids=$(ss -lptn "sport = :${port}" 2>/dev/null | grep -o 'pid=[0-9]*' | cut -d= -f2 || true)
            if [ -n "$ss_pids" ]; then
                for p in $ss_pids; do
                    kill -9 "$p" 2>/dev/null || true
                done
            fi
        fi

        sleep 0.3

        # Comprobar si se liberó con éxito
        if check_port_busy "$port"; then
            echo -e "     ${C_GREEN}[OK] Puerto ${port} liberado exitosamente.${C_RESET}"
            FREED_COUNT=$((FREED_COUNT + 1))
        else
            echo -e "     ${C_RED}[!] No se pudo liberar el puerto ${port} (puede pertenecer a root).${C_RESET}"
            STILL_BUSY+=("$port")
        fi
    fi
done

# 3. Limpiar archivo de estado y PIDs temporales
rm -f "$STATE_FILE" 2>/dev/null || true
if [ -d "$LOGS_DIR" ]; then
    rm -f "$LOGS_DIR"/*.pid 2>/dev/null || true
fi

# 4. Resumen
echo -e "\n${C_CYAN}================================================================================${C_RESET}"
echo -e "${C_CYAN}                               RESUMEN FINAL                                    ${C_RESET}"
echo -e "${C_CYAN}================================================================================${C_RESET}"

if [ "$OCCUPIED_FOUND" -eq 0 ]; then
    echo -e "${C_GREEN}Todos los puertos analizados (${TARGET_PORTS[*]}) ya estaban libres.${C_RESET}\n"
elif [ "${#STILL_BUSY[@]}" -eq 0 ]; then
    echo -e "${C_GREEN}¡Se liberaron exitosamente todos los puertos ($FREED_COUNT de $OCCUPIED_FOUND ocupados)!${C_RESET}"
    echo -e "${C_CYAN}Ahora puedes iniciar tus servicios sin errores ejecutando:${C_RESET}"
    echo -e "  ${C_BOLD}${C_YELLOW}./iniciar_servicios.sh${C_RESET}\n"
else
    echo -e "${C_YELLOW}Se liberaron $FREED_COUNT puertos, pero los siguientes siguen ocupados: ${STILL_BUSY[*]}${C_RESET}"
    echo -e "${C_RED}Si esos procesos fueron iniciados con 'sudo' o por otro usuario, ejecuta:${C_RESET}"
    echo -e "  ${C_BOLD}${C_YELLOW}sudo ./liberar_puertos.sh${C_RESET}\n"
fi
