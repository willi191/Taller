def resumir(registros):
    datos = []
    for r in registros:
        try:
            ventas = float(r.get("ventas", 0) or 0)
            gastos = float(r.get("gastos", 0) or 0)
            clientes = int(float(r.get("clientes", 0) or 0))
            datos.append({
                "mes": r.get("mes", ""),
                "ventas": ventas,
                "gastos": gastos,
                "ganancia": ventas - gastos,
                "clientes": clientes
            })
        except (TypeError, ValueError):
            continue

    ventas_total = sum(x["ventas"] for x in datos)
    gastos_total = sum(x["gastos"] for x in datos)
    ganancia_total = ventas_total - gastos_total
    clientes_total = sum(x["clientes"] for x in datos)
    margen = (ganancia_total / ventas_total * 100) if ventas_total else 0

    cambio = None
    if len(datos) >= 2 and datos[-2]["ventas"] != 0:
        cambio = (datos[-1]["ventas"] - datos[-2]["ventas"]) / datos[-2]["ventas"] * 100

    observaciones = []
    if not datos:
        observaciones.append("No hay registros todavía. Registra datos desde la consola y recarga el dashboard.")
    else:
        if ganancia_total < 0:
            observaciones.append("Los gastos acumulados superan las ventas. Revisa los costos y las fuentes de ingreso.")
        else:
            observaciones.append("La operación acumulada presenta una ganancia positiva.")
        if margen < 10:
            observaciones.append("El margen de ganancia es inferior al 10 %. Conviene revisar precios, costos y gastos.")
        else:
            observaciones.append("El margen de ganancia es igual o superior al 10 %.")
        if cambio is not None:
            if cambio > 0:
                observaciones.append(f"Las ventas del último periodo aumentaron {cambio:.1f}% frente al periodo anterior.")
            elif cambio < 0:
                observaciones.append(f"Las ventas del último periodo disminuyeron {abs(cambio):.1f}% frente al periodo anterior.")
            else:
                observaciones.append("Las ventas se mantuvieron estables frente al periodo anterior.")
        if len(datos) < 3:
            observaciones.append("Hay pocos periodos registrados: estas observaciones son descriptivas, no una predicción confiable.")
        else:
            observaciones.append("Se dispone de varios periodos para comparar tendencias; valida los resultados con el contexto del negocio.")

    return {
        "registros": datos,
        "kpis": {
            "ventas": ventas_total, "gastos": gastos_total,
            "ganancia": ganancia_total, "clientes": clientes_total,
            "margen": margen, "cambio_ventas": cambio
        },
        "analisis": observaciones
    }
