import re
import random
from collections import Counter, defaultdict

MODELOS = {
    "unigram": 1,
    "bigram": 2,
    "trigram": 3,
}

class GeneradorNgramas:
    def __init__(self, df, orden_maximo=3):
        self.corpus = [
            texto.split()
            for texto in df["texto_preprocesado"]
            if isinstance(texto, str) and texto.strip()
        ]

        self.unigramas = Counter()
        for tokens in self.corpus:
            self.unigramas.update(tokens)

        self.modelos = {}
        for n in range(2, orden_maximo + 1):
            modelo = defaultdict(Counter)
            for tokens in self.corpus:
                for i in range(len(tokens) - n + 1):
                    contexto = tuple(tokens[i:i + n - 1])
                    modelo[contexto][tokens[i + n - 1]] += 1
            self.modelos[n] = modelo

    def generar(self, modelo="bigram", palabra_inicial="", largo_maximo=30):
        if modelo not in MODELOS:
            raise ValueError(f"Modelo no soportado: {modelo}")
        n = MODELOS[modelo]
        largo_maximo = max(1, min(int(largo_maximo), 200))

        semilla = re.sub(r"[^a-z\s]", " ", (palabra_inicial or "").lower()).split()
        semilla = semilla[0] if semilla else ""

        texto = [semilla] if semilla else []

        while len(texto) < largo_maximo:
            if n == 1:
                opciones = self.unigramas
            else:
                contexto = tuple(texto[-(n - 1):])
                opciones = self.modelos[n].get(contexto) or self.unigramas

            siguiente = random.choices(list(opciones), weights=list(opciones.values()))[0]
            texto.append(siguiente)

        return {
            "modelo": modelo,
            "palabra_inicial": semilla,
            "cantidad_palabras": len(texto),
            "texto_generado": " ".join(texto),
        }
