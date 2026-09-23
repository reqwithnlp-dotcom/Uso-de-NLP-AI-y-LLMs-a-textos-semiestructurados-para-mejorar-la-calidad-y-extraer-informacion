from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.weak_verbs import router as weak_verbs_router


app = FastAPI()
#Permitir CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(weak_verbs_router)

