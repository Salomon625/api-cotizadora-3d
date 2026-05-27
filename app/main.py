import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.calculadora import calcular_cotizacion
from app.config_store import cargar_config, guardar_config
from app.models import CotizacionRequest

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(
    title="API Cotizadora de Impresiones 3D",
    version="2.0.0",
    description="API para cotizar impresiones 3D con materiales, desperdicio, luz, repuesto, mano de obra y envio.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/")
def inicio():
    return {
        "mensaje": "API Cotizadora de Impresiones 3D funcionando",
        "docs": "/docs",
        "admin": "/admin",
    }


@app.get("/salud")
def salud():
    return {"estado": "ok"}


async def leer_cotizacion_request(request: Request):
    contenido = await request.body()

    if not contenido:
        return None

    try:
        return CotizacionRequest.model_validate_json(contenido)
    except ValidationError as error:
        return JSONResponse(
            status_code=422,
            content={"error": "Datos invalidos", "detalle": error.errors()},
        )
    except json.JSONDecodeError:
        try:
            datos_json = json.loads(contenido.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

    try:
        return CotizacionRequest.model_validate(datos_json)
    except ValidationError as error:
        return JSONResponse(
            status_code=422,
            content={"error": "Datos invalidos", "detalle": error.errors()},
        )


@app.post("/api/cotizar")
async def cotizar(request: Request):
    datos = await leer_cotizacion_request(request)

    if datos is None:
        return JSONResponse(
            status_code=400,
            content={"error": "No se recibio una cotizacion valida en JSON"},
        )

    if isinstance(datos, JSONResponse):
        return datos

    return calcular_cotizacion(datos)


@app.get("/api/cotizar")
def ayuda_cotizar():
    return {
        "mensaje": "Este endpoint recibe cotizaciones con metodo POST.",
        "ejemplo": {
            "nombre_producto": "Mini mesa",
            "cantidad": 3,
            "incluir_envio": True,
            "materiales": [
                {"material": "tpu", "color": "gris", "peso_gramos": 400},
                {
                    "material": "pla_carbono",
                    "color": "negro con carbono 4%",
                    "peso_gramos": 150,
                },
            ],
        },
    }


@app.options("/api/cotizar")
def opciones_cotizar():
    return {"estado": "ok"}


@app.get("/api/config")
def obtener_config():
    return cargar_config()


@app.put("/api/config")
async def actualizar_config(request: Request):
    config = await request.json()
    guardar_config(config)
    return {"mensaje": "Configuracion guardada", "config": config}


@app.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

