import pandas as pd
from pathlib import Path

class CargadorDatos:
    def __init__(self, ruta = None):
        if ruta is None:
            self.ruta = Path(__file__).resolve().parent.parent / "data"
        else:
            self.ruta = ruta
    
    def cargar_biblia(self):
        df_versiculos = pd.read_csv(self.ruta / "t_web.csv")
        df_libros = pd.read_csv(self.ruta / "key_english.csv")
        df_generos = pd.read_csv(self.ruta / "key_genre_english.csv")

        df_libros = df_libros.rename(columns={"t": "testamento", "n": "nombre_libro"})

        df_biblia = df_versiculos.merge(df_libros, on="b").merge(df_generos, on="g").rename(columns={
            "b": "numero_libro", "c": "capitulo", "v": "versiculo",
            "t": "texto_versiculo", "g": "numero_genero", "n": "nombre_genero"
        })
        
        return df_biblia

