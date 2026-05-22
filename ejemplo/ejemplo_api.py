from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Hola mundo"}

@app.get("/suma")
def suma(a: int, b: int):
    return {"resultado": a + b}