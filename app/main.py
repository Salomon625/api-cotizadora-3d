import json

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.calculadora import calcular_cotizacion
from app.config_store import cargar_config, guardar_config
from app.models import CotizacionRequest

app = FastAPI(
    title="API Cotizadora de Impresiones 3D",
    version="3.0.0",
    description="Backend JSON para cotizar impresiones 3D desde apps moviles o clientes externos.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API Cotizadora de Impresiones 3D funcionando",
        "version": "3.0.0",
        "docs": "/docs",
        "estado": "/api/status",
        "cotizar": "/api/cotizar",
        "configuracion": "/api/config",
        "materiales": "/api/materiales",
    }


@app.head("/")
def inicio_head():
    return Response(status_code=200)


@app.get("/salud")
def salud():
    return {"estado": "ok"}


@app.get("/api/status")
def status():
    config = cargar_config()
    return {
        "estado": "ok",
        "version": "3.0.0",
        "materiales_disponibles": len(config["materiales"]),
    }


@app.get("/api/materiales")
def obtener_materiales():
    return cargar_config()["materiales"]


@app.get("/api/config")
def obtener_config():
    return cargar_config()


@app.put("/api/config")
async def actualizar_config(request: Request):
    config = await request.json()
    guardar_config(config)
    return {"mensaje": "Configuracion guardada", "config": config}


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
