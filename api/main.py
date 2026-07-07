from fastapi import FastAPI
from api.routes.dashboard import router as dashboard_router
from api.routes.buscador import router as buscador_router
from api.routes.generador import router as generador_router

app = FastAPI(title="API Biblia")

app.include_router(dashboard_router)
app.include_router(buscador_router)
app.include_router(generador_router)