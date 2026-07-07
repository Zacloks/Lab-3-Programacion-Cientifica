# Laboratorio 3 - Programación Científica

## Integrantes

- Miguel Valenzuela
- Juan Alvarado
- Roger Villarroel

---

## Descripción

Sistema cliente-servidor para analizar el corpus bíblico WEB (World English Bible). La API en FastAPI procesa el texto; Streamlit solo pide datos y los muestra, sin guardar nada.
Cuatro secciones: dashboard con estadísticas y nube de palabras (filtrable por testamento, libro y capítulo), buscador de versículos similares a una frase, visualizador PCA/Word2Vec en 2D y 3D, y generador de versículos con n-gramas. El texto se representa con TF-IDF y Word2Vec, y todo el cálculo corre en la API.

---

## Dataset

Se utiliza el dataset **Bible**, disponible en [Kaggle](https://www.kaggle.com/datasets/oswinrh/bible).

Los tres archivos van en la carpeta `api/data/`:

| Archivo | Contenido |
|---|---|
| `t_web.csv` | Versículos: id, libro, capítulo, versículo, texto |
| `key_english.csv` | Nombre y testamento por libro |
| `key_genre_english.csv` | Género literario por libro |

Cada versículo queda asociado a su libro, capítulo, testamento y género tras la carga.

---

## Estructura

```text
Lab-3-Programacion-Cientifica/
├── api/
│   ├── data/
│   │   ├── t_web.csv
│   │   ├── key_english.csv
│   │   └── key_genre_english.csv
│   ├── loader/
│   │   └── cargador_datos.py
│   ├── services/
│   │   ├── preprocesar.py
│   │   ├── dashboard_service.py
│   │   ├── buscador_service.py
│   │   ├── generador_service.py
│   │   └── visualizador_service.py
│   ├── routes/
│   │   ├── dashboard.py
│   │   ├── buscador.py
│   │   ├── generador.py
│   │   └── visualizador.py
│   ├── df.py
│   ├── main.py
│   ├── requirements.txt
│   └── environment.yml
│
└── app/
    ├── views/
    │   ├── dashboard_view.py
    │   ├── buscador_view.py
    │   ├── generador_view.py
    │   └── visualizador_view.py
    ├── api_client.py
    ├── main.py
    ├── .env
    ├── requirements.txt
    └── environment.yml
```

| Módulo | Responsabilidad |
|---|---|
| `api/loader` | Carga y unión de los CSV |
| `api/services` | Lógica: preprocesamiento, dashboard, buscador, generador y visualizador |
| `api/routes` | Endpoints REST, uno por módulo |
| `api/df.py` | Carga el corpus una vez y lo comparte entre servicios |
| `api/main.py` | Crea la app y registra los routers |
| `app/views` | Una vista de Streamlit por sección |
| `app/api_client.py` | Llamadas HTTP hacia la API |
| `app/main.py` | Navegación entre vistas |

---

## Requisitos

- Python 3.12

**API (`api/requirements.txt`):**

- fastapi
- uvicorn
- pandas
- numpy
- scikit-learn
- gensim
- nltk

**App (`app/requirements.txt`):**

- streamlit
- requests
- python-dotenv
- pandas
- wordcloud
- plotly

---

## Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/Zacloks/Lab-3-Programacion-Cientifica.git
cd Lab-3-Programacion-Cientifica
```

### 2. Instalar dependencias

La API y la app tienen dependencias separadas. Instala cada una en su propio entorno.

**Con conda:**

```bash
conda env create -f api/environment.yml
conda env create -f app/environment.yml
```

Esto crea los entornos `api` y `app`.

**Con pip:**

```bash
pip install -r api/requirements.txt
pip install -r app/requirements.txt
```

### 3. Ejecutar

La API y la app corren en dos terminales, ambas desde la raíz del proyecto. Levanta primero la API.

**Terminal 1 (API):**

```bash
conda activate api
uvicorn api.main:app --reload
```

La API queda en `http://127.0.0.1:8000`. La documentación interactiva está en `http://127.0.0.1:8000/docs`.

**Terminal 2 (app):**

```bash
conda activate app
streamlit run app/main.py
```

La app abre en `http://localhost:8501`. La dirección de la API se lee desde `app/.env` (variable `API_URL`).