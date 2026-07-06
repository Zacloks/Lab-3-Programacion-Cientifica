"""
from fastapi import FastAPI
app = FastAPI()
"""

from api.loader.cargador_datos import CargadorDatos
from api.dashboard import Dashboard
from api.preprocesar import Preprocesador

def main():
    cargador = CargadorDatos()
    df = cargador.cargar_biblia()
    preprocesador = Preprocesador(df)
    df = preprocesador.preprocesar()
    dashboard = Dashboard(df)
    print(dashboard.cantidad_versiculos_libro())
    print(dashboard.longitud_promedio_versiculos_libro())
    print(dashboard.top_palabras_frecuentes())

if __name__ == "__main__":
    main()