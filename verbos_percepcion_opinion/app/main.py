from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.perception_opinion_api import router as perception_opinion_router

app = FastAPI()
# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(perception_opinion_router)
