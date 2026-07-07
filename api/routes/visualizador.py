from fastapi import APIRouter, Query
from api.services.visualizador_service import Visualizador
from api.df import get_df

router = APIRouter()
visualizador = Visualizador(get_df())

@router.get("/visualizador/coordenadas")
def coordenadas(metodo: str = Query("tfidf", pattern="^(tfidf|word2vec)$"), dim: int = Query(2, ge=2, le=3)):
    return visualizador.coordenadas(metodo, dim)
