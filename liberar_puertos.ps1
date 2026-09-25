<#
.SYNOPSIS
    Script para liberar de forma forzada los puertos ocupados por los microservicios en Windows.
    Puertos por defecto: 8000 al 8015 y 5173
#>

param(
    [int[]]$Ports = @(8000, 8001, 8002, 8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010, 8011, 8012, 8013, 8014, 8015, 5173)
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host "`n================================================================================" -ForegroundColor Cyan
Write-Host "                LIBERADOR DE PUERTOS Y PROCESOS NLP (WINDOWS)                  " -ForegroundColor Cyan
Write-Host "================================================================================`n" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$StateFile = Join-Path $ScriptDir ".services_state.json"
if (Test-Path $StateFile) { Remove-Item $StateFile -Force }

$freedCount = 0
$occupiedCount = 0

foreach ($port in $Ports) {
    $connections = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($connections) {
        $occupiedCount++
        foreach ($conn in $connections) {
            $pidToKill = $conn.OwningProcess
            if ($pidToKill -and $pidToKill -ne 0) {
                Write-Host "  -> Liberando puerto $port (PID $pidToKill)..." -ForegroundColor Yellow
                Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
                $freedCount++
            }
        }
    }
}

# Detener cualquier uvicorn remanente
Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -match "uvicorn" -or $_.CommandLine -match "runserver"
} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "`n================================================================================" -ForegroundColor Cyan
if ($occupiedCount -eq 0) {
    Write-Host "Todos los puertos analizados estaban libres." -ForegroundColor Green
} else {
    Write-Host "Se procesaron $occupiedCount puertos ocupados y se liberaron sus procesos." -ForegroundColor Green
}
Write-Host "Ahora puedes iniciar los servicios con .\iniciar_servicios.ps1`n" -ForegroundColor Cyan
