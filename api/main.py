from  fastapi import FastAPI
from typing import Optional
from api.loader.cargador_datos import CargadorDatos
from api.dashboard import Dashboard
from api.preprocesar import Preprocesador
    
app = FastAPI(title = "API Biblia")

cargador = CargadorDatos()
df = cargador.cargar_biblia()

preprocesador = Preprocesador(df)
df = preprocesador.preprocesar()

dashboard = Dashboard(df)

@app.get("/api/dashboard/versiculos-por-libro")
def versiculos_por_libro(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    resultado = dashboard.cantidad_versiculos_libro(testamento, libro, capitulo)
    return resultado.to_dict()

@app.get("/api/dashboard/longitud-promedio")
def longitudPromedio(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    resultado = dashboard.longitud_promedio_versiculos_libro(testamento, libro, capitulo)
    return resultado.to_dict()

@app.get("/api/dashboard/top-palabras")
def top_palabras(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    top = dashboard.top_palabras_frecuentes(n = 10, testamento = testamento, libro = libro, capitulo = capitulo)
    return [{"Palabra": palabra, "Frecuencia": frecuencia} for palabra, frecuencia in top]

@app.get("/api/dashboard/nube-palabras")
def nube_palabras(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[str] = None):
    resultado = dashboard.nube_palabras(n = 100, testamento = testamento, libro = libro, capitulo = capitulo)
    return resultado