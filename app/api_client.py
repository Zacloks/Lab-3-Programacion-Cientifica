import requests

REQUEST_TIMEOUT = 20

def api_get(base_url: str, path: str, params: dict | None = None):
    response = requests.get(
        f"{base_url.rstrip('/')}{path}",
        params = params,
        timeout = REQUEST_TIMEOUT
    )
    response.raise_for_status()
    return response.json()

#Dashboard
def versiculos_por_libro(base_url: str, params: dict | None = None):
    return api_get(base_url, "/dashboard/versiculos-por-libro", params)

def longitud_promedio(base_url: str, params: dict | None = None):
    return api_get(base_url, "/dashboard/longitud-promedio", params)

def top_palabras(base_url: str, params: dict | None = None):
    return api_get(base_url, "/dashboard/top-palabras", params)

def nube_palabras(base_url: str, params: dict | None = None):
    return api_get(base_url, "/dashboard/nube-palabras", params)

#Buscador
def buscar(base_url: str, frase: str, n: int = 20):
    return api_get(base_url, "/buscador/buscar", {"frase": frase, "n": n})

#Generador
def generador_modelos(base_url: str):
    return api_get(base_url, "/generador/modelos")

def generar(base_url: str, modelo: str, palabra_inicial: str, largo_maximo: int):
    return api_get(base_url, "/generador/generar", {
        "modelo": modelo,
        "palabra_inicial": palabra_inicial,
        "largo_maximo": largo_maximo,
    })