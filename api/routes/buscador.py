from fastapi import APIRouter, Query
from api.services.buscador_service import Buscador
from api.df import get_df

router = APIRouter()
buscador = Buscador(get_df())

@router.get("/buscador/buscar")
def buscar_versiculos(frase: str = Query(..., min_length=1, description="Frase a buscar"), n: int = Query(20, ge=1, le=100)):
    resultado = buscador.buscar(frase, n)
    columnas = ["nombre_libro", "capitulo", "versiculo", "texto_versiculo", "similitud"]
    return resultado[columnas].to_dict(orient="records")