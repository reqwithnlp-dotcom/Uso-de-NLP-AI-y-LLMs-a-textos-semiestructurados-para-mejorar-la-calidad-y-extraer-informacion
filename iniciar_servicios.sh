#!/usr/bin/env bash
# ==============================================================================
# Script: iniciar_servicios.sh
# Alias en español para start_services.sh (servidor Linux / Ubuntu)
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="$SCRIPT_DIR/start_services.sh"

if [ ! -f "$TARGET" ]; then
    echo "[ERROR] No se encontró $TARGET" >&2
    exit 1
fi

chmod +x "$TARGET" 2>/dev/null || true
exec "$TARGET" "$@"
