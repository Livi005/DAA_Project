def asignacion_greedy(problema):
    """
    Asigna frecuencias usando estrategia greedy simple
    
    Ordena por grado y asigna frecuencia más barata disponible
    No garantiza optimalidad
    """
    grafo = problema['grafo']
    n = problema['n']
    k = problema['k']
    costos = problema['costos']
    
    asignacion = [-1] * n
    
    # Ordenar torres por número de vecinos (descendente)
    torres = list(range(n))
    torres.sort(key=lambda i: len(grafo.obtener_vecinos(i)), reverse=True)
    
    for torre in torres:
        # Frecuencias usadas por vecinos ya asignados
        prohibidas = set()
        for vecino in grafo.obtener_vecinos(torre):
            if asignacion[vecino] != -1:
                prohibidas.add(asignacion[vecino])
        
        # Buscar frecuencia permitida más barata
        mejor_frecuencia = -1
        mejor_costo = float('inf')
        
        for f in range(k):
            if f not in prohibidas and costos[torre][f] < mejor_costo:
                mejor_costo = costos[torre][f]
                mejor_frecuencia = f
        
        # Si no hay permitida, usar la más barata (habrá conflicto)
        if mejor_frecuencia == -1:
            mejor_frecuencia = min(range(k), key=lambda f: costos[torre][f])
        
        asignacion[torre] = mejor_frecuencia
    
    return asignacion