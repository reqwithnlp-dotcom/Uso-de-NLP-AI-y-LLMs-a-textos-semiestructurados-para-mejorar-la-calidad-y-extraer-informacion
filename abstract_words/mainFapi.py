from fastapi import FastAPI
from pydantic import BaseModel
from main import extract_abstract_words

app = FastAPI()

class TextInput(BaseModel):
    text: str
    threshold: float = 3.4

@app.post("/predict")
def predict(data: TextInput):

    results = extract_abstract_words(
        text=data.text,
        threshold=data.threshold
    )

    return {
        "results": results
    }