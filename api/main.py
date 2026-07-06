from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from api.loader.cargador_datos import CargadorDatos
from api.dashboard import Dashboard
from api.preprocesar import Preprocesador
from api.buscador import Buscador
from api.generador import GeneradorNgramas

app = FastAPI(title = "API Biblia")

cargador = CargadorDatos()
df = cargador.cargar_biblia()

preprocesador = Preprocesador(df)
df = preprocesador.preprocesar()

dashboard = Dashboard(df)

buscador = Buscador(df)

generador = GeneradorNgramas(df, orden_maximo = 3)

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
def nube_palabras(testamento: Optional[str] = None, libro: Optional[str] = None, capitulo: Optional[int] = None):
    resultado = dashboard.nube_palabras(n = 100, testamento = testamento, libro = libro, capitulo = capitulo)
    return resultado

@app.get("/api/buscador/buscar")
def buscar_versiculos(frase: str = Query(..., min_length=1, description="Frase a buscar"),n: int = Query(20, ge=1, le=100),):
    resultado = buscador.buscar(frase, n)
    columnas = ["nombre_libro", "capitulo", "versiculo", "texto_versiculo", "similitud"]
    return resultado[columnas].to_dict(orient="records")

@app.get("/api/generador/modelos")
def generador_modelos():
    return generador.modelos_disponibles()

@app.get("/api/generador/generar")
def generar_versiculo(
    modelo: str = Query("bigram", description="unigram, bigram o trigram"),
    palabra_inicial: str = Query("", description="Palabra inicial (opcional)"),
    largo_maximo: int = Query(30, ge=1, le=200, description="Maximo de palabras a generar"),
):
    try:
        return generador.generar(modelo, palabra_inicial, largo_maximo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))