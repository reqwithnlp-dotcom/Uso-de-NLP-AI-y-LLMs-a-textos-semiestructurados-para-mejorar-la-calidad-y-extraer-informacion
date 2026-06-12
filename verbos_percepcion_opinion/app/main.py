from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.perception_opinion_api import router as perception_opinion_router

app = FastAPI()
# Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"],  # Incluye OPTIONS
    allow_headers=["*"],
)
app.include_router(perception_opinion_router)
