# Installation

## Create virtual environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows (PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Windows (CMD)

```cmd
python -m venv venv
venv\Scripts\activate.bat
```

---

## Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## Install project dependencies

```bash
pip install -r requirements.txt
```

---

## Download SpaCy English model

```bash
python -m spacy download en_core_web_sm
```

---

## Verify installation

```bash
python -m spacy validate
```

You should see the `en_core_web_sm` model installed and compatible with the current SpaCy version.

---

## Run tests

```bash
pytest
```

Or with verbose output:

```bash
pytest -v
```