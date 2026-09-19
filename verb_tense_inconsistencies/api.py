from fastapi import FastAPI

from models.request import AnalyzeRequest
from models.response import AnalyzeResponse

from service import VerbTenseService


app = FastAPI(

    title="Verb Tense Inconsistency Detector",

    version="1.0.0"

)

service = VerbTenseService()


@app.post(

    "/analyze",

    response_model=AnalyzeResponse

)
def analyze(request: AnalyzeRequest):

    return service.analyze(request.text)