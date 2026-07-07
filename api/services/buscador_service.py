import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from api.services.preprocesar import Preprocesador

STOP_WORDS = list(stopwords.words("english"))

class Buscador:
    def __init__(self, df):
        self.df = df
        self.preprocesador = Preprocesador(None)
        self.vectorizador = TfidfVectorizer(stop_words=STOP_WORDS)
        self.matriz_tfidf = self.vectorizador.fit_transform(df["texto_preprocesado"])

    def buscar(self, frase, n=20):
        frase_procesada = self.preprocesador.aplicar_pipeline(frase)
        vector_consulta = self.vectorizador.transform([frase_procesada])
        similitud_consulta = cosine_similarity(vector_consulta, self.matriz_tfidf)[0]

        indices_ordenados = np.argsort(similitud_consulta)[::-1][:n]

        resultados = self.df.iloc[indices_ordenados].copy()
        resultados["similitud"] = similitud_consulta[indices_ordenados]

        return resultados