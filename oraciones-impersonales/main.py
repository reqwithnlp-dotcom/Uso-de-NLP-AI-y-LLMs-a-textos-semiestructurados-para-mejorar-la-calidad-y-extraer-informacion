"""
Punto de entrada del microservicio (arranque plano, igual que `ejemplo/`).

Reexporta el objeto `app` para poder levantarlo desde la raíz del servicio
sin conocer la estructura interna (service/, model/):

    uvicorn main:app --reload

o directamente:

    python main.py
"""

import uvicorn

from service.api import app  # noqa: F401  (reexport para `uvicorn main:app`)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
