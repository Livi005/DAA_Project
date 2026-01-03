def verificar_solucion(problema, asignacion, calcular_todo=True):
    """
    Verifica si asignación cumple restricciones y calcula costo
    
    Args:
        problema: diccionario con grafo, k, costos
        asignacion: lista de frecuencias para cada torre
        calcular_todo: si False, se detiene al primer error (más rápido)
    
    Returns:
        (es_valida, costo_total, lista_conflictos)
    """
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    # Verificar longitud
    if len(asignacion) != n:
        if calcular_todo:
            return False, float('inf'), ["Longitud incorrecta"]
        else:
            return False, float('inf'), []
    
    costo_total = 0
    conflictos = []
    
    # Verificar rangos y calcular costo
    for i in range(n):
        freq = asignacion[i]
        
        # Verificar rango válido
        if freq < 0 or freq >= k:
            if not calcular_todo:
                return False, float('inf'), []
            else:
                conflictos.append(f"Frecuencia inválida en torre {i}: {freq}")
        
        costo_total += costos[i][freq]
    
    # Verificar interferencias
    for i in range(n):
        for j in grafo.obtener_vecinos(i):
            if i < j and asignacion[i] == asignacion[j]:
                conflictos.append((i, j))
                if not calcular_todo:
                    return False, costo_total, conflictos
    
    es_valida = len([c for c in conflictos if isinstance(c, tuple)]) == 0
    
    return (es_valida, costo_total, conflictos)

def analisis_detallado(problema, asignacion):
    """
    Análisis detallado de una solución
    
    Returns:
        diccionario con métricas detalladas
    """
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    valida, costo_total, conflictos = verificar_solucion(problema, asignacion, calcular_todo=True)
    
    # Calcular frecuencias utilizadas
    frecuencias_usadas = set(asignacion)
    
    # Calcular costos por frecuencia
    costos_por_frecuencia = {}
    torres_por_frecuencia = {}
    
    for f in range(k):
        costos_por_frecuencia[f] = 0
        torres_por_frecuencia[f] = 0
    
    for i, f in enumerate(asignacion):
        costos_por_frecuencia[f] += costos[i][f]
        torres_por_frecuencia[f] += 1
    
    # Calcular torres problemáticas (con más conflictos)
    conflictos_por_torre = {}
    for conflicto in conflictos:
        if isinstance(conflicto, tuple):
            i, j = conflicto
            conflictos_por_torre[i] = conflictos_por_torre.get(i, 0) + 1
            conflictos_por_torre[j] = conflictos_por_torre.get(j, 0) + 1
    
    return {
        'valida': valida,
        'costo_total': costo_total,
        'costo_promedio': costo_total / n if n > 0 else 0,
        'num_conflictos': len([c for c in conflictos if isinstance(c, tuple)]),
        'frecuencias_utilizadas': len(frecuencias_usadas),
        'conflictos_detallados': conflictos,
        'costos_por_frecuencia': costos_por_frecuencia,
        'torres_por_frecuencia': torres_por_frecuencia,
        'conflictos_por_torre': conflictos_por_torre,
        'torres_problematicas': sorted(conflictos_por_torre.items(), key=lambda x: x[1], reverse=True)[:5]
    }