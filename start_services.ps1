<#
.SYNOPSIS
    Script para orquestar y levantar todos los microservicios y aplicaciones del repositorio.

.DESCRIPTION
    Inicia en segundo plano cada microservicio en un puerto dedicado evitando colisiones,
    redirige los logs a la carpeta .logs/ y muestra una tabla detallada con el nombre del servicio,
    el puerto asignado, la URL de la documentacion interactiva (Swagger) y el estado del proceso.

.PARAMETER Stop
    Detiene todos los procesos y libera los puertos asignados a los servicios.

.PARAMETER Status
    Muestra la tabla del estado actual de todos los servicios sin reiniciar procesos.

.PARAMETER IncludeWebDoc
    Si se especifica, tambien intenta levantar la aplicacion frontend Vite/React (WebDocumentacion).

.EXAMPLE
    .\start_services.ps1
    Levanta todos los servicios y muestra la tabla resumen.

.EXAMPLE
    .\start_services.ps1 -Stop
    Detiene todos los servicios iniciados.

.EXAMPLE
    .\start_services.ps1 -Status
    Verifica los puertos y muestra el estado de cada servicio.
#>

param(
    [switch]$Stop,
    [switch]$Status,
    [switch]$IncludeWebDoc
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LogsDir = Join-Path $ScriptDir ".logs"
$StateFile = Join-Path $ScriptDir ".services_state.json"

# =============================================================================
# DEFINICION DE SERVICIOS Y PUERTOS
# =============================================================================
$Services = @(
    [PSCustomObject]@{
        Id             = "appweb"
        Name           = "AppWeb (Portal Django)"
        Directory      = "AppWeb"
        Type           = "django"
        CommandArgs    = @("manage.py", "runserver", "127.0.0.1:8000", "--noreload")
        Port           = 8000
        Url            = "http://127.0.0.1:8000"
        DocsUrl        = "http://127.0.0.1:8000"
    },
    [PSCustomObject]@{
        Id             = "cliches"
        Name           = "Deteccion de Cliches"
        Directory      = "servicio-deteccion-cliches"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8001")
        Port           = 8001
        Url            = "http://127.0.0.1:8001"
        DocsUrl        = "http://127.0.0.1:8001/docs"
    },
    [PSCustomObject]@{
        Id             = "repeticion"
        Name           = "Repeticion de Palabras"
        Directory      = "servicio-repeticion-palabras"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8002")
        Port           = 8002
        Url            = "http://127.0.0.1:8002"
        DocsUrl        = "http://127.0.0.1:8002/docs"
    },
    [PSCustomObject]@{
        Id             = "conectores_logicos"
        Name           = "Conectores Logicos"
        Directory      = "deteccion_conectores_logicos"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8003")
        Port           = 8003
        Url            = "http://127.0.0.1:8003"
        DocsUrl        = "http://127.0.0.1:8003/docs"
    },
    [PSCustomObject]@{
        Id             = "doble_negacion"
        Name           = "Doble Negacion"
        Directory      = "detector_doble_negacion"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8004")
        Port           = 8004
        Url            = "http://127.0.0.1:8004"
        DocsUrl        = "http://127.0.0.1:8004/docs"
    },
    [PSCustomObject]@{
        Id             = "puntuacion_inusual"
        Name           = "Puntuacion Inusual"
        Directory      = "deteccion_puntuacion_inusual"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8005")
        Port           = 8005
        Url            = "http://127.0.0.1:8005"
        DocsUrl        = "http://127.0.0.1:8005/docs"
    },
    [PSCustomObject]@{
        Id             = "verbos_modales"
        Name           = "Verbos Modales"
        Directory      = "deteccion_verbos_modales"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8006")
        Port           = 8006
        Url            = "http://127.0.0.1:8006"
        DocsUrl        = "http://127.0.0.1:8006/docs"
    },
    [PSCustomObject]@{
        Id             = "detector_adverbios"
        Name           = "Detector de Adverbios"
        Directory      = "detector_adverbios"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8007")
        Port           = 8007
        Url            = "http://127.0.0.1:8007"
        DocsUrl        = "http://127.0.0.1:8007/docs"
    },
    [PSCustomObject]@{
        Id             = "metricas_legibilidad"
        Name           = "Metricas de Legibilidad"
        Directory      = "metricas-de-legibilidad"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8008")
        Port           = 8008
        Url            = "http://127.0.0.1:8008"
        DocsUrl        = "http://127.0.0.1:8008/docs"
    },
    [PSCustomObject]@{
        Id             = "oraciones_impersonales"
        Name           = "Oraciones Impersonales"
        Directory      = "oraciones-impersonales"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8009")
        Port           = 8009
        Url            = "http://127.0.0.1:8009"
        DocsUrl        = "http://127.0.0.1:8009/docs"
    },
    [PSCustomObject]@{
        Id             = "verbos_percepcion_opinion"
        Name           = "Verbos Percepcion / Opinion"
        Directory      = "verbos_percepcion_opinion"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8010")
        Port           = 8010
        Url            = "http://127.0.0.1:8010"
        DocsUrl        = "http://127.0.0.1:8010/docs"
    },
    [PSCustomObject]@{
        Id             = "voz_pasiva"
        Name           = "Voz Pasiva"
        Directory      = "voz_pasiva"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8011")
        Port           = 8011
        Url            = "http://127.0.0.1:8011"
        DocsUrl        = "http://127.0.0.1:8011/docs"
    },
    [PSCustomObject]@{
        Id             = "weak_verbs"
        Name           = "Verbos Debiles (Weak Verbs)"
        Directory      = "weak_verbs"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8012")
        Port           = 8012
        Url            = "http://127.0.0.1:8012"
        DocsUrl        = "http://127.0.0.1:8012/docs"
    },
    [PSCustomObject]@{
        Id             = "abstract_words"
        Name           = "Palabras Abstractas"
        Directory      = "abstract_words"
        Type           = "uvicorn"
        CommandArgs    = @("-m", "uvicorn", "api:app", "--host", "127.0.0.1", "--port", "8013")
        Port           = 8013
        Url            = "http://127.0.0.1:8013"
        DocsUrl        = "http://127.0.0.1:8013/docs"
    }
)

if ($IncludeWebDoc) {
    $Services += [PSCustomObject]@{
        Id             = "web_documentacion"
        Name           = "Web Documentacion (Vite/React)"
        Directory      = "WebDocumentacion"
        Type           = "npm"
        CommandArgs    = @("run", "dev", "--", "--port", "5173")
        Port           = 5173
        Url            = "http://localhost:5173"
        DocsUrl        = "http://localhost:5173"
    }
}

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================
function Find-PythonExecutable {
    # 1. Entorno virtual activo
    if ($env:VIRTUAL_ENV) {
        $candidate = Join-Path $env:VIRTUAL_ENV "Scripts\python.exe"
        if (Test-Path $candidate) { return $candidate }
    }

    # 2. Entorno virtual local 'entorno'
    $localEntorno = Join-Path $ScriptDir "entorno\Scripts\python.exe"
    if (Test-Path $localEntorno) { return $localEntorno }

    # 3. Otros nombres comunes (.venv, venv)
    foreach ($v in @(".venv", "venv")) {
        $candidate = Join-Path $ScriptDir "$v\Scripts\python.exe"
        if (Test-Path $candidate) { return $candidate }
    }

    # 4. python en PATH
    $pyCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pyCmd) {
        $realPath = $pyCmd.Source
        if ((Get-Item $realPath).Length -gt 0) {
            return $realPath
        }
    }

    # 5. py launcher de Python.org
    $pyLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        $realPy = & py.exe -3.12 -c "import sys; print(sys.executable)" 2>$null
        if ($realPy -and (Test-Path $realPy)) {
            return $realPy.Trim()
        }
    }

    return $null
}

function Get-PortProcessId($Port) {
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($conn -and $conn.OwningProcess -and $conn.OwningProcess -ne 0) {
        return $conn.OwningProcess
    }
    return $null
}

function Stop-AllServices {
    Write-Host "`n=================================================================" -ForegroundColor Yellow
    Write-Host "                DETENIENDO SERVICIOS ACTIVOS                     " -ForegroundColor Yellow
    Write-Host "=================================================================`n" -ForegroundColor Yellow

    # Detener por estado guardado
    if (Test-Path $StateFile) {
        try {
            $saved = Get-Content $StateFile -Raw | ConvertFrom-Json
            foreach ($item in $saved) {
                if ($item.PID) {
                    $p = Get-Process -Id $item.PID -ErrorAction SilentlyContinue
                    if ($p) {
                        Write-Host "  -> Deteniendo proceso $($item.Name) (PID $($item.PID))..." -ForegroundColor Gray
                        Stop-Process -Id $item.PID -Force -ErrorAction SilentlyContinue
                    }
                }
            }
        } catch { }
        Remove-Item $StateFile -Force -ErrorAction SilentlyContinue
    }

    # Detener por puertos asignados para asegurar liberacion
    foreach ($svc in $Services) {
        $pidOnPort = Get-PortProcessId -Port $svc.Port
        if ($pidOnPort) {
            Write-Host "  -> Liberando puerto $($svc.Port) ($($svc.Name), PID $pidOnPort)..." -ForegroundColor Gray
            Stop-Process -Id $pidOnPort -Force -ErrorAction SilentlyContinue
        }
    }

    Write-Host "`n[OK] Todos los servicios han sido detenidos y los puertos liberados.`n" -ForegroundColor Green
}

function Show-StatusTable {
    Write-Host "`n==========================================================================================" -ForegroundColor Cyan
    Write-Host "                           ESTADO DE LOS SERVICIOS                                         " -ForegroundColor Cyan
    Write-Host "==========================================================================================" -ForegroundColor Cyan

    $rows = @()
    foreach ($svc in $Services) {
        $pidOnPort = Get-PortProcessId -Port $svc.Port
        $status = if ($pidOnPort) { "ACTIVO" } else { "DETENIDO" }
        $pidText = if ($pidOnPort) { $pidOnPort } else { "-" }

        $rows += [PSCustomObject]@{
            "Servicio"            = $svc.Name
            "Puerto"              = $svc.Port
            "Estado"              = $status
            "PID"                 = $pidText
            "URL / Documentacion" = $svc.DocsUrl
        }
    }

    $rows | Format-Table -AutoSize
}

# =============================================================================
# PROCESAMIENTO DE PARAMETROS: STOP / STATUS
# =============================================================================
if ($Stop) {
    Stop-AllServices
    exit 0
}

if ($Status) {
    Show-StatusTable
    exit 0
}

# =============================================================================
# INICIALIZACION Y VALIDACION DEL ENTORNO
# =============================================================================
Clear-Host
Write-Host "==========================================================================================" -ForegroundColor Cyan
Write-Host "                   LEVANTANDO TODOS LOS SERVICIOS (NLP & LLMs)                           " -ForegroundColor Cyan
Write-Host "==========================================================================================" -ForegroundColor Cyan

$pythonExe = Find-PythonExecutable

if (-not $pythonExe) {
    Write-Host "`n[ERROR] No se encontro un interprete de Python valido." -ForegroundColor Red
    Write-Host "Asegurate de activar el entorno virtual o tener Python instalado." -ForegroundColor Yellow
    exit 1
}

Write-Host "`nInterprete de Python detectado:" -ForegroundColor Gray
Write-Host "  $pythonExe`n" -ForegroundColor DarkCyan

# Verificar si uvicorn y fastapi estan instalados en este entorno
$checkFastAPI = & $pythonExe -c "import fastapi, uvicorn; print('OK')" 2>$null
if ($checkFastAPI -ne "OK") {
    Write-Host "[!] ADVERTENCIA: 'fastapi' o 'uvicorn' no estan instalados en este interprete de Python." -ForegroundColor Yellow
    Write-Host "    Para instalar todas las dependencias del proyecto, ejecuta primero:" -ForegroundColor Yellow
    Write-Host "    & '$pythonExe' -m pip install -r requirements.txt`n" -ForegroundColor White
}

# Verificar si los modelos de spaCy estan descargados
$checkSpacyModels = & $pythonExe -c "import importlib.util; sm = bool(importlib.util.find_spec('en_core_web_sm')); trf = bool(importlib.util.find_spec('en_core_web_trf')); print(f'{sm},{trf}')" 2>$null
if ($checkSpacyModels) {
    $smInstalled, $trfInstalled = $checkSpacyModels.Trim().Split(',')
    if ($smInstalled -ne "True") {
        Write-Host "[!] ADVERTENCIA: Falta descargar el modelo spaCy 'en_core_web_sm'." -ForegroundColor Yellow
        Write-Host "    Ejecuta: & '$pythonExe' -m spacy download en_core_web_sm`n" -ForegroundColor White
    }
    if ($trfInstalled -ne "True") {
        Write-Host "[!] ADVERTENCIA: Falta descargar el modelo spaCy 'en_core_web_trf'." -ForegroundColor Yellow
        Write-Host "    Ejecuta: & '$pythonExe' -m spacy download en_core_web_trf`n" -ForegroundColor White
    }
}

# Asegurar carpeta de logs
if (-not (Test-Path $LogsDir)) {
    New-Item -Path $LogsDir -ItemType Directory | Out-Null
}

# =============================================================================
# LANZAMIENTO DE CADA SERVICIO
# =============================================================================
$launchedState = @()

foreach ($svc in $Services) {
    $fullDir = Join-Path $ScriptDir $svc.Directory

    if (-not (Test-Path $fullDir)) {
        Write-Host "[SALTADO] Carpeta no encontrada: $($svc.Directory)" -ForegroundColor DarkYellow
        continue
    }

    # Verificar si el puerto ya esta ocupado
    $existingPid = Get-PortProcessId -Port $svc.Port
    if ($existingPid) {
        Write-Host "[INFO] Puerto $($svc.Port) ya ocupado ($($svc.Name) activo en PID $existingPid)." -ForegroundColor Yellow
        $launchedState += [PSCustomObject]@{
            Id   = $svc.Id
            Name = $svc.Name
            Port = $svc.Port
            PID  = $existingPid
            Url  = $svc.DocsUrl
        }
        continue
    }

    # Caso especial abstract_words: advertir si no hay modelo entrenado
    if ($svc.Id -eq "abstract_words") {
        $hasJoblib = Get-ChildItem -Path "$fullDir\models" -Filter "*.joblib" -ErrorAction SilentlyContinue
        if (-not $hasJoblib) {
            Write-Host "[AVISO] 'abstract_words': Requiere entrenar el modelo antes del primer uso (python train_model.py)." -ForegroundColor DarkYellow
        }
    }

    $logOut = Join-Path $LogsDir "$($svc.Id).log"
    $logErr = Join-Path $LogsDir "$($svc.Id)_err.log"

    $exePath = $pythonExe
    $argsList = $svc.CommandArgs

    if ($svc.Type -eq "npm") {
        $npmCmd = Get-Command npm.cmd -ErrorAction SilentlyContinue
        if ($npmCmd) {
            $exePath = $npmCmd.Source
        } else {
            Write-Host "[AVISO] Node/npm no encontrado para $($svc.Name)." -ForegroundColor DarkYellow
            continue
        }
    }

    try {
        $proc = Start-Process -FilePath $exePath `
                              -ArgumentList $argsList `
                              -WorkingDirectory $fullDir `
                              -PassThru `
                              -RedirectStandardOutput $logOut `
                              -RedirectStandardError $logErr `
                              -WindowStyle Hidden

        $launchedState += [PSCustomObject]@{
            Id   = $svc.Id
            Name = $svc.Name
            Port = $svc.Port
            PID  = $proc.Id
            Url  = $svc.DocsUrl
        }
    } catch {
        Write-Host "[ERROR] No se pudo iniciar $($svc.Name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Guardar estado para poder detenerlos posteriormente
$launchedState | ConvertTo-Json | Set-Content -Path $StateFile -Force

# Pausa para permitir que los servicios inicialicen sus modelos y abran sus sockets
Write-Host "Esperando a que los servicios completen su inicio (cargando modelos NLP)..." -ForegroundColor Gray
Start-Sleep -Seconds 6

# =============================================================================
# MOSTRAR TABLA FINAL CON SERVICIOS Y PUERTOS
# =============================================================================
Show-StatusTable

Write-Host "Instrucciones de uso:" -ForegroundColor Cyan
Write-Host "  * Para verificar el estado de los servicios:   .\start_services.ps1 -Status" -ForegroundColor White
Write-Host "  * Para detener todos los servicios:           .\start_services.ps1 -Stop" -ForegroundColor White
Write-Host "  * Los registros (logs) de cada servicio estan en: .logs\`n" -ForegroundColor White
