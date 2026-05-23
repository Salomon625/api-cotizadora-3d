from pydantic import BaseModel, Field


class MaterialCotizado(BaseModel):
    material: str = Field(..., examples=["pla"])
    color: str | None = Field(None, examples=["negro"])
    peso_gramos: float = Field(..., gt=0, examples=[150])


class CotizacionRequest(BaseModel):
    nombre_producto: str = Field(..., examples=["Soporte para celular"])
    materiales: list[MaterialCotizado]
    cantidad: int = Field(1, gt=0, examples=[1])
    tiempo_horas: float | None = Field(None, gt=0, examples=[1])
    incluir_envio: bool = Field(False)