import pandas as pd
from collections import Counter

class Dashboard:
    def __init__(self, df_biblia):
        self.df = df_biblia
        
    def filtrar_df(self, testamento = None, libro = None, capitulo = None):
        df_filtrado = self.df.copy()
        
        if testamento:
            df_filtrado = df_filtrado[df_filtrado['testamento'] == testamento]
        
        if libro:
            df_filtrado = df_filtrado[df_filtrado['nombre_libro'] == libro]
        
        if capitulo:
            df_filtrado = df_filtrado[df_filtrado['capitulo'] == capitulo]
            
        return df_filtrado
        

    def cantidad_versiculos_libro(self, testamento = None, libro = None, capitulo = None):
        df_f = self.filtrar_df(testamento, libro, capitulo)
        return self.df.groupby("numero_libro")["versiculo"].count()
    
    def longitud_promedio_versiculos_libro(self, testamento = None, libro = None, capitulo = None):
        df_f = self.filtrar_df(testamento, libro, capitulo)
        return self.df.groupby("nombre_libro")["longitud_versiculos"].mean()

    def top_palabras_frecuentes(self, n = 20, testamento = None, libro = None, capitulo = None):
        df_f = self.filtrar_df(testamento, libro, capitulo)
        contador = Counter()
        for tokens in self.df["tokens"]:
            contador.update(tokens)
        return contador.most_common(n)

    def nube_palabras(self):
        pass