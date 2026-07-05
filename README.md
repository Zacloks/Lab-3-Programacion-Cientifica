# Laboratorio 3 - Programación Científica

## Integrantes

- Miguel Valenzuela
- Juan Alvarado
- Roger Villarroel

---

## Descripción

Sistema cliente-servidor para analizar el corpus bíblico en su versión World English Bible (WEB). Una API en FastAPI hace todo el procesamiento del texto y una aplicación en Streamlit funciona como interfaz: le pide los datos a la API y los muestra. Streamlit no almacena el corpus, solo lo que muestra en cada momento.

La aplicación tiene cuatro secciones: un dashboard con estadísticas del corpus y nube de palabras, filtrable por testamento, libro y capítulo; un buscador que devuelve los versículos más parecidos a una frase; un visualizador que proyecta los versículos en 2D y 3D con PCA y Word2Vec; y un generador de versículos basado en modelos de n-gramas. La representación del texto se hace con TF-IDF y Word2Vec, y todo el cálculo ocurre en la API.

---

## Dataset

Se utiliza el dataset **Bible**, disponible en [Kaggle](https://www.kaggle.com/datasets/oswinrh/bible).

Los tres archivos van en la carpeta `data/`:

| Archivo | Contenido |
|---|---|
| `t_web.csv` | Versículos: id, libro, capítulo, versículo, texto |
| `key_english.csv` | Nombre y testamento por libro |
| `key_genre_english.csv` | Género literario por libro |

Cada versículo queda asociado a su libro, capítulo, testamento y género tras la carga.