"""
Punto de entrada del microservicio.

Uso:
    python main.py
o directamente:
    uvicorn service.api:app --reload
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("service.api:app", host="127.0.0.1", port=8000, reload=True)
