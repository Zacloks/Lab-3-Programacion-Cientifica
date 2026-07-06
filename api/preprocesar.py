import nltk
nltk.download("stopwords")
from nltk.corpus import stopwords
import re

STOP_WORDS = set(stopwords.words("english"))

class Preprocesador:
    def __init__(self, df):
        self.df = df

    def aplicar_pipeline(self, texto):
        texto = re.sub(r"\{[^}]*\}", "", texto).lower()
        texto = re.sub(r"[^a-z\s]", " ", texto)
        texto = re.sub(r"\s+", " ", texto).strip()
        return texto

    def preprocesar(self):
        self.df["texto_preprocesado"] = self.df["texto_versiculo"].apply(self.aplicar_pipeline)
        self.df["tokens"] = self.df["texto_preprocesado"].apply(
            lambda texto: [palabra for palabra in texto.split() if palabra not in STOP_WORDS]
        )
        
        return self.df