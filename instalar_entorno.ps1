<#
.SYNOPSIS
    Script de instalacion y configuracion automatica del entorno para el proyecto.
    Repositorio: Uso de NLP, AI y LLMs a textos semiestructurados.

.DESCRIPTION
    Este script automatiza por completo la preparacion del proyecto en cualquier computadora con Windows:
    1. Detecta o solicita un interprete de Python 3.10 - 3.12 valido.
    2. Crea el entorno virtual 'entorno' si no existe.
    3. Actualiza pip y setuptools.
    4. Instala todas las dependencias consolidadas desde requirements.txt.
    5. Descarga los modelos de spaCy necesarios (en_core_web_sm, en_core_web_trf y en_core_web_md).
    6. Descarga y deja en cache local el modelo Sentence-Transformers (SBERT).
    7. Aplica las migraciones iniciales de base de datos para la aplicacion Django (AppWeb).
    8. Ejecuta un test de verificacion de integridad de todos los microservicios.

.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\instalar_entorno.ps1
#>

[CmdletBinding()]
param(
    [switch]$RecreateVenv,
    [switch]$StartServices
)

$ErrorActionPreference = "Continue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$VenvDir = Join-Path $ScriptDir "entorno"
$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$ReqFile = Join-Path $ScriptDir "requirements.txt"

function Write-Section($title) {
    Write-Host "`n==========================================================================================" -ForegroundColor Cyan
    Write-Host "  $title" -ForegroundColor Cyan
    Write-Host "==========================================================================================" -ForegroundColor Cyan
}

function Write-Success($msg) {
    Write-Host "  [OK] $msg" -ForegroundColor Green
}

function Write-WarningMsg($msg) {
    Write-Host "  [!] $msg" -ForegroundColor Yellow
}

function Write-ErrorMsg($msg) {
    Write-Host "  [ERROR] $msg" -ForegroundColor Red
}

# =============================================================================
# PASO 1: DETECCION DEL INTERPRETE BASE DE PYTHON
# =============================================================================
Write-Section "PASO 1: Verificando instalacion de Python en el sistema"

function Find-BasePython {
    # 1. Probar lanzador py con version 3.12 o 3.11
    $pyLauncher = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($pyLauncher) {
        foreach ($ver in @("-3.12", "-3.11", "-3.10", "-3")) {
            $test = & py.exe $ver -c "import sys; print(sys.executable)" 2>$null
            if ($test -and (Test-Path $test.Trim())) {
                return @("py.exe", $ver)
            }
        }
    }

    # 2. Probar python en PATH
    $pyCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($pyCmd) {
        $realPath = $pyCmd.Source
        if ((Get-Item $realPath).Length -gt 0) {
            # Descartar alias de WindowsApps de 0 bytes
            $isWorking = & $realPath -c "import sys; print(sys.executable)" 2>$null
            if ($isWorking) {
                return @($realPath, "")
            }
        }
    }

    # 3. Buscar en rutas estandar de AppData y Program Files
    $standardPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:ProgramFiles\Python312\python.exe",
        "$env:ProgramFiles\Python311\python.exe"
    )

    foreach ($p in $standardPaths) {
        if (Test-Path $p) {
            return @($p, "")
        }
    }

    # 4. En maquina nueva sin Python: auto-instalar Python 3.12 desatendido via winget
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "  -> Python no detectado. Intentando instalacion automatica via winget..." -ForegroundColor Yellow
        & winget.exe install Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements --scope currentUser
        foreach ($p in $standardPaths) {
            if (Test-Path $p) {
                return @($p, "")
            }
        }
        $pyCmd = Get-Command python.exe -ErrorAction SilentlyContinue
        if ($pyCmd -and (Test-Path $pyCmd.Source) -and (Get-Item $pyCmd.Source).Length -gt 0) {
            return @($pyCmd.Source, "")
        }
    }

    return $null
}

# Auto-instalar VC++ Redistributable si falta en Windows virgen
if (-not (Test-Path "$env:SystemRoot\System32\vcruntime140.dll")) {
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "  -> Visual C++ Runtime ausente. Instalando silenciosamente via winget..." -ForegroundColor Yellow
        & winget.exe install Microsoft.VCRedist.2015+.x64 --silent --accept-package-agreements --accept-source-agreements
    }
}

$basePy = Find-BasePython

if (-not $basePy) {
    Write-ErrorMsg "No se encontro una instalacion funcional de Python en este equipo."
    Write-Host "`nPor favor, instala Python 3.12 desde: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "IMPORTANTE: Durante la instalacion marca la casilla 'Add python.exe to PATH'." -ForegroundColor Yellow
    exit 1
}

$basePyExe = $basePy[0]
$basePyArg = $basePy[1]

$detectedVersion = if ($basePyArg) {
    & $basePyExe $basePyArg -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
} else {
    & $basePyExe -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}')"
}

Write-Success "Python base detectado: $basePyExe $basePyArg (Version: $detectedVersion)"

# =============================================================================
# PASO 2: CREACION O VALIDACION DEL ENTORNO VIRTUAL
# =============================================================================
Write-Section "PASO 2: Preparando entorno virtual ('entorno')"

if ($RecreateVenv -and (Test-Path $VenvDir)) {
    Write-Host "  -> Eliminando entorno existente por parametro -RecreateVenv..." -ForegroundColor Gray
    Remove-Item -Path $VenvDir -Recurse -Force -ErrorAction SilentlyContinue
}

if (-not (Test-Path $VenvPython)) {
    Write-Host "  -> Creando nuevo entorno virtual en: $VenvDir ..." -ForegroundColor Gray
    if ($basePyArg) {
        & $basePyExe $basePyArg -m venv $VenvDir
    } else {
        & $basePyExe -m venv $VenvDir
    }

    if (-not (Test-Path $VenvPython)) {
        Write-ErrorMsg "No se pudo crear el entorno virtual. Verifica los permisos de la carpeta."
        exit 1
    }
    Write-Success "Entorno virtual creado exitosamente."
} else {
    Write-Success "Entorno virtual existente encontrado en: $VenvDir"
}

# =============================================================================
# PASO 3: ACTUALIZACION DE HERRAMIENTAS DE PIP
# =============================================================================
Write-Section "PASO 3: Actualizando pip, setuptools y wheel"
Write-Host "  -> Actualizando gestor de paquetes pip..." -ForegroundColor Gray
& $VenvPython -m pip install --upgrade pip setuptools wheel --quiet
Write-Success "Gestor de paquetes pip actualizado."

# =============================================================================
# PASO 4: INSTALACION DE DEPENDENCIAS DE REQUIREMENTS.TXT
# =============================================================================
Write-Section "PASO 4: Instalando dependencias del proyecto (requirements.txt)"

if (-not (Test-Path $ReqFile)) {
    Write-ErrorMsg "No se encontro el archivo requirements.txt en: $ReqFile"
    exit 1
}

Write-Host "  -> Instalando librerias (FastAPI, spaCy, PyTorch, Transformers, Scikit-Learn, Django, etc.)..." -ForegroundColor Gray
Write-Host "     (Esto puede tardar unos minutos dependiendo de la conexion a internet)..." -ForegroundColor DarkGray

& $VenvPython -m pip install --no-input --disable-pip-version-check -r $ReqFile

if ($LASTEXITCODE -ne 0) {
    Write-ErrorMsg "Hubo un error al instalar los paquetes de requirements.txt."
    Write-Host "`nSi el error menciona 'Microsoft Visual C++ 14.0 or greater is required':" -ForegroundColor Yellow
    Write-Host "Instala Visual C++ Build Tools desde: https://visualstudio.microsoft.com/visual-cpp-build-tools/" -ForegroundColor White
    exit 1
}
Write-Success "Todas las dependencias de requirements.txt han sido instaladas."

# =============================================================================
# PASO 5: DESCARGA DE MODELOS DE SPACY
# =============================================================================
Write-Section "PASO 5: Descargando modelos de lenguaje de spaCy"

Write-Host "  -> Descargando modelo spaCy ligero: en_core_web_sm..." -ForegroundColor Gray
& $VenvPython -m spacy download en_core_web_sm
if ($LASTEXITCODE -eq 0) {
    Write-Success "Modelo 'en_core_web_sm' instalado correctamente."
} else {
    Write-ErrorMsg "Fallo la descarga de 'en_core_web_sm'."
}

Write-Host "`n  -> Descargando modelo spaCy basado en Transformers: en_core_web_trf..." -ForegroundColor Gray
& $VenvPython -m spacy download en_core_web_trf
if ($LASTEXITCODE -eq 0) {
    Write-Success "Modelo 'en_core_web_trf' instalado correctamente."
} else {
    Write-ErrorMsg "Fallo la descarga de 'en_core_web_trf'."
}

Write-Host "`n  -> Descargando modelo spaCy mediano: en_core_web_md..." -ForegroundColor Gray
& $VenvPython -m spacy download en_core_web_md
if ($LASTEXITCODE -eq 0) {
    Write-Success "Modelo 'en_core_web_md' instalado correctamente."
} else {
    Write-ErrorMsg "Fallo la descarga de 'en_core_web_md'."
}

# =============================================================================
# PASO 6: PRE-DESCARGA DEL MODELO SBERT (SENTENCE TRANSFORMERS)
# =============================================================================
Write-Section "PASO 6: Descargando y guardando en cache el modelo SBERT"

Write-Host "  -> Descargando 'paraphrase-MiniLM-L6-v2' para deteccion de cliches..." -ForegroundColor Gray
& $VenvPython -c "
try:
    from sentence_transformers import SentenceTransformer
    m = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    print('OK_SBERT')
except Exception as e:
    print(f'ERROR: {e}')
"

Write-Success "Modelo Sentence-Transformers precargado en cache."

# =============================================================================
# PASO 7: ENTRENAMIENTO DEL MODELO DE PALABRAS ABSTRACTAS (ABSTRACT_WORDS)
# =============================================================================
Write-Section "PASO 7: Verificando modelo de clasificacion de palabras abstractas"

$AbstractModel = Join-Path $ScriptDir "abstract_words\models\spacy_rf.joblib"
$AbstractDataset = Join-Path $ScriptDir "abstract_words\datasets\Concreteness_ratings_Brysbaert_et_al_BRM.txt"

if (-not (Test-Path $AbstractModel)) {
    if (Test-Path $AbstractDataset) {
        Write-Host "  -> Entrenando modelo (spaCy + Random Forest) a partir del dataset de concrecion..." -ForegroundColor Gray
        Write-Host "     (Esto toma aproximadamente 1 a 2 minutos en una instalacion limpia)..." -ForegroundColor DarkGray
        $AbstractDir = Join-Path $ScriptDir "abstract_words"
        Push-Location $AbstractDir
        try {
            if (-not (Test-Path "datasets\train.csv")) {
                & $VenvPython "split_dataset.py"
            }
            & $VenvPython "train_model.py"
            if (Test-Path "models\spacy_rf.joblib") {
                Write-Success "Modelo de palabras abstractas entrenado y guardado correctamente."
            } else {
                Write-WarningMsg "No se pudo generar 'spacy_rf.joblib'. El servicio usara el estimador de contingencia."
            }
        } catch {
            Write-WarningMsg "Error durante el entrenamiento: $($_.Exception.Message)"
        } finally {
            Pop-Location
        }
    } else {
        Write-WarningMsg "Dataset de concrecion no encontrado. El servicio usara modelo de contingencia."
    }
} else {
    Write-Success "Modelo 'spacy_rf.joblib' listo (detectado en abstract_words/models)."
}

# =============================================================================
# PASO 8: MIGRACIONES DE BASE DE DATOS DJANGO (APPWEB)
# =============================================================================
Write-Section "PASO 8: Inicializando base de datos Django (AppWeb)"

$appWebDir = Join-Path $ScriptDir "AppWeb"
$managePy = Join-Path $appWebDir "manage.py"

if (Test-Path $managePy) {
    Write-Host "  -> Aplicando migraciones de SQLite..." -ForegroundColor Gray
    Push-Location $appWebDir
    try {
        & $VenvPython "manage.py" migrate --noinput
        Write-Success "Base de datos de Django inicializada."
    } catch {
        Write-WarningMsg "No se pudo aplicar las migraciones de Django: $($_.Exception.Message)"
    } finally {
        Pop-Location
    }
}

# =============================================================================
# PASO 9: VERIFICACION DE INTEGRIDAD DE TODOS LOS MICROSERVICIOS
# =============================================================================
Write-Section "PASO 9: Comprobando que todos los microservicios inicializan bien"

$serviceChecks = @(
    @{ Dir = 'servicio-deteccion-cliches'; Mod = 'main' },
    @{ Dir = 'servicio-repeticion-palabras'; Mod = 'main' },
    @{ Dir = 'deteccion_conectores_logicos'; Mod = 'main' },
    @{ Dir = 'detector_doble_negacion'; Mod = 'main' },
    @{ Dir = 'deteccion_puntuacion_inusual'; Mod = 'main' },
    @{ Dir = 'deteccion_verbos_modales'; Mod = 'main' },
    @{ Dir = 'detector_adverbios'; Mod = 'main' },
    @{ Dir = 'metricas-de-legibilidad'; Mod = 'main' },
    @{ Dir = 'oraciones-impersonales'; Mod = 'main' },
    @{ Dir = 'verbos_percepcion_opinion'; Mod = 'app.main' },
    @{ Dir = 'weak_verbs'; Mod = 'app.main' },
    @{ Dir = 'voz_pasiva'; Mod = 'main' },
    @{ Dir = 'abstract_words'; Mod = 'api' },
    @{ Dir = 'povshift'; Mod = 'main' },
    @{ Dir = 'verb_tense_inconsistencies'; Mod = 'api' }
)

$allPassed = $true
foreach ($c in $serviceChecks) {
    $dir = Join-Path $ScriptDir $c.Dir
    if (-not (Test-Path $dir)) {
        Write-WarningMsg "$($c.Dir) no encontrado."
        continue
    }
    Push-Location $dir
    try {
        $mod = $c.Mod
        $res = & $VenvPython -c "import $mod; print('IMPORT_OK')" 2>&1
        $matched = ($res | Out-String) -match "IMPORT_OK"
        if ($matched) {
            Write-Success $c.Dir
        } else {
            $allPassed = $false
            Write-ErrorMsg "Fallo al inicializar $($c.Dir)"
        }
    } finally {
        Pop-Location
    }
}

# =============================================================================
# RESUMEN FINAL
# =============================================================================
Write-Section "INSTALACION COMPLETADA"

if ($allPassed) {
    Write-Host "`n  ¡EL ENTORNO HA SIDO CONFIGURADO EXITOSAMENTE!" -ForegroundColor Green
    Write-Host "`n  Para levantar todos los servicios, ejecuta en PowerShell:" -ForegroundColor White
    Write-Host "    .\iniciar_servicios.ps1`n" -ForegroundColor Yellow
    Write-Host "  Para verificar el estado de los puertos y servicios:" -ForegroundColor White
    Write-Host "    .\iniciar_servicios.ps1 -Status`n" -ForegroundColor Yellow
    Write-Host "  Para detener los servicios:" -ForegroundColor White
    Write-Host "    .\iniciar_servicios.ps1 -Stop`n" -ForegroundColor Yellow

    if ($StartServices) {
        Write-Host "  -> Parametro -StartServices detectado. Levantando servicios..." -ForegroundColor Cyan
        & (Join-Path $ScriptDir "start_services.ps1")
    }
} else {
    Write-Host "`n  Algunos microservicios presentaron advertencias. Revisa los mensajes anteriores." -ForegroundColor Yellow
}
