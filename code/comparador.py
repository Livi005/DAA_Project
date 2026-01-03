import time
from verificador import verificar_solucion
from greedy_simple import asignacion_greedy, greedy_con_reintentos
from busqueda_local import mejorar_solucion, mejorar_solucion_con_reinicio

def comparar_algoritmos(problema, algoritmos):
    """
    Compara varios algoritmos en mismo problema
    
    Args:
        problema: diccionario con el problema
        algoritmos: lista de tuplas (nombre, funcion, kwargs)
    
    Returns:
        lista de resultados
    """
    print("="*70)
    print("COMPARACIÓN DE ALGORITMOS")
    print(f"Problema: {problema['n']} torres, {problema['k']} frecuencias")
    print("="*70)
    
    resultados = []
    
    for nombre, funcion, kwargs in algoritmos:
        print(f"\nEjecutando: {nombre}")
        print("-"*40)
        
        inicio = time.time()
        
        try:
            if kwargs:
                solucion = funcion(problema, **kwargs)
            else:
                solucion = funcion(problema)
            
            tiempo = time.time() - inicio
            
            valida, costo, conflictos = verificar_solucion(problema, solucion)
            
            resultados.append({
                'algoritmo': nombre,
                'tiempo': tiempo,
                'costo': costo,
                'valida': valida,
                'conflictos': len([c for c in conflictos if isinstance(c, tuple)]),
                'solucion': solucion
            })
            
            print(f"  - Tiempo: {tiempo:.4f}s")
            print(f"  - Costo: {costo:.2f}")
            print(f"  - Válida: {valida}")
            print(f"  - Conflictos: {resultados[-1]['conflictos']}")
            
        except Exception as e:
            print(f"  - ERROR: {e}")
            resultados.append({
                'algoritmo': nombre,
                'error': str(e)
            })
    
    # Mostrar resumen comparativo
    print("\n" + "="*70)
    print("RESUMEN COMPARATIVO")
    print("="*70)
    
    # Filtrar resultados exitosos
    resultados_exitosos = [r for r in resultados if 'costo' in r]
    
    if resultados_exitosos:
        # Ordenar por costo (ascendente)
        resultados_exitosos.sort(key=lambda x: x['costo'])
        
        print("\nRanking por costo (mejor a peor):")
        for i, resultado in enumerate(resultados_exitosos, 1):
            print(f"{i}. {resultado['algoritmo']}: {resultado['costo']:.2f} "
                  f"(tiempo: {resultado['tiempo']:.4f}s, "
                  f"válida: {resultado['valida']})")
        
        # Mejor algoritmo
        mejor = resultados_exitosos[0]
        print(f"\nMEJOR ALGORITMO: {mejor['algoritmo']}")
        print(f"  - Costo: {mejor['costo']:.2f}")
        print(f"  - Tiempo: {mejor['tiempo']:.4f}s")
        print(f"  - Válida: {mejor['valida']}")
    
    return resultados

def comparacion_estandar(problema):
    """
    Comparación estándar de algoritmos comunes
    """
    algoritmos = [
        ("Greedy (grado)", asignacion_greedy, {'estrategia': 'grado'}),
        ("Greedy (costo)", asignacion_greedy, {'estrategia': 'costo'}),
        ("Greedy (mixto)", asignacion_greedy, {'estrategia': 'mixto'}),
        ("Greedy con reintentos", greedy_con_reintentos, {'reintentos': 5}),
        ("Hill Climbing", lambda p: mejorar_solucion(p, asignacion_greedy(p), metodo='hill_climbing'), {}),
        ("Tabu Search", lambda p: mejorar_solucion(p, asignacion_greedy(p), metodo='tabu_search'), {}),
        ("Búsqueda con reinicio", mejorar_solucion_con_reinicio, {'max_reinicios': 3}),
    ]
    
    return comparar_algoritmos(problema, algoritmos)

def analizar_escalabilidad():
    """
    Analiza cómo escalan los algoritmos con diferentes tamaños de problema
    """
    from instancias import crear_problema
    
    tamanos = [10, 20, 30, 50, 100]
    resultados_escalabilidad = []
    
    for n in tamanos:
        print(f"\n{'='*70}")
        print(f"ANALIZANDO ESCALABILIDAD: n={n}")
        print(f"{'='*70}")
        
        # Crear problema
        problema = crear_problema(n, 4, 0.3, semilla=42)
        
        # Algoritmos a comparar
        algoritmos = [
            ("Greedy", asignacion_greedy, {}),
            ("Hill Climbing", lambda p: mejorar_solucion(p, asignacion_greedy(p), max_iter=min(1000, n*10)), {}),
        ]
        
        resultados = comparar_algoritmos(problema, algoritmos)
        
        for r in resultados:
            if 'costo' in r:
                resultados_escalabilidad.append({
                    'n': n,
                    'algoritmo': r['algoritmo'],
                    'tiempo': r['tiempo'],
                    'costo': r['costo']
                })
    
    # Mostrar resumen de escalabilidad
    print("\n" + "="*70)
    print("RESUMEN DE ESCALABILIDAD")
    print("="*70)
    
    print("\nTiempo vs tamaño:")
    for n in tamanos:
        print(f"\nn={n}:")
        for algo in ['Greedy', 'Hill Climbing']:
            datos = [r for r in resultados_escalabilidad if r['n'] == n and r['algoritmo'] == algo]
            if datos:
                print(f"  {algo}: {datos[0]['tiempo']:.4f}s")
    
    return resultados_escalabilidad