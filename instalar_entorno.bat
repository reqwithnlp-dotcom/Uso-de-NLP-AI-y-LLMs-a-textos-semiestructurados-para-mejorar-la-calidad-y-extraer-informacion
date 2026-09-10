@echo off
REM ==============================================================================
REM Acceso directo para instalar el entorno completo con PowerShell (Bypass ExecutionPolicy)
REM Repositorio: Uso de NLP, AI y LLMs a textos semiestructurados
REM ==============================================================================

title Instalando entorno NLP y LLMs...
echo ==============================================================================
echo        INICIANDO INSTALACION DEL ENTORNO (PROYECTO NLP & LLMs)
echo ==============================================================================
echo.

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0instalar_entorno.ps1"

echo.
echo Presione cualquier tecla para salir...
pause >nul
