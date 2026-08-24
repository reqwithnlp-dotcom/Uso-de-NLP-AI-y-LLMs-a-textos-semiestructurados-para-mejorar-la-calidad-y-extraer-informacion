from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from src.detector import AdverbDetector

app = FastAPI(
    title="Detección de Adverbios",
    description="Servicio que detecta y clasifica adverbios en un texto en inglés.",
    version="1.0.0",
)

detector = AdverbDetector()

class TextoRequest(BaseModel):
    texto: str

class Adverbio(BaseModel):
    word: str
    category: str

class AnalisisResponse(BaseModel):
    adverbs: List[Adverbio]

#------- Endpoints -------

@app.get("/")
def root():
    return {"mensaje": "Servicio de detección de adverbios activo"}

@app.post("/analizar", response_model=AnalisisResponse)
def analizar_texto(request: TextoRequest):
    lista_resultados = detector.analyze_sentence(request.texto)
    
    adverbios_formateados = []
    for resultado in lista_resultados:
        adverbios_formateados.append(Adverbio(word=resultado[0], category=resultado[1]))
        
    return {"adverbs": adverbios_formateados}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
