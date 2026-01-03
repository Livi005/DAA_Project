import random

def asignacion_greedy(problema, estrategia='grado'):
    """
    Asigna frecuencias usando estrategia greedy mejorada
    
    Args:
        problema: diccionario con el problema
        estrategia: 'grado', 'costo', 'mixto', 'aleatorio'
    
    Returns:
        lista de frecuencias asignadas
    """
    grafo = problema['grafo']
    n = problema['n']
    k = problema['k']
    costos = problema['costos']
    
    asignacion = [-1] * n
    
    # Seleccionar orden según estrategia
    torres = list(range(n))
    
    if estrategia == 'grado':
        # Ordenar por grado descendente (la estrategia original)
        torres.sort(key=lambda i: len(grafo.obtener_vecinos(i)), reverse=True)
    
    elif estrategia == 'costo':
        # Ordenar por costo mínimo de frecuencia ascendente
        torres.sort(key=lambda i: min(costos[i]))
    
    elif estrategia == 'mixto':
        # Combinación: grado * variabilidad de costos
        def prioridad_mixta(i):
            grado = len(grafo.obtener_vecinos(i))
            costo_min = min(costos[i])
            costo_max = max(costos[i])
            variabilidad = costo_max - costo_min
            return grado * variabilidad
        torres.sort(key=prioridad_mixta, reverse=True)
    
    elif estrategia == 'aleatorio':
        # Orden aleatorio (para múltiples intentos)
        random.shuffle(torres)
    else:
        # Por defecto: orden por grado
        torres.sort(key=lambda i: len(grafo.obtener_vecinos(i)), reverse=True)
    
    for torre in torres:
        # Frecuencias prohibidas por vecinos ya asignados
        prohibidas = set()
        for vecino in grafo.obtener_vecinos(torre):
            if asignacion[vecino] != -1:
                prohibidas.add(asignacion[vecino])
        
        # Buscar mejor frecuencia permitida (sin conflictos)
        mejor_frecuencia = -1
        mejor_costo = float('inf')
        
        for f in range(k):
            if f not in prohibidas and costos[torre][f] < mejor_costo:
                mejor_costo = costos[torre][f]
                mejor_frecuencia = f
        
        # SIEMPRE EVITAR CONFLICTOS: si no hay permitida, buscar alternativa
        if mejor_frecuencia == -1:
            # Buscar la frecuencia que cause menos conflictos con menor costo
            mejores_opciones = []
            
            for f in range(k):
                # Contar conflictos que causaría esta frecuencia
                conflictos_potenciales = 0
                for vecino in grafo.obtener_vecinos(torre):
                    if asignacion[vecino] == f:
                        conflictos_potenciales += 1
                
                costo_f = costos[torre][f]
                # Penalizar conflictos fuertemente
                costo_penalizado = costo_f + (conflictos_potenciales * 1000)
                mejores_opciones.append((costo_penalizado, conflictos_potenciales, costo_f, f))
            
            # Ordenar: primero menor costo penalizado
            mejores_opciones.sort()
            mejor_frecuencia = mejores_opciones[0][3]
        
        asignacion[torre] = mejor_frecuencia
    
    return asignacion

def greedy_con_reintentos(problema, reintentos=5):
    """
    Ejecuta greedy múltiples veces con diferentes estrategias
    y devuelve la mejor solución encontrada
    """
    mejor_solucion = None
    mejor_costo = float('inf')
    mejor_valida = False
    
    estrategias = ['grado', 'costo', 'mixto', 'aleatorio']
    
    for intento in range(reintentos):
        if intento < len(estrategias):
            estrategia = estrategias[intento]
        else:
            estrategia = 'aleatorio'
        
        # Ejecutar greedy con esta estrategia
        solucion = asignacion_greedy(problema, estrategia)
        
        # Calcular costo rápidamente
        costo = sum(problema['costos'][i][solucion[i]] for i in range(problema['n']))
        
        # Verificar si es válida
        from verificador import verificar_solucion
        valida, costo_real, conflictos = verificar_solucion(problema, solucion)
        
        # PRIORIDAD 1: Soluciones válidas, luego por costo
        if (valida and not mejor_valida) or \
           (valida == mejor_valida and costo_real < mejor_costo):
            mejor_costo = costo_real
            mejor_solucion = solucion
            mejor_valida = valida
    
    return mejor_solucion