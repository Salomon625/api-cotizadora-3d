from app.config_store import cargar_config


def calcular_margen(cantidad, general):
    if cantidad >= 10:
        return general["margen_10_o_mas"]
    if cantidad >= 4:
        return general["margen_4_a_9"]
    return general["margen_1_a_3"]


def calcular_cotizacion(datos):
    config = cargar_config()
    general = config["general"]
    materiales_config = config["materiales"]

    if not datos.materiales:
        return {"error": "Debes enviar al menos un material"}

    cantidad_materiales = len(datos.materiales)
    desperdicio = general["desperdicio_base"] + (
        max(cantidad_materiales - 1, 0) * general["desperdicio_extra_por_material"]
    )

    peso_total = 0
    volumen_total_cm3 = 0
    costo_material_total = 0
    detalle_materiales = []

    for item in datos.materiales:
        codigo = item.material.lower().strip()

        if codigo not in materiales_config:
            return {
                "error": "Material no disponible",
                "material_recibido": item.material,
                "materiales_disponibles": list(materiales_config.keys()),
            }

        material = materiales_config[codigo]
        peso_con_desperdicio = item.peso_gramos * (1 + desperdicio)
        volumen = peso_con_desperdicio / material["densidad_g_cm3"]
        costo = (peso_con_desperdicio * material["precio_kg"]) / 1000

        peso_total += peso_con_desperdicio
        volumen_total_cm3 += volumen
        costo_material_total += costo

        detalle_materiales.append({
            "material": codigo,
            "nombre": material["nombre"],
            "color": item.color,
            "origen": material["origen"],
            "peso_base_gramos": round(item.peso_gramos, 2),
            "peso_con_desperdicio_gramos": round(peso_con_desperdicio, 2),
            "densidad_g_cm3": material["densidad_g_cm3"],
            "volumen_cm3": round(volumen, 2),
            "precio_kg": material["precio_kg"],
            "costo": round(costo, 2),
        })

    tiempo_horas = datos.tiempo_horas
    if tiempo_horas is None:
        tiempo_horas = peso_total / general["gramos_impresos_por_hora"]

    precio_kwh = general["precio_kwh_base"] * (1 + general["margen_seguridad_luz"])
    costo_luz = (general["consumo_watts"] / 1000) * tiempo_horas * precio_kwh

    costo_repuesto_hora = (
        general["valor_repuesto"] / general["horas_vida_util_repuesto"]
    )
    costo_repuesto = costo_repuesto_hora * tiempo_horas

    costo_mano_obra_pedido = (
        general["mano_obra_base_pedido"]
        + max(datos.cantidad - 1, 0) * general["mano_obra_extra_por_unidad"]
    )
    costo_mano_obra_unidad = costo_mano_obra_pedido / datos.cantidad

    costo_produccion_unidad = (
        costo_material_total
        + costo_luz
        + costo_repuesto
        + costo_mano_obra_unidad
    )

    margen = calcular_margen(datos.cantidad, general)
    precio_unidad = costo_produccion_unidad * (1 + margen)
    subtotal = precio_unidad * datos.cantidad

    envio_calculado = (
        volumen_total_cm3 * datos.cantidad / 100
    ) * general["envio_por_100_cm3"]

    costo_envio = 0
    if datos.incluir_envio:
        costo_envio = max(general["envio_minimo"], envio_calculado)

    total = subtotal + costo_envio

    return {
        "producto": datos.nombre_producto,
        "cantidad": datos.cantidad,
        "resumen": {
            "precio_total_con_envio": round(total, 2),
            "envio": round(costo_envio, 2),
            "precio_unitario": round(precio_unidad, 2),
            "subtotal_sin_envio": round(subtotal, 2),
            "moneda": "COP",
        },
        "tiempo_horas_por_unidad": round(tiempo_horas, 2),
        "peso_total_con_desperdicio_gramos_por_unidad": round(peso_total, 2),
        "volumen_total_cm3_por_unidad": round(volumen_total_cm3, 2),
        "desperdicio_porcentaje": round(desperdicio * 100, 2),
        "margen_aplicado_porcentaje": round(margen * 100, 2),
        "materiales": detalle_materiales,
        "costos": {
            "material_unidad": round(costo_material_total, 2),
            "electricidad_unidad": round(costo_luz, 2),
            "repuesto_unidad": round(costo_repuesto, 2),
            "mano_obra_pedido": round(costo_mano_obra_pedido, 2),
            "mano_obra_unidad": round(costo_mano_obra_unidad, 2),
            "produccion_unidad": round(costo_produccion_unidad, 2),
            "precio_unidad": round(precio_unidad, 2),
            "envio": round(costo_envio, 2),
            "subtotal": round(subtotal, 2),
            "total": round(total, 2),
        },
        "configuracion_usada": {
            "precio_kwh_base": general["precio_kwh_base"],
            "precio_kwh_con_margen": round(precio_kwh, 2),
            "consumo_watts": general["consumo_watts"],
            "costo_repuesto_hora": round(costo_repuesto_hora, 2),
            "gramos_impresos_por_hora": general["gramos_impresos_por_hora"],
        },
        "moneda": "COP",
    }