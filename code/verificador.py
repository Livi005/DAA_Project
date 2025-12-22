def verificar_solucion(problema, asignacion):
    """
    Verifica si asignación cumple restricciones y calcula costo
    
    problema: diccionario con grafo, k, costos
    asignacion: lista de frecuencias para cada torre
    
    Retorna: (es_valida, costo_total, lista_conflictos)
    """
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    # Verificar longitud
    if len(asignacion) != n:
        return False, float('inf'), ["Longitud incorrecta"]
    
    costo_total = 0
    conflictos = []
    
    # Calcular costo y verificar rangos
    for i in range(n):
        if asignacion[i] < 0 or asignacion[i] >= k:
            return False, float('inf'), [f"Frecuencia inválida en torre {i}"]
        costo_total += costos[i][asignacion[i]]
    
    # Verificar interferencias
    for i in range(n):
        for j in grafo.obtener_vecinos(i):
            if i < j and asignacion[i] == asignacion[j]:
                conflictos.append((i, j))
    
    return (len(conflictos) == 0, costo_total, conflictos)