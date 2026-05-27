# API Cotizadora 3D

API para cotizar impresiones 3D con materiales, desperdicio, electricidad, repuestos, mano de obra, margen de ganancia y envio.

## Ejecutar en local

```powershell
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

## Rutas principales

- `/` estado general
- `/docs` documentacion automatica
- `/admin` panel de configuracion
- `/api/cotizar` endpoint de cotizacion
