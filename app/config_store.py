import json
from pathlib import Path

CONFIG_PATH = Path("data/config.json")

DEFAULT_CONFIG = {
    "general": {
        "precio_kwh_base": 1000,
        "margen_seguridad_luz": 0.30,
        "consumo_watts": 170,
        "gramos_impresos_por_hora": 170,

        "mano_obra_base_pedido": 20000,
        "mano_obra_extra_por_unidad": 5000,

        "valor_repuesto": 7500000,
        "horas_vida_util_repuesto": 3000,

        "margen_1_a_3": 0.70,
        "margen_4_a_9": 0.60,
        "margen_10_o_mas": 0.50,

        "desperdicio_base": 0.10,
        "desperdicio_extra_por_material": 0.06,

        "envio_minimo": 17000,
        "envio_por_100_cm3": 3500
    },
    "materiales": {
        "pla": {"nombre": "PLA+", "precio_kg": 89250, "densidad_g_cm3": 1.24, "origen": "4D-Lab", "colores": ["amarillo", "azul rey", "blanco", "gris", "negro", "rojo", "verde pino"]},
        "pla_ecologico": {"nombre": "PLA Ecologico", "precio_kg": 78750, "densidad_g_cm3": 1.24, "origen": "4D-Lab", "colores": ["color aleatorio ecologico"]},
        "pla_carbono": {"nombre": "PLA Carbono 4%", "precio_kg": 94500, "densidad_g_cm3": 1.28, "origen": "4D-Lab", "colores": ["negro con carbono 4%"]},
        "pla_marmol": {"nombre": "PLA Marmol", "precio_kg": 94500, "densidad_g_cm3": 1.25, "origen": "4D-Lab", "colores": ["marmol"]},
        "pla_seda": {"nombre": "PLA Seda", "precio_kg": 89250, "densidad_g_cm3": 1.24, "origen": "4D-Lab", "colores": ["azul silk", "bronce silk", "dorado silk", "rojo silk", "plateado"]},
        "pla_traslucido": {"nombre": "PLA Traslucido", "precio_kg": 89250, "densidad_g_cm3": 1.24, "origen": "4D-Lab", "colores": ["azul rey traslucido", "amarillo traslucido", "morado traslucido", "natural traslucido", "rojo traslucido", "verde petroleo traslucido"]},
        "pla_glitter": {"nombre": "PLA Glitter", "precio_kg": 89250, "densidad_g_cm3": 1.24, "origen": "4D-Lab", "colores": ["azul glitter", "verde glitter", "rojo glitter"]},
        "petg": {"nombre": "PETG", "precio_kg": 89250, "densidad_g_cm3": 1.28, "origen": "4D-Lab", "colores": ["amarillo", "azul rey", "blanco", "gris", "naranja", "negro", "rojo", "transparente", "verde pino"]},
        "abs": {"nombre": "ABS", "precio_kg": 89250, "densidad_g_cm3": 1.05, "origen": "4D-Lab", "colores": ["amarillo", "azul rey", "blanco hueso", "gris", "negro", "rojo", "verde pino"]},
        "tpu": {"nombre": "TPU Flexible", "precio_kg": 150938, "densidad_g_cm3": 1.15, "origen": "4D-Lab", "colores": ["amarillo traslucido", "azul rey", "blanco", "negro", "naranja traslucido", "rojo", "verde traslucido"]},
        "pp": {"nombre": "PP", "precio_kg": 118125, "densidad_g_cm3": 0.90, "origen": "4D-Lab", "colores": ["azul", "blanco", "gris", "natural", "negro", "rojo"]},
        "asa": {"nombre": "ASA", "precio_kg": 135000, "densidad_g_cm3": 1.08, "origen": "Importado", "colores": ["negro", "blanco", "gris", "natural"]},
        "nylon": {"nombre": "Nylon", "precio_kg": 170000, "densidad_g_cm3": 1.14, "origen": "Importado", "colores": ["natural", "negro", "blanco"]},
        "pc": {"nombre": "PC Policarbonato", "precio_kg": 220000, "densidad_g_cm3": 1.19, "origen": "Importado", "colores": ["transparente", "negro", "blanco"]}
    }
}


def cargar_config():
    if not CONFIG_PATH.exists():
        guardar_config(DEFAULT_CONFIG)

    with CONFIG_PATH.open("r", encoding="utf-8") as archivo:
        config = json.load(archivo)

    config["general"] = DEFAULT_CONFIG["general"] | config.get("general", {})
    config["materiales"] = DEFAULT_CONFIG["materiales"] | config.get("materiales", {})
    return config


def guardar_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as archivo:
        json.dump(config, archivo, indent=2, ensure_ascii=False)
    return config
