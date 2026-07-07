from typing import Optional
from fastapi import APIRouter
from api.services.dashboard_service import Dashboard
from api.df import get_df

router = APIRouter()
dashboard = Dashboard(get_df())

@router.get("/dashboard/versiculos-por-libro")
def versiculos_por_libro(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    resultado = dashboard.cantidad_versiculos_libro(testamento, libro, capitulo)
    return resultado.to_dict()

@router.get("/dashboard/longitud-promedio")
def longitud_promedio(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    resultado = dashboard.longitud_promedio_versiculos_libro(testamento, libro, capitulo)
    return resultado.to_dict()

@router.get("/dashboard/top-palabras")
def top_palabras(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    top = dashboard.top_palabras_frecuentes(n=10, testamento=testamento, libro=libro, capitulo=capitulo)
    return [{"Palabra": palabra, "Frecuencia": frecuencia} for palabra, frecuencia in top]

@router.get("/dashboard/nube-palabras")
def nube_palabras(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    resultado = dashboard.nube_palabras(n=100, testamento=testamento, libro=libro, capitulo=capitulo)
    return resultado