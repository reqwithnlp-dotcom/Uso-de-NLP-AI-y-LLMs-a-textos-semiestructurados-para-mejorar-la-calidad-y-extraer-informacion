from fastapi import FastAPI

from .api.weak_verbs import router as weak_verbs_router

app = FastAPI()
app.include_router(weak_verbs_router)
