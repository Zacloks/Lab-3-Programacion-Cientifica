import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD, PCA
from gensim.models import Word2Vec
from api.services.buscador_service import STOP_WORDS

class Visualizador:
    def __init__(self, df, n_muestra=3000, semilla=42):
        self.df = df.reset_index(drop=True)

        tokens = [t if isinstance(t, list) else [] for t in self.df["tokens"]]
        textos = self.df["texto_preprocesado"].fillna("")

        vectorizador = TfidfVectorizer(stop_words=STOP_WORDS)
        matriz_tfidf = vectorizador.fit_transform(textos)
        self.coords_tfidf = {
            2: TruncatedSVD(n_components=2, random_state=semilla).fit_transform(matriz_tfidf),
            3: TruncatedSVD(n_components=3, random_state=semilla).fit_transform(matriz_tfidf),
        }

        modelo_w2v = Word2Vec(sentences=tokens, vector_size=100, window=5, min_count=2, workers=4, seed=semilla)
        vectores = np.array([self._vector_versiculo(t, modelo_w2v) for t in tokens])
        self.coords_w2v = {
            2: PCA(n_components=2).fit_transform(vectores),
            3: PCA(n_components=3).fit_transform(vectores),
        }

        rng = np.random.default_rng(semilla)
        n = min(n_muestra, len(self.df))
        self.indices_muestra = np.sort(rng.choice(len(self.df), size=n, replace=False))

    @staticmethod
    def _vector_versiculo(tokens, modelo):
        vectores = [modelo.wv[palabra] for palabra in tokens if palabra in modelo.wv]
        if not vectores:
            return np.zeros(modelo.vector_size)
        return np.mean(vectores, axis=0)

    def coordenadas(self, metodo="tfidf", dim=2):
        coords = (self.coords_tfidf if metodo == "tfidf" else self.coords_w2v)[dim]
        salida = []
        for i in self.indices_muestra:
            i = int(i)
            punto = {
                "x": float(coords[i][0]),
                "y": float(coords[i][1]),
                "nombre_libro": self.df["nombre_libro"].iloc[i],
                "testamento": self.df["testamento"].iloc[i],
            }
            if dim == 3:
                punto["z"] = float(coords[i][2])
            salida.append(punto)
        return salida
