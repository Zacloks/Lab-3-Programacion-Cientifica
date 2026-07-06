import re
import random
from collections import Counter, defaultdict

INICIO = "<s>"
FIN = "</s>"

MODELOS = {
    "unigram": 1,
    "bigram": 2,
    "trigram": 3,
}


class GeneradorNgramas:
    """Modelo generativo de texto basado en n-gramas construido sobre el corpus biblico.

    Aprende, para cada contexto de n-1 palabras, la distribucion de la palabra
    siguiente. Al generar usa 'back-off': si el contexto de orden n no existe,
    retrocede a ordenes menores hasta llegar al unigrama.
    """

    def __init__(self, df, orden_maximo=3):
        self.orden_maximo = orden_maximo

        self.corpus = [
            texto.split()
            for texto in df["texto_preprocesado"]
            if isinstance(texto, str) and texto.strip()
        ]

        self.unigramas = Counter()
        for tokens in self.corpus:
            self.unigramas.update(tokens)

        self.modelos = {
            n: self._construir(n) for n in range(2, orden_maximo + 1)
        }

    def _construir(self, n):
        modelo = defaultdict(Counter)
        for tokens in self.corpus:
            secuencia = [INICIO] * (n - 1) + tokens + [FIN]
            for i in range(len(secuencia) - n + 1):
                contexto = tuple(secuencia[i:i + n - 1])
                siguiente = secuencia[i + n - 1]
                modelo[contexto][siguiente] += 1
        return modelo

    @staticmethod
    def _muestrear(contador):
        palabras = list(contador.keys())
        pesos = list(contador.values())
        return random.choices(palabras, weights=pesos, k=1)[0]

    def _siguiente(self, n, historial):
        for m in range(min(n, self.orden_maximo), 1, -1):
            modelo = self.modelos.get(m)
            if not modelo:
                continue
            tam = m - 1
            ultimos = historial[-tam:]
            if len(ultimos) < tam:
                ultimos = [INICIO] * (tam - len(ultimos)) + ultimos
            contador = modelo.get(tuple(ultimos))
            if contador:
                return self._muestrear(contador)
        return self._muestrear(self.unigramas)

    def modelos_disponibles(self):
        return [nombre for nombre, n in MODELOS.items() if n <= self.orden_maximo]

    def generar(self, modelo="bigram", palabra_inicial="", largo_maximo=30):
        if modelo not in MODELOS:
            raise ValueError(f"Modelo no soportado: {modelo}")
        n = MODELOS[modelo]
        largo_maximo = max(1, min(int(largo_maximo), 200))

        semilla = re.sub(r"[^a-z\s]", " ", (palabra_inicial or "").lower()).split()
        semilla = semilla[0] if semilla else ""
        semilla_conocida = (semilla in self.unigramas) if semilla else None

        historial = [semilla] if semilla else []

        while len(historial) < largo_maximo:
            if n == 1:
                siguiente = self._muestrear(self.unigramas)
            else:
                siguiente = self._siguiente(n, historial)

            if siguiente == FIN:
                if not historial:
                    continue  
                break  
            if siguiente == INICIO:
                continue
            historial.append(siguiente)

        return {
            "modelo": modelo,
            "n": n,
            "palabra_inicial": semilla,
            "palabra_inicial_conocida": semilla_conocida,
            "largo_maximo": largo_maximo,
            "cantidad_palabras": len(historial),
            "texto_generado": " ".join(historial),
        }
