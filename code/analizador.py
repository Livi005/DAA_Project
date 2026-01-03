from verificador import verificar_solucion, analisis_detallado

def analizar_solucion(problema, asignacion):
    """
    Proporciona métricas sobre una solución
    
    Retorna diccionario con estadísticas
    """
    # Obtener análisis detallado
    analisis = analisis_detallado(problema, asignacion)
    
    n = problema['n']
    k = problema['k']
    costos = problema['costos']
    
    # Calcular métricas adicionales
    # 1. Eficiencia: cuántas torres obtuvieron su frecuencia más barata
    torres_con_frecuencia_optima = 0
    for i in range(n):
        costo_min = min(costos[i])
        if abs(costos[i][asignacion[i]] - costo_min) < 0.001:
            torres_con_frecuencia_optima += 1
    
    eficiencia = (torres_con_frecuencia_optima / n * 100) if n > 0 else 0
    
    # 2. Balance de carga entre frecuencias
    distribucion = analisis['torres_por_frecuencia']
    if distribucion:
        promedio = sum(distribucion.values()) / len(distribucion)
        if promedio > 0:
            varianza = sum((count - promedio) ** 2 for count in distribucion.values()) / len(distribucion)
            desviacion = varianza ** 0.5
            balance = max(0, 100 - (desviacion / promedio * 100))
        else:
            balance = 100
    else:
        balance = 100
    
    # 3. Costos individuales (solo las 5 más caras)
    costos_individuales = []
    for i in range(n):
        costo_torre = costos[i][asignacion[i]]
        grado = len(problema['grafo'].obtener_vecinos(i))
        costos_individuales.append((i, asignacion[i], costo_torre, grado))
    
    # Ordenar por costo descendente
    costos_individuales.sort(key=lambda x: x[2], reverse=True)
    
    # 4. Análisis de posibles mejoras
    posibles_mejoras = estimar_potencial_mejora(problema, asignacion)
    
    # Combinar todo en un diccionario
    resultado = {
        'valida': analisis['valida'],
        'costo_total': analisis['costo_total'],
        'costo_promedio': analisis['costo_promedio'],
        'num_conflictos': analisis['num_conflictos'],
        'frecuencias_utilizadas': analisis['frecuencias_utilizadas'],
        'eficiencia_porcentaje': eficiencia,
        'balance_carga_porcentaje': balance,
        'torres_con_frecuencia_optima': torres_con_frecuencia_optima,
        'torres_mas_caras': costos_individuales[:5],  # Solo las 5 más caras
        'distribucion_frecuencias': analisis['torres_por_frecuencia'],
        'costos_por_frecuencia': analisis['costos_por_frecuencia'],
        'torres_problematicas': analisis['torres_problematicas'],
        'potencial_mejora_estimado': posibles_mejoras
    }
    
    return resultado

def estimar_potencial_mejora(problema, asignacion):
    """
    Estima cuánto se podría mejorar la solución actual
    """
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    potencial_total = 0
    torres_mejorables = 0
    
    for i in range(n):
        freq_actual = asignacion[i]
        costo_actual = costos[i][freq_actual]
        
        # Encontrar la mejor alternativa que no cause conflictos
        mejor_alternativa = None
        mejor_costo = costo_actual
        
        # Frecuencias prohibidas por vecinos
        frec_prohibidas = set()
        for vecino in grafo.obtener_vecinos(i):
            frec_prohibidas.add(asignacion[vecino])
        
        for f in range(k):
            if f != freq_actual and f not in frec_prohibidas:
                if costos[i][f] < mejor_costo:
                    mejor_costo = costos[i][f]
                    mejor_alternativa = f
        
        # Si hay alternativa mejor, sumar al potencial
        if mejor_alternativa is not None:
            ahorro = costo_actual - mejor_costo
            potencial_total += ahorro
            torres_mejorables += 1
    
    return {
        'potencial_total': potencial_total,
        'torres_mejorables': torres_mejorables,
        'porcentaje_mejora_potencial': (potencial_total / problema['costos'].sum() * 100) if problema['costos'].sum() > 0 else 0
    }

def comparar_soluciones(problema, solucion1, solucion2, nombre1="Solución 1", nombre2="Solución 2"):
    """
    Compara dos soluciones y muestra diferencias
    """
    analisis1 = analizar_solucion(problema, solucion1)
    analisis2 = analizar_solucion(problema, solucion2)
    
    print("="*60)
    print("COMPARACIÓN DE SOLUCIONES")
    print("="*60)
    
    print(f"\n{nombre1}:")
    print(f"  Costo total: {analisis1['costo_total']:.2f}")
    print(f"  Válida: {analisis1['valida']}")
    print(f"  Conflictos: {analisis1['num_conflictos']}")
    print(f"  Eficiencia: {analisis1['eficiencia_porcentaje']:.1f}%")
    
    print(f"\n{nombre2}:")
    print(f"  Costo total: {analisis2['costo_total']:.2f}")
    print(f"  Válida: {analisis2['valida']}")
    print(f"  Conflictos: {analisis2['num_conflictos']}")
    print(f"  Eficiencia: {analisis2['eficiencia_porcentaje']:.1f}%")
    
    diferencia = analisis1['costo_total'] - analisis2['costo_total']
    if analisis1['costo_total'] > 0:
        porcentaje = (diferencia / analisis1['costo_total']) * 100
    else:
        porcentaje = 0
    
    print(f"\nDIFERENCIA:")
    print(f"  {nombre2} es {diferencia:.2f} {'más barata' if diferencia > 0 else 'más cara'} que {nombre1}")
    print(f"  Diferencia porcentual: {abs(porcentaje):.1f}%")
    
    return {
        'diferencia_costo': diferencia,
        'porcentaje_diferencia': porcentaje,
        'mejor_solucion': nombre2 if diferencia > 0 else nombre1
    }