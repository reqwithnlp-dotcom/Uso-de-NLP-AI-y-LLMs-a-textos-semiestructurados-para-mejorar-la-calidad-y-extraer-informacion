# Detección y clasificación de adverbios
Servicio que se encarga de detectar los *adverbios* presentes en un texto en inglés, devolviendo también la clasificación de dichos adverbios. Por ejemplo al adverbio "here" es del tipo "Place"

### Instalación
1. Tenés que abrir la carpeta del servicio en la terminal
```bash
cd detector_adverbios
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

2. Levanta la API con FastAPI para probar el endpoint
```bash
python main.py 
```

3. Para testear el endpoint mediante una interfaz, accede a la siguiente URL
[http://localhost:8000/docs](http://localhost:8000/docs)

4. Dentro del cuadro del endpoint, debes pulsar el botón "Try it out" para poder ingresar el texto que desees probar reemplazando la palabra "string"

5. Luego presiona el botón "Execute" para que debajo se muestre la salida con la lista de adverbios y sus categorías

6. 