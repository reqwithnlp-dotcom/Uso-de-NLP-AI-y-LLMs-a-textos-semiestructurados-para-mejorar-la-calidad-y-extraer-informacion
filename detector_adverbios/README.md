# Detección y clasificación de adverbios
Servicio que se encarga de detectar los *adverbios* presentes en un texto en inglés, devolviendo también la clasificación de dichos adverbios. Por ejemplo al adverbio "here" es del tipo "Place"

### Instalación
1. Tenés que abrir la carpeta del servicio en la terminal
```bash
cd deteccion_conectores_logicos
```

2. Crea un entorno virtual con Python 3.12

```bash
py -3.12 -m venv venv
```

3. Activa el entorno virtual
```bash
.\venv\Scripts\activate
```

4. Ahora vas a tener que instalar las dependencias
```bash
pip install -r requirements.txt
```

5. Descarga el modelo de lenguaje de Spacy que usa el servicio
```bash
python -m spacy download en_core_web_trf
```

### Uso del servicio
1. (Opcional) Si no tenés activado el entorno virtual, ejecutá la siguiente línea en la terminal dentro de la carpeta del servicio
```bash
.\venv\Scripts\activate
```

2. Ejecuta el servicio poniendo una oración en inglés entre comillas
```bash
python main.py "See you tomorrow at the library"
```
Esto devuelve - *[['tomorrow', 'Time']]*

3. Para correr los tests debes ejecutar la siguiente linea
```bash
pytest
```