from fastapi import FastAPI

from .api.perception_opinion_api import router as perception_opinion_router

app = FastAPI()
app.include_router(perception_opinion_router)
