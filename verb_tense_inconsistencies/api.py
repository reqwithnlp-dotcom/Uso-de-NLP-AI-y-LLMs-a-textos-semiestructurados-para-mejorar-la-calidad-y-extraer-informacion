from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models.request import AnalyzeRequest
from models.response import AnalyzeResponse

from service import VerbTenseService


app = FastAPI(
    title="Verb Tense Inconsistency Detector",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

service = VerbTenseService()


@app.post(

    "/analyze",

    response_model=AnalyzeResponse

)
def analyze(request: AnalyzeRequest):

    return service.analyze(request.text)