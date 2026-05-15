from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# ---------------------------------------
# CORS
# ---------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# ---------------------------------------
# MODELO
# ---------------------------------------

class Mensaje(BaseModel):
    texto: str

# ---------------------------------------
# ENDPOINT
# ---------------------------------------

@app.post("/analizar")

def analizar(data: Mensaje):

    texto = data.texto.lower()

    toxicidad = round(random.uniform(0,1),2)
    sesgo = round(random.uniform(0,1),2)
    transparencia = round(random.uniform(0,1),2)

    impacto = round(
        (toxicidad + sesgo)/2,
        2
    )

    # Riesgo
    palabras_peligrosas = [
        "manipular",
        "engañar",
        "fraude",
        "controlar",
        "mentir"
    ]

    riesgo = "Seguro"

    for palabra in palabras_peligrosas:

        if palabra in texto:
            riesgo = "Alto"

    # Motor de reglas
    if toxicidad > 0.80:

        accion = "Bloquear"

    elif riesgo == "Alto":

        accion = "Escalar"

    else:

        accion = "Aprobar"

    respuesta_ia = f"""
    El sistema detectó riesgo {riesgo}.
    Acción ejecutada: {accion}.
    """

    return {

        "mensaje": texto,

        "riesgo": riesgo,

        "accion": accion,

        "toxicidad": toxicidad,

        "sesgo": sesgo,

        "transparencia": transparencia,

        "impacto": impacto,

        "respuesta_ia": respuesta_ia
    }
    
