import random
from verificador import verificar_solucion

def hill_climbing(problema, asignacion_inicial, costo_inicial, max_iter):
    """Ascenso de colina simple (solo acepta mejoras que no creen conflictos)"""
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    mejor_asignacion = asignacion_inicial[:]
    mejor_costo = costo_inicial
    mejoras = 0
    
    for iteracion in range(max_iter):
        # Generar lista de movimientos posibles que NO causen conflictos
        movimientos_validos = []
        
        for torre in range(n):
            freq_actual = mejor_asignacion[torre]
            
            # Obtener frecuencias usadas por vecinos
            frec_vecinos = set()
            for vecino in grafo.obtener_vecinos(torre):
                frec_vecinos.add(mejor_asignacion[vecino])
            
            # Evaluar todas las frecuencias alternativas
            for f in range(k):
                if f != freq_actual and f not in frec_vecinos:
                    # Calcular ahorro potencial (solo si no causa conflictos)
                    ahorro = costos[torre][freq_actual] - costos[torre][f]
                    if ahorro > 0:
                        movimientos_validos.append((torre, f, ahorro))
        
        # Si no hay movimientos válidos que mejoren, terminar
        if not movimientos_validos:
            break
        
        # Seleccionar el mejor movimiento
        movimientos_validos.sort(key=lambda x: x[2], reverse=True)
        mejor_torre, mejor_freq, mejor_ahorro = movimientos_validos[0]
        
        # Aplicar el movimiento
        mejor_asignacion[mejor_torre] = mejor_freq
        mejor_costo -= mejor_ahorro
        mejoras += 1
    
    return mejor_asignacion, mejor_costo, f"Hill Climbing: {mejoras} mejoras"

def hill_climbing_con_conflictos(problema, asignacion_inicial, costo_inicial, max_iter):
    """Ascenso de colina que permite conflictos temporales pero los repara"""
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    mejor_asignacion = asignacion_inicial[:]
    mejor_costo = costo_inicial
    mejoras = 0
    
    for iteracion in range(max_iter):
        mejor_movimiento = None
        mejor_ahorro_neto = 0
        
        # Evaluar todas las torres
        for torre in range(n):
            freq_actual = mejor_asignacion[torre]
            costo_actual = costos[torre][freq_actual]
            
            # Evaluar todas las frecuencias alternativas
            for f in range(k):
                if f != freq_actual:
                    # Calcular ahorro potencial
                    ahorro = costo_actual - costos[torre][f]
                    
                    if ahorro > 0:  # Solo considerar si hay ahorro
                        # Contar conflictos que causaría
                        conflictos_nuevos = 0
                        for vecino in grafo.obtener_vecinos(torre):
                            if mejor_asignacion[vecino] == f:
                                conflictos_nuevos += 1
                        
                        # Calcular ahorro neto: ahorro - penalización por conflictos
                        # Penalización más inteligente: proporcional al costo de las torres en conflicto
                        penalizacion = 0
                        if conflictos_nuevos > 0:
                            # Penalizar más si hay muchos conflictos
                            penalizacion = conflictos_nuevos * 20
                        
                        ahorro_neto = ahorro - penalizacion
                        
                        if ahorro_neto > mejor_ahorro_neto:
                            mejor_ahorro_neto = ahorro_neto
                            mejor_movimiento = (torre, f, ahorro, conflictos_nuevos)
        
        # Aplicar el mejor movimiento si hay mejora neta
        if mejor_movimiento and mejor_ahorro_neto > 0:
            torre, nueva_freq, ahorro, conflictos = mejor_movimiento
            mejor_asignacion[torre] = nueva_freq
            mejor_costo -= ahorro
            mejoras += 1
            
            # Si creamos conflictos, intentar repararlos inmediatamente
            if conflictos > 0:
                # Intentar cambiar las torres en conflicto
                for vecino in grafo.obtener_vecinos(torre):
                    if mejor_asignacion[vecino] == nueva_freq:
                        # Buscar alternativa para el vecino
                        mejor_alternativa = None
                        mejor_costo_alternativa = float('inf')
                        
                        # Frecuencias prohibidas para el vecino
                        prohibidas_vecino = set()
                        for v2 in grafo.obtener_vecinos(vecino):
                            if v2 != torre:
                                prohibidas_vecino.add(mejor_asignacion[v2])
                        
                        for f_alt in range(k):
                            if f_alt != nueva_freq and f_alt not in prohibidas_vecino:
                                if costos[vecino][f_alt] < mejor_costo_alternativa:
                                    mejor_costo_alternativa = costos[vecino][f_alt]
                                    mejor_alternativa = f_alt
                        
                        if mejor_alternativa is not None:
                            mejor_asignacion[vecino] = mejor_alternativa
                            mejor_costo = mejor_costo - costos[vecino][nueva_freq] + mejor_costo_alternativa
        
        else:
            # No hay más mejoras
            break
    
    return mejor_asignacion, mejor_costo, f"Hill Climbing mejorado: {mejoras} mejoras"

def tabu_search_simple(problema, asignacion_inicial, costo_inicial, max_iter, tamano_tabu=10):
    """Búsqueda Tabú simple con lista de movimientos prohibidos"""
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    mejor_asignacion_global = asignacion_inicial[:]
    mejor_costo_global = costo_inicial
    
    asignacion_actual = asignacion_inicial[:]
    costo_actual = costo_inicial
    
    # Lista Tabú: almacena (torre, frecuencia_vieja, frecuencia_nueva)
    lista_tabu = []
    mejoras = 0
    
    for iteracion in range(max_iter):
        mejor_movimiento = None
        mejor_costo_vecino = float('inf')
        mejor_asignacion_vecino = None
        
        # Evaluar todos los movimientos posibles
        for torre in range(n):
            freq_actual = asignacion_actual[torre]
            
            for f in range(k):
                if f != freq_actual:
                    # Calcular nuevo costo
                    nuevo_costo = costo_actual - costos[torre][freq_actual] + costos[torre][f]
                    
                    # Verificar si movimiento está en lista Tabú
                    es_tabu = (torre, f, freq_actual) in lista_tabu
                    
                    # Criterio de aspiración: aceptar si es mejor que el global aunque sea tabú
                    if (nuevo_costo < mejor_costo_vecino and not es_tabu) or \
                       (nuevo_costo < mejor_costo_global):
                        mejor_costo_vecino = nuevo_costo
                        mejor_movimiento = (torre, f, freq_actual)
                        
                        # Crear nueva asignación
                        nueva_asignacion = asignacion_actual[:]
                        nueva_asignacion[torre] = f
                        mejor_asignacion_vecino = nueva_asignacion
        
        if mejor_movimiento is None:
            # No hay movimientos no tabú, terminar
            break
        
        # Aplicar el mejor movimiento
        torre, nueva_freq, vieja_freq = mejor_movimiento
        asignacion_actual = mejor_asignacion_vecino
        costo_actual = mejor_costo_vecino
        
        # Añadir a lista Tabú
        movimiento_tabu = (torre, vieja_freq, nueva_freq)
        lista_tabu.append(movimiento_tabu)
        
        # Mantener tamaño de lista Tabú
        if len(lista_tabu) > tamano_tabu:
            lista_tabu.pop(0)
        
        # Actualizar mejor solución global
        if costo_actual < mejor_costo_global:
            mejor_costo_global = costo_actual
            mejor_asignacion_global = asignacion_actual[:]
            mejoras += 1
    
    return mejor_asignacion_global, mejor_costo_global, f"Tabu Search: {mejoras} mejoras"

def arreglar_conflictos(problema, asignacion, max_intentos=10):
    """
    Intenta arreglar conflictos en una solución inválida
    
    Args:
        problema: diccionario con el problema
        asignacion: solución con conflictos
        max_intentos: máximo de intentos de arreglo
    
    Returns:
        solución arreglada (puede seguir teniendo conflictos si es imposible)
    """
    n = problema['n']
    k = problema['k']
    grafo = problema['grafo']
    costos = problema['costos']
    
    asignacion_arreglada = asignacion[:]
    
    for intento in range(max_intentos):
        # Identificar todos los conflictos
        conflictos = []
        for i in range(n):
            for j in grafo.obtener_vecinos(i):
                if i < j and asignacion_arreglada[i] == asignacion_arreglada[j]:
                    conflictos.append((i, j))
        
        # Si no hay conflictos, hemos terminado
        if not conflictos:
            break
        
        # Tomar el conflicto con mayor costo
        conflictos.sort(key=lambda x: costos[x[0]][asignacion_arreglada[x[0]]] + 
                                   costos[x[1]][asignacion_arreglada[x[1]]], reverse=True)
        i, j = conflictos[0]
        freq_conflicto = asignacion_arreglada[i]
        
        # Decidir qué torre cambiar (la que tenga alternativa más barata)
        mejor_cambio_i = None
        mejor_costo_i = float('inf')
        
        mejor_cambio_j = None
        mejor_costo_j = float('inf')
        
        # Buscar alternativa para torre i
        for f in range(k):
            if f != freq_conflicto:
                # Verificar que no cause conflictos con otros vecinos
                conflicto_con_vecinos = False
                for vecino in grafo.obtener_vecinos(i):
                    if vecino != j and asignacion_arreglada[vecino] == f:
                        conflicto_con_vecinos = True
                        break
                
                if not conflicto_con_vecinos and costos[i][f] < mejor_costo_i:
                    mejor_costo_i = costos[i][f]
                    mejor_cambio_i = f
        
        # Buscar alternativa para torre j
        for f in range(k):
            if f != freq_conflicto:
                # Verificar que no cause conflictos con otros vecinos
                conflicto_con_vecinos = False
                for vecino in grafo.obtener_vecinos(j):
                    if vecino != i and asignacion_arreglada[vecino] == f:
                        conflicto_con_vecinos = True
                        break
                
                if not conflicto_con_vecinos and costos[j][f] < mejor_costo_j:
                    mejor_costo_j = costos[j][f]
                    mejor_cambio_j = f
        
        # Aplicar el cambio que sea mejor (menor costo)
        if mejor_cambio_i is not None and mejor_cambio_j is not None:
            costo_cambio_i = costos[i][mejor_cambio_i] - costos[i][freq_conflicto]
            costo_cambio_j = costos[j][mejor_cambio_j] - costos[j][freq_conflicto]
            
            if costo_cambio_i <= costo_cambio_j:
                asignacion_arreglada[i] = mejor_cambio_i
            else:
                asignacion_arreglada[j] = mejor_cambio_j
        elif mejor_cambio_i is not None:
            asignacion_arreglada[i] = mejor_cambio_i
        elif mejor_cambio_j is not None:
            asignacion_arreglada[j] = mejor_cambio_j
        else:
            # No hay alternativa sin conflictos, elegir la más barata
            for f in range(k):
                if f != freq_conflicto:
                    asignacion_arreglada[i] = f
                    break
    
    return asignacion_arreglada

def mejorar_solucion(problema, asignacion_inicial, max_iter=1000, metodo='hill_climbing'):
    """
    Mejora solución mediante búsqueda local mejorada
    
    Args:
        problema: diccionario con el problema
        asignacion_inicial: solución inicial
        max_iter: máximo de iteraciones
        metodo: 'hill_climbing', 'tabu_search', 'hill_climbing_con_conflictos'
    
    Returns:
        mejor_asignacion, mejor_costo, info
    """
    # Primero verificar y arreglar si es necesario
    valida, costo_actual, conflictos = verificar_solucion(problema, asignacion_inicial)
    asignacion_actual = asignacion_inicial[:]
    
    # Si la solución no es válida, intentar arreglarla primero
    if not valida:
        asignacion_actual = arreglar_conflictos(problema, asignacion_actual)
        valida, costo_actual, conflictos = verificar_solucion(problema, asignacion_actual)
    
    # Si después de arreglar sigue siendo inválida, devolver como está
    if not valida:
        return asignacion_actual, costo_actual, "Solución inválida después de intentar arreglar"
    
    # Ahora aplicar búsqueda local según el método
    if metodo == 'hill_climbing':
        return hill_climbing(problema, asignacion_actual, costo_actual, max_iter)
    elif metodo == 'tabu_search':
        return tabu_search_simple(problema, asignacion_actual, costo_actual, max_iter)
    elif metodo == 'hill_climbing_con_conflictos':
        return hill_climbing_con_conflictos(problema, asignacion_actual, costo_actual, max_iter)
    else:
        return hill_climbing(problema, asignacion_actual, costo_actual, max_iter)

def mejorar_solucion_con_reinicio(problema, solucion_inicial=None, max_reinicios=3, iter_por_reinicio=300):
    """
    Búsqueda local con múltiples reinicios
    
    RETORNA SIEMPRE UNA SOLUCIÓN - NUNCA None
    """
    n = problema['n']
    k = problema['k']
    
    mejor_solucion = None
    mejor_costo = float('inf')
    mejor_valida = False
    
    # Si no se proporciona solución inicial, usar una aleatoria
    if solucion_inicial is None:
        solucion_inicial = [random.randint(0, k-1) for _ in range(n)]
    
    for reinicio in range(max_reinicios):
        if reinicio == 0:
            # Usar solución inicial en el primer reinicio
            solucion_actual = solucion_inicial[:]
        else:
            # Generar solución aleatoria MEJORADA
            solucion_actual = []
            for i in range(n):
                # Intentar elegir frecuencia que minimice conflicto local
                frecuencias_disponibles = list(range(k))
                random.shuffle(frecuencias_disponibles)
                mejor_f = frecuencias_disponibles[0]
                solucion_actual.append(mejor_f)
        
        # Intentar arreglar conflictos
        solucion_arreglada = arreglar_conflictos(problema, solucion_actual)
        
        # Aplicar búsqueda local (usar hill climbing con conflictos para más exploración)
        solucion_mejorada, costo, info = mejorar_solucion(
            problema, solucion_arreglada, max_iter=iter_por_reinicio,
            metodo='hill_climbing_con_conflictos'
        )
        
        # Verificar si es mejor
        valida, costo_real, _ = verificar_solucion(problema, solucion_mejorada)
        
        # PRIORIDAD: 1) Soluciones válidas, 2) Menor costo
        if mejor_solucion is None:
            mejor_solucion = solucion_mejorada
            mejor_costo = costo_real
            mejor_valida = valida
        else:
            if valida and not mejor_valida:
                # Nueva solución es válida, la anterior no
                mejor_solucion = solucion_mejorada
                mejor_costo = costo_real
                mejor_valida = valida
            elif valida == mejor_valida and costo_real < mejor_costo:
                # Misma validez, pero mejor costo
                mejor_solucion = solucion_mejorada
                mejor_costo = costo_real
    
    # Garantizar que siempre retornamos una solución
    if mejor_solucion is None:
        # Si por alguna razón no hay solución, devolver la inicial arreglada
        mejor_solucion = arreglar_conflictos(problema, solucion_inicial[:])
        mejor_valida, mejor_costo, _ = verificar_solucion(problema, mejor_solucion)
    
    return mejor_solucion, mejor_costo, f"Reinicios: {max_reinicios}"