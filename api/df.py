from api.loader.cargador_datos import CargadorDatos
from api.services.preprocesar import Preprocesador

_df = None

def get_df():
    global _df
    if _df is None:
        cargador = CargadorDatos()
        df = cargador.cargar_biblia()
        preprocesador = Preprocesador(df)
        _df = preprocesador.preprocesar()
    return _df