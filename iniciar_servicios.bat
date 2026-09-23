@echo off
REM ==============================================================================
REM Acceso directo para levantar todos los servicios NLP con PowerShell
REM Repositorio: Uso de NLP, AI y LLMs a textos semiestructurados
REM ==============================================================================

title Iniciando servicios NLP y LLMs...
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar_servicios.ps1" %*

if "%~1"=="" (
    echo.
    echo Presione cualquier tecla para cerrar esta ventana...
    pause >nul
)
