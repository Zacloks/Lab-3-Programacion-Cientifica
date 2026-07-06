import pandas as pd
from collections import Counter

class Dashboard:
    def __init__(self, df_biblia):
        self.df = df_biblia

    def cantidad_versiculos_libro(self):
        return self.df.groupby("numero_libro")["versiculo"].count()
    
    def longitud_promedio_versiculos_libro(self):
        self.df["longitud_versiculos"] = self.df["texto_versiculo"].apply(len)
        return self.df.groupby("nombre_libro")["longitud_versiculos"].mean()

    def top_palabras_frecuentes(self, n = 20):
        contador = Counter()
        for tokens in self.df["tokens"]:
            contador.update(tokens)
        return contador.most_common(n)

    def nube_palabras(self):
        pass