from verificador import verificar_solucion

def analizar_solucion(problema, asignacion):
    """
    Proporciona métricas sobre una solución
    
    Retorna diccionario con estadísticas
    """
    valida, costo, conflictos = verificar_solucion(problema, asignacion)
    
    # Frecuencias utilizadas
    frec_utilizadas = set(asignacion)
    
    # Costo por torre
    costos_torre = []
    for i, f in enumerate(asignacion):
        costos_torre.append((i, problema['costos'][i][f]))
    
    # Torres con más conflictos
    conflictos_por_torre = {}
    for i, j in conflictos:
        conflictos_por_torre[i] = conflictos_por_torre.get(i, 0) + 1
        conflictos_por_torre[j] = conflictos_por_torre.get(j, 0) + 1
    
    return {
        'valida': valida,
        'costo_total': costo,
        'num_conflictos': len(conflictos),
        'frecuencias_utilizadas': len(frec_utilizadas),
        'costo_promedio': costo / len(asignacion) if asignacion else 0,
        'conflictos_por_torre': conflictos_por_torre,
        'costos_individuales': costos_torre
    }