def mejorar_solucion(problema, asignacion_inicial, max_iter=1000):
    """
    Mejora solución mediante búsqueda local
    
    Intenta reducir costo cambiando frecuencias una a una
    """
    mejor_asignacion = asignacion_inicial[:]
    valida, mejor_costo, _ = verificar_solucion(problema, mejor_asignacion)
    
    if not valida:
        return mejor_asignacion, mejor_costo, "Solución inicial inválida"
    
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    mejoras = 0
    for _ in range(max_iter):
        # Elegir torre aleatoria
        torre = random.randint(0, n-1)
        
        # Frecuencias actual y sus vecinos
        freq_actual = mejor_asignacion[torre]
        frec_vecinos = set(mejor_asignacion[v] for v in grafo.obtener_vecinos(torre))
        
        # Buscar mejor frecuencia alternativa
        mejor_alternativa = -1
        mejor_ahorro = 0
        
        for f in range(k):
            if f != freq_actual and f not in frec_vecinos:
                ahorro = costos[torre][freq_actual] - costos[torre][f]
                if ahorro > mejor_ahorro:
                    mejor_ahorro = ahorro
                    mejor_alternativa = f
        
        # Aplicar cambio si mejora
        if mejor_alternativa != -1:
            mejor_asignacion[torre] = mejor_alternativa
            mejor_costo -= mejor_ahorro
            mejoras += 1
    
    return mejor_asignacion, mejor_costo, f"Mejoras: {mejoras}"