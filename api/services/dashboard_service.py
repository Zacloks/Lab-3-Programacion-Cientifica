from collections import Counter

class Dashboard:
    def __init__(self, df_biblia):
        self.df = df_biblia
        
        self.df["longitud_versiculos"] = self.df["texto_versiculo"].str.len()
        
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
        return df_f.groupby("nombre_libro")["versiculo"].count()
    
    def longitud_promedio_versiculos_libro(self, testamento = None, libro = None, capitulo = None):
        df_f = self.filtrar_df(testamento, libro, capitulo)
        return df_f.groupby("nombre_libro")["longitud_versiculos"].mean()

    def top_palabras_frecuentes(self, n = 10, testamento = None, libro = None, capitulo = None):
        df_f = self.filtrar_df(testamento, libro, capitulo)
        contador = Counter()
        for tokens in df_f["tokens"]:
            contador.update(tokens)
        return contador.most_common(n)

    def nube_palabras(self, n = 100, testamento = None, libro = None, capitulo = None):
        df_f = self.filtrar_df(testamento, libro, capitulo)
        contador = Counter()
        
        for tokens in df_f["tokens"].dropna():
            if isinstance(tokens, list):
                contador.update(tokens)
            else:
                contador.update(str(tokens).split())
        
        return dict(contador.most_common(n))
        