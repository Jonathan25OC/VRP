from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from app.vrp import vrp_voraz
from app.models import VRPRequest
from app.map_utils import generar_mapa
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.post("/optimizar-rutas")
def optimizar_rutas(request: VRPRequest):
    rutas = vrp_voraz(request.coord, request.pedidos, request.almacen, request.max_carga)
    return {"rutas": rutas}

@app.post("/mapa", response_class=HTMLResponse)
def mapa(request: VRPRequest):
    rutas = vrp_voraz(request.coord, request.pedidos, request.almacen, request.max_carga)
    mapa_html = generar_mapa(rutas, request.coord, request.almacen)
    return HTMLResponse(content=mapa_html, status_code=200)