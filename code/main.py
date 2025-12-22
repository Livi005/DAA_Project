import time
from grafo import Grafo
from instancias import crear_problema
from verificador import verificar_solucion
from greedy_simple import asignacion_greedy
from busqueda_local import mejorar_solucion
from analizador import analizar_solucion
from visualizador import dibujar_solucion

def resolver_problema_completo(n_torres=10, k_frecuencias=3, visualizar=True):
    """
    Función principal: crea problema y encuentra solución usando módulos
    """
    print("="*60)
    print("RESOLVIENDO PROBLEMA DE ASIGNACIÓN DE FRECUENCIAS")
    print("="*60)
    
    print("\n1. Creando problema...")
    problema = crear_problema(n_torres, k_frecuencias)
    print(f"   - {n_torres} torres, {k_frecuencias} frecuencias")
    print(f"   - {sum(len(v) for v in problema['grafo'].vecinos)//2} interferencias")
    
    print("\n2. Aplicando algoritmo greedy...")
    inicio = time.time()
    solucion_inicial = asignacion_greedy(problema)
    tiempo_greedy = time.time() - inicio
    
    valida, costo_inicial, conflictos = verificar_solucion(problema, solucion_inicial)
    print(f"   - Tiempo: {tiempo_greedy:.3f}s")
    print(f"   - Costo inicial: {costo_inicial:.2f}")
    print(f"   - Válida: {valida}, Conflictos: {len(conflictos)}")
    
    print("\n3. Mejorando con búsqueda local...")
    inicio = time.time()
    solucion_mejorada, costo_mejorado, info = mejorar_solucion(problema, solucion_inicial)
    tiempo_mejora = time.time() - inicio
    
    valida_final, costo_final, conflictos_final = verificar_solucion(problema, solucion_mejorada)
    print(f"   - Tiempo: {tiempo_mejora:.3f}s")
    print(f"   - {info}")
    print(f"   - Costo final: {costo_final:.2f}")
    print(f"   - Mejora: {((costo_inicial - costo_final)/costo_inicial*100):.1f}%")
    
    print("\n4. Analizando solución...")
    analisis = analizar_solucion(problema, solucion_mejorada)
    print(f"   - Frecuencias utilizadas: {analisis['frecuencias_utilizadas']}/{k_frecuencias}")
    print(f"   - Costo promedio por torre: {analisis['costo_promedio']:.2f}")
    
    if visualizar and n_torres <= 20:
        print("\n5. Generando visualización...")
        dibujar_solucion(problema, solucion_mejorada, 
                        f"Solución Mejorada (n={n_torres}, k={k_frecuencias})")
    
    print("\n" + "="*60)
    print("RESUMEN FINAL:")
    print(f"Costo inicial: {costo_inicial:.2f}")
    print(f"Costo final:   {costo_final:.2f}")
    print(f"Mejora:        {((costo_inicial - costo_final)/costo_inicial*100):.1f}%")
    print(f"Tiempo total:  {(tiempo_greedy + tiempo_mejora):.3f}s")
    print("="*60)
    
    return {
        'problema': problema,
        'solucion_inicial': solucion_inicial,
        'solucion_final': solucion_mejorada,
        'costo_inicial': costo_inicial,
        'costo_final': costo_final,
        'analisis': analisis
    }

# Ejecutar si este archivo es el principal
if __name__ == "__main__":
    resultado = resolver_problema_completo(n_torres=15, k_frecuencias=4, visualizar=True)