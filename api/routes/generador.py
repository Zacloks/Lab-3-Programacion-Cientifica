from fastapi import APIRouter, Query, HTTPException
from api.services.generador_service import GeneradorNgramas
from api.df import get_df

router = APIRouter()
generador = GeneradorNgramas(get_df(), orden_maximo=3)

@router.get("/generador/generar")
def generar_versiculo(
    modelo: str = Query("bigram", description="unigram, bigram o trigram"),
    palabra_inicial: str = Query("", description="Palabra inicial (opcional)"),
    largo_maximo: int = Query(30, ge=1, le=200, description="Maximo de palabras a generar"),
):
    try:
        return generador.generar(modelo, palabra_inicial, largo_maximo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))