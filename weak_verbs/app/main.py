from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.weak_verbs import router as weak_verbs_router


app = FastAPI()
#Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # o ["*"] para desarrollo
    allow_credentials=True,
    allow_methods=["*"], # Incluye OPTIONS
    allow_headers=["*"],
)
app.include_router(weak_verbs_router)

