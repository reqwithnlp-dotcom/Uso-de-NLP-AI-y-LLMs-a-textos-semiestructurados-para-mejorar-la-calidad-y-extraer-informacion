from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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