from fastapi import FastAPI, Query
from typing import Optional
from api.loader.cargador_datos import CargadorDatos
from api.dashboard import Dashboard
from api.preprocesar import Preprocesador
from api.buscador import Buscador

app = FastAPI(title = "API Biblia")

cargador = CargadorDatos()
df = cargador.cargar_biblia()

preprocesador = Preprocesador(df)
df = preprocesador.preprocesar()

dashboard = Dashboard(df)

buscador = Buscador(df)

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

@app.get("/api/buscador/buscar")
def buscar_versiculos(frase: str = Query(..., min_length=1, description="Frase a buscar"),n: int = Query(20, ge=1, le=100),):
    resultado = buscador.buscar(frase, n)
    columnas = ["nombre_libro", "capitulo", "versiculo", "texto_versiculo", "similitud"]
    return resultado[columnas].to_dict(orient="records")