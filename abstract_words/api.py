from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel

from service import (
    setup,
    extract_abstract_words
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Initializing abstract words service...")
    setup()

    print("Service initialized")

    yield

    print("Shutting down service...")


app = FastAPI(lifespan=lifespan)

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict(data: TextInput):

    results = extract_abstract_words(
        text=data.text,
        threshold=3
    )

    return {
        "results": results
    }