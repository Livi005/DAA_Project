import datetime
import time
import json
from grafo import Grafo
from busqueda_local import mejorar_solucion, mejorar_solucion_con_reinicio, hill_climbing_con_conflictos
from instancias import crear_problema, crear_problema_especial
from verificador import verificar_solucion
from greedy_simple import asignacion_greedy, greedy_con_reintentos
from busqueda_local import mejorar_solucion, mejorar_solucion_con_reinicio
from analizador import analizar_solucion, comparar_soluciones
from visualizador import dibujar_solucion, visualizar_evolucion

def ejecutar_varios_experimentos():
    """
    Ejecuta múltiples experimentos sistemáticamente para análisis comparativo
    """
    print("\n" + "="*70)
    print("EJECUCIÓN DE MÚLTIPLES EXPERIMENTOS SISTEMÁTICOS")
    print("="*70)
    
    experimentos = []
    
    # Experimento 1: Variar número de torres
    print("\n1. VARIANDO NÚMERO DE TORRES (k=4, densidad=0.3)")
    print("-"*50)
    
    for n in [10, 20, 30, 50, 100]:
        print(f"\n  n = {n} torres...")
        resultado = resolver_problema_completo(
            n_torres=n,
            k_frecuencias=4,
            densidad=0.3,
            estrategia_greedy='mixto',
            metodo_busqueda='hill_climbing_con_conflictos',  # Cambiado a método mejorado
            max_iteraciones=min(200, n*2),
            visualizar=False,
            semilla=42
        )
        
        experimentos.append({
            'tipo': 'variar_n',
            'n': n,
            'k': 4,
            'resultado': resultado
        })
    
    # Experimento 2: Variar número de frecuencias
    print("\n2. VARIANDO NÚMERO DE FRECUENCIAS (n=20, densidad=0.3)")
    print("-"*50)
    
    for k in [2, 3, 4, 6, 8]:
        print(f"\n  k = {k} frecuencias...")
        resultado = resolver_problema_completo(
            n_torres=20,
            k_frecuencias=k,
            densidad=0.3,
            estrategia_greedy='mixto',
            metodo_busqueda='hill_climbing_con_conflictos',  # Cambiado a método mejorado
            max_iteraciones=200,
            visualizar=False,
            semilla=43
        )
        
        experimentos.append({
            'tipo': 'variar_k',
            'n': 20,
            'k': k,
            'resultado': resultado
        })
    
    # Experimento 3: Comparar estrategias greedy
    print("\n3. COMPARANDO ESTRATEGIAS GREEDY (n=30, k=4)")
    print("-"*50)
    
    estrategias = ['grado', 'costo', 'mixto', 'aleatorio']
    
    for estrategia in estrategias:
        print(f"\n  Estrategia greedy: {estrategia}...")
        resultado = resolver_problema_completo(
            n_torres=30,
            k_frecuencias=4,
            densidad=0.3,
            estrategia_greedy=estrategia,
            metodo_busqueda='hill_climbing_con_conflictos',  # Cambiado a método mejorado
            max_iteraciones=200,
            visualizar=False,
            semilla=44
        )
        
        experimentos.append({
            'tipo': 'comparar_greedy',
            'estrategia': estrategia,
            'resultado': resultado
        })
    
    # Experimento 4: Comparar métodos de búsqueda
    print("\n4. COMPARANDO MÉTODOS DE BÚSQUEDA (n=40, k=5)")
    print("-"*50)
    
    metodos = ['hill_climbing_con_conflictos', 'tabu_search']  # Cambiado el primero
    
    for metodo in metodos:
        print(f"\n  Método de búsqueda: {metodo}...")
        resultado = resolver_problema_completo(
            n_torres=40,
            k_frecuencias=5,
            densidad=0.3,
            estrategia_greedy='mixto',
            metodo_busqueda=metodo,
            max_iteraciones=300,
            visualizar=False,
            semilla=45
        )
        
        experimentos.append({
            'tipo': 'comparar_busqueda',
            'metodo': metodo,
            'resultado': resultado
        })
    
    # Mostrar resumen de todos los experimentos
    print("\n" + "="*70)
    print("RESUMEN DE TODOS LOS EXPERIMENTOS")
    print("="*70)
    
    # Tabla de resultados
    print("\n" + "-"*90)
    print(f"{'Experimento':<15} {'n':<5} {'k':<5} {'Costo Inicial':<15} {'Costo Final':<15} {'Mejora %':<10} {'Tiempo (s)':<10}")
    print("-"*90)
    
    tiempo_total = 0
    
    for exp in experimentos:
        if 'tipo' in exp:
            if exp['tipo'] == 'variar_n':
                n = exp['n']
                k = exp['k']
                desc = f"n={n}"
            elif exp['tipo'] == 'variar_k':
                n = exp['n']
                k = exp['k']
                desc = f"k={k}"
            elif exp['tipo'] == 'comparar_greedy':
                desc = f"greedy={exp['estrategia']}"
                n = exp['resultado']['problema']['n']
                k = exp['resultado']['problema']['k']
            elif exp['tipo'] == 'comparar_busqueda':
                desc = f"busqueda={exp['metodo']}"
                n = exp['resultado']['problema']['n']
                k = exp['resultado']['problema']['k']
            else:
                desc = exp['tipo']
                n = exp.get('n', '?')
                k = exp.get('k', '?')
            
            costo_ini = exp['resultado']['costo_inicial']
            costo_fin = exp['resultado']['costo_final']
            
            if costo_ini > 0:
                mejora = ((costo_ini - costo_fin) / costo_ini * 100)
            else:
                mejora = 0
            
            # Calcular tiempo aproximado (sumando greedy + búsqueda)
            tiempo_estimado = n * k / 1000  # Estimación simplificada
            
            print(f"{desc:<15} {n:<5} {k:<5} {costo_ini:<15.2f} {costo_fin:<15.2f} {mejora:<10.2f} {tiempo_estimado:<10.3f}")
            
            tiempo_total += tiempo_estimado
    
    print("-"*90)
    print(f"\nTotal de experimentos: {len(experimentos)}")
    print(f"Tiempo total estimado: {tiempo_total:.2f} segundos")
    print("="*70)
    
    # Guardar resultados detallados
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"resultados_experimentos_{timestamp}.json"
    
    # Preparar datos para guardar
    datos_guardar = []
    for exp in experimentos:
        datos_guardar.append({
            'tipo': exp.get('tipo', 'desconocido'),
            'configuracion': {k: v for k, v in exp.items() if k != 'resultado'},
            'resultados_resumen': {
                'costo_inicial': exp['resultado']['costo_inicial'],
                'costo_final': exp['resultado']['costo_final'],
                'mejora_porcentual': ((exp['resultado']['costo_inicial'] - exp['resultado']['costo_final']) / exp['resultado']['costo_inicial'] * 100) if exp['resultado']['costo_inicial'] > 0 else 0
            }
        })
    
    with open(nombre_archivo, 'w') as f:
        json.dump(datos_guardar, f, indent=2, default=str)
    
    print(f"\nResultados detallados guardados en: {nombre_archivo}")
    
    return experimentos

def resolver_problema_completo(n_torres=15, k_frecuencias=4, densidad=0.3, 
                               estrategia_greedy='mixto', metodo_busqueda='hill_climbing_con_conflictos',
                               max_iteraciones=500, visualizar=True, semilla=None):
    """
    Función principal mejorada: crea problema y encuentra solución
    
    Args:
        n_torres: número de torres
        k_frecuencias: número de frecuencias
        densidad: densidad del grafo (0 a 1)
        estrategia_greedy: 'grado', 'costo', 'mixto', 'aleatorio'
        metodo_busqueda: 'hill_climbing', 'tabu_search', 'hill_climbing_con_conflictos'
        max_iteraciones: máximo de iteraciones para búsqueda local
        visualizar: si True, genera visualización
        semilla: semilla para reproducibilidad
    """
    print("="*70)
    print("RESOLVIENDO PROBLEMA DE ASIGNACIÓN DE FRECUENCIAS (MEJORADO)")
    print("="*70)
    
    # 1. Crear problema
    print("\n1. CREANDO PROBLEMA...")
    print("-"*40)
    
    if semilla is not None:
        print(f"   Usando semilla: {semilla}")
    
    problema = crear_problema(n_torres, k_frecuencias, densidad, semilla)
    
    print(f"   - {n_torres} torres, {k_frecuencias} frecuencias")
    print(f"   - Interferencias: {problema['grafo'].numero_interferencias()}")
    print(f"   - Densidad del grafo: {problema['grafo'].densidad():.2f}")
    print(f"   - Grado máximo: {problema['grafo'].grado_maximo()}")
    
    # 2. Aplicar algoritmo greedy MEJORADO
    print(f"\n2. APLICANDO ALGORITMO GREEDY MEJORADO ({estrategia_greedy})...")
    print("-"*40)
    
    inicio = time.time()
    
    # Usar greedy con reintentos para mejor calidad
    solucion_inicial = greedy_con_reintentos(problema, reintentos=5)  # Aumentado reintentos
    
    tiempo_greedy = time.time() - inicio
    
    valida, costo_inicial, conflictos = verificar_solucion(problema, solucion_inicial)
    
    print(f"   - Tiempo: {tiempo_greedy:.4f} segundos")
    print(f"   - Costo inicial: {costo_inicial:.2f}")
    print(f"   - Válida: {valida}")
    
    if not valida:
        conflictos_reales = [c for c in conflictos if isinstance(c, tuple)]
        print(f"   - Conflictos: {len(conflictos_reales)}")
        # Si hay errores de rango, mostrarlos
        errores_rango = [c for c in conflictos if isinstance(c, str)]
        if errores_rango:
            print(f"   - Errores de rango: {len(errores_rango)}")
    
    # 3. Aplicar búsqueda local MEJORADA
    print(f"\n3. MEJORANDO CON {metodo_busqueda.upper()}...")
    print("-"*40)
    
    inicio = time.time()
    
    # Siempre usar hill_climbing_con_conflictos si está disponible (más robusto)
    if metodo_busqueda == 'hill_climbing_con_conflictos':
        try:
            # Usar hill climbing mejorado que permite conflictos controlados
            solucion_mejorada, costo_mejorado, info = hill_climbing_con_conflictos(
                problema, solucion_inicial, costo_inicial, max_iteraciones
            )
        except Exception as e:
            print(f"   Error en hill_climbing_con_conflictos: {e}")
            # Fallback a hill climbing estándar
            solucion_mejorada, costo_mejorado, info = mejorar_solucion(
                problema, solucion_inicial, 
                max_iter=max_iteraciones, 
                metodo='hill_climbing'
            )
    elif metodo_busqueda == 'tabu_search':
        solucion_mejorada, costo_mejorado, info = mejorar_solucion(
            problema, solucion_inicial, 
            max_iter=max_iteraciones, 
            metodo='tabu_search'
        )
    else:
        # Por defecto, usar hill climbing con conflictos
        try:
            solucion_mejorada, costo_mejorado, info = hill_climbing_con_conflictos(
                problema, solucion_inicial, costo_inicial, max_iteraciones
            )
        except:
            solucion_mejorada, costo_mejorado, info = mejorar_solucion(
                problema, solucion_inicial, 
                max_iter=max_iteraciones, 
                metodo='hill_climbing'
            )
    
    tiempo_busqueda = time.time() - inicio
    
    # Verificar que tengamos una solución
    if solucion_mejorada is None:
        print("   ¡ADVERTENCIA: No se encontró solución mejorada! Usando solución inicial.")
        solucion_mejorada = solucion_inicial
        costo_mejorado = costo_inicial
        info = "No se encontraron mejoras"
    
    valida_final, costo_final, conflictos_final = verificar_solucion(problema, solucion_mejorada)
    
    print(f"   - Tiempo: {tiempo_busqueda:.4f} segundos")
    print(f"   - {info}")
    print(f"   - Costo final: {costo_final:.2f}")
    print(f"   - Válida final: {valida_final}")
    
    # Calcular mejora porcentual CORRECTAMENTE
    if costo_inicial > 0:
        if costo_final < costo_inicial:
            mejora_porcentual = ((costo_inicial - costo_final) / costo_inicial) * 100
            print(f"   - Mejora: {mejora_porcentual:.2f}% (reducción)")
        else:
            # Si el costo aumentó, mostrar como negativo
            deterioro_porcentual = ((costo_final - costo_inicial) / costo_inicial) * 100
            print(f"   - Deterioro: {deterioro_porcentual:.2f}% (aumento)")
    else:
        print(f"   - Mejora: 0.00%")
    
    # 4. Análisis detallado
    print("\n4. ANÁLISIS DETALLADO DE LA SOLUCIÓN...")
    print("-"*40)
    
    analisis = analizar_solucion(problema, solucion_mejorada)
    
    print(f"   - Frecuencias utilizadas: {analisis['frecuencias_utilizadas']}/{k_frecuencias}")
    print(f"   - Costo promedio por torre: {analisis['costo_promedio']:.2f}")
    print(f"   - Eficiencia: {analisis['eficiencia_porcentaje']:.1f}% de torres con frecuencia óptima")
    print(f"   - Balance de carga: {analisis['balance_carga_porcentaje']:.1f}%")
    
    # Mostrar las torres más caras
    if analisis['torres_mas_caras']:
        print(f"   - Torres más caras:")
        for torre, freq, costo, grado in analisis['torres_mas_caras'][:3]:
            print(f"       Torre {torre}: frecuencia {freq}, costo {costo:.2f}, grado {grado}")
    
    # 5. Visualización (si se solicita y el problema no es muy grande)
    if visualizar and n_torres <= 25:
        print("\n5. GENERANDO VISUALIZACIÓN...")
        print("-"*40)
        
        titulo = f"Solución: {metodo_busqueda.title()} (n={n_torres}, k={k_frecuencias})"
        nombre_archivo = dibujar_solucion(problema, solucion_mejorada, titulo, guardar_archivo=True)
        
        if nombre_archivo:
            print(f"   - Imagen guardada: {nombre_archivo}")
    
    # 6. Resumen final
    print("\n" + "="*70)
    print("RESUMEN FINAL")
    print("="*70)
    
    print(f"CONFIGURACIÓN:")
    print(f"  - Torres: {n_torres}, Frecuencias: {k_frecuencias}")
    print(f"  - Densidad: {densidad}, Greedy: {estrategia_greedy}, Búsqueda: {metodo_busqueda}")
    
    print(f"\nRESULTADOS:")
    print(f"  Costo inicial (greedy): {costo_inicial:.2f}")
    print(f"  Costo final:            {costo_final:.2f}")
    
    # Calcular y mostrar mejora de forma clara
    if costo_inicial > 0:
        if costo_final < costo_inicial:
            mejora = ((costo_inicial - costo_final) / costo_inicial) * 100
            print(f"  Mejora:                 {mejora:.2f}% (reducción)")
        else:
            deterioro = ((costo_final - costo_inicial) / costo_inicial) * 100
            print(f"  Deterioro:              {deterioro:.2f}% (aumento)")
    else:
        print(f"  Mejora:                 0.00%")
    
    print(f"  Tiempo total:           {tiempo_greedy + tiempo_busqueda:.4f} segundos")
    print(f"  Solución válida:        {valida_final}")
    
    # Calcular número de conflictos
    conflictos_finales = len([c for c in conflictos_final if isinstance(c, tuple)])
    conflictos_iniciales = len([c for c in conflictos if isinstance(c, tuple)])
    
    if conflictos_iniciales > 0 or conflictos_finales > 0:
        print(f"  Conflictos iniciales:   {conflictos_iniciales}")
        print(f"  Conflictos finales:     {conflictos_finales}")
    
    # 7. Guardar resultados en archivo JSON
    resultados = {
        'configuracion': {
            'n_torres': n_torres,
            'k_frecuencias': k_frecuencias,
            'densidad': densidad,
            'estrategia_greedy': estrategia_greedy,
            'metodo_busqueda': metodo_busqueda,
            'max_iteraciones': max_iteraciones,
            'semilla': semilla
        },
        'resultados': {
            'costo_inicial': float(costo_inicial),
            'costo_final': float(costo_final),
            'mejora_porcentual': float(((costo_inicial - costo_final) / costo_inicial * 100) if costo_inicial > 0 else 0),
            'tiempo_total': float(tiempo_greedy + tiempo_busqueda),
            'valida_inicial': valida,
            'valida_final': valida_final,
            'conflictos_iniciales': conflictos_iniciales,
            'conflictos_finales': conflictos_finales
        },
        'analisis': {
            'frecuencias_utilizadas': analisis['frecuencias_utilizadas'],
            'costo_promedio': float(analisis['costo_promedio']),
            'eficiencia_porcentaje': float(analisis['eficiencia_porcentaje']),
            'balance_carga_porcentaje': float(analisis['balance_carga_porcentaje'])
        }
    }
    
    # Guardar en archivo
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo_resultados = f"resultados_{n_torres}t_{k_frecuencias}f_{timestamp}.json"
    
    with open(nombre_archivo_resultados, 'w') as f:
        json.dump(resultados, f, indent=2)
    
    print(f"\n  Resultados guardados en: {nombre_archivo_resultados}")
    print("="*70)
    
    return {
        'problema': problema,
        'solucion_inicial': solucion_inicial,
        'solucion_final': solucion_mejorada,
        'costo_inicial': costo_inicial,
        'costo_final': costo_final,
        'analisis': analisis,
        'resultados_archivo': nombre_archivo_resultados
    }

def menu_interactivo():
    """Menú interactivo para configurar la ejecución"""
    print("\n" + "="*70)
    print("CONFIGURADOR INTERACTIVO - ASIGNACIÓN DE FRECUENCIAS")
    print("="*70)
    
    print("\nCONFIGURACIÓN DEL PROBLEMA:")
    
    # Número de torres
    while True:
        try:
            n_torres = input("  Número de torres [15]: ").strip()
            if n_torres == "":
                n_torres = 15
            else:
                n_torres = int(n_torres)
            
            if n_torres <= 0:
                print("  Error: debe ser un número positivo")
                continue
            break
        except ValueError:
            print("  Error: ingrese un número válido")
    
    # Número de frecuencias
    while True:
        try:
            k_frecuencias = input("  Número de frecuencias [4]: ").strip()
            if k_frecuencias == "":
                k_frecuencias = 4
            else:
                k_frecuencias = int(k_frecuencias)
            
            if k_frecuencias <= 0:
                print("  Error: debe ser un número positivo")
                continue
            break
        except ValueError:
            print("  Error: ingrese un número válido")
    
    # Densidad del grafo
    while True:
        try:
            densidad = input("  Densidad del grafo (0.1 a 0.9) [0.3]: ").strip()
            if densidad == "":
                densidad = 0.3
            else:
                densidad = float(densidad)
            
            if densidad < 0.1 or densidad > 0.9:
                print("  Error: debe estar entre 0.1 y 0.9")
                continue
            break
        except ValueError:
            print("  Error: ingrese un número válido")
    
    print("\nCONFIGURACIÓN DE ALGORITMOS:")
    
    # Estrategia greedy
    print("  Estrategia Greedy:")
    print("    1. Por grado (recomendado para grafos densos)")
    print("    2. Por costo mínimo")
    print("    3. Mixto (grado × variabilidad de costos) [RECOMENDADO]")
    print("    4. Aleatorio")
    
    while True:
        opcion = input("  Seleccione opción (1-4) [3]: ").strip()
        if opcion == "":
            estrategia = 'mixto'
            break
        elif opcion == "1":
            estrategia = 'grado'
            break
        elif opcion == "2":
            estrategia = 'costo'
            break
        elif opcion == "3":
            estrategia = 'mixto'
            break
        elif opcion == "4":
            estrategia = 'aleatorio'
            break
        else:
            print("  Error: opción no válida")
    
    # Método de búsqueda
    print("\n  Método de Búsqueda Local:")
    print("    1. Hill Climbing mejorado (permite conflictos temporales) [RECOMENDADO]")
    print("    2. Tabu Search (más lento, evita óptimos locales)")
    print("    3. Hill Climbing estándar (rápido, pero limitado)")
    
    while True:
        opcion = input("  Seleccione opción (1-3) [1]: ").strip()
        if opcion == "":
            metodo = 'hill_climbing_con_conflictos'
            break
        elif opcion == "1":
            metodo = 'hill_climbing_con_conflictos'
            break
        elif opcion == "2":
            metodo = 'tabu_search'
            break
        elif opcion == "3":
            metodo = 'hill_climbing'
            break
        else:
            print("  Error: opción no válida")
    
    # Iteraciones
    while True:
        try:
            iteraciones = input("  Iteraciones de búsqueda local [500]: ").strip()
            if iteraciones == "":
                iteraciones = 500
            else:
                iteraciones = int(iteraciones)
            
            if iteraciones <= 0:
                print("  Error: debe ser un número positivo")
                continue
            break
        except ValueError:
            print("  Error: ingrese un número válido")
    
    # Visualización
    visualizar_input = input("  ¿Generar visualización? (s/n) [s]: ").strip().lower()
    visualizar = visualizar_input != 'n'
    
    # Semilla para reproducibilidad
    semilla_input = input("  Semilla para reproducibilidad (dejar vacío para aleatorio): ").strip()
    if semilla_input == "":
        semilla = None
    else:
        try:
            semilla = int(semilla_input)
        except ValueError:
            print("  Usando semilla aleatoria")
            semilla = None
    
    print("\n" + "="*70)
    print("CONFIGURACIÓN COMPLETADA")
    print("="*70)
    
    return {
        'n_torres': n_torres,
        'k_frecuencias': k_frecuencias,
        'densidad': densidad,
        'estrategia_greedy': estrategia,
        'metodo_busqueda': metodo,
        'max_iteraciones': iteraciones,
        'visualizar': visualizar,
        'semilla': semilla
    }

def ejecutar_ejemplo_rapido():
    """Ejecuta un ejemplo rápido con parámetros predeterminados"""
    print("\n" + "="*70)
    print("EJEMPLO RÁPIDO - 15 TORRES, 4 FRECUENCIAS")
    print("="*70)
    
    resultado = resolver_problema_completo(
        n_torres=15,
        k_frecuencias=4,
        densidad=0.3,
        estrategia_greedy='mixto',
        metodo_busqueda='hill_climbing_con_conflictos',  # Método mejorado
        max_iteraciones=300,
        visualizar=True,
        semilla=42
    )
    
    return resultado

if __name__ == "__main__":
    print("\n" + "="*70)
    print("SISTEMA DE ASIGNACIÓN ÓPTIMA DE FRECUENCIAS")
    print("Problema NP-Completo - Solución con Heurísticas Avanzadas")
    print("="*70)
    
    print("\nMODO DE EJECUCIÓN:")
    print("  1. Interactivo (configurar parámetros)")
    print("  2. Ejemplo rápido (15 torres, 4 frecuencias)")
    print("  3. Ejecutar varios experimentos")
    
    while True:
        opcion = input("\nSeleccione opción (1-3) [2]: ").strip()
        
        if opcion == "" or opcion == "2":
            resultado = ejecutar_ejemplo_rapido()
            break
        elif opcion == "1":
            config = menu_interactivo()
            resultado = resolver_problema_completo(**config)
            break
        elif opcion == "3":
            ejecutar_varios_experimentos()
            break
        else:
            print("Opción no válida. Intente de nuevo.")