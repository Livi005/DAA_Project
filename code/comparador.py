import time
from verificador import verificar_solucion

def comparar_algoritmos(problema, metodos):
    """
    Compara varios algoritmos en mismo problema
    
    metodos: lista de funciones que toman problema y retornan asignación
    """
    resultados = []
    
    for nombre, funcion in metodos:
        inicio = time.time()
        asignacion = funcion(problema)
        tiempo = time.time() - inicio
        
        valida, costo, conflictos = verificar_solucion(problema, asignacion)
        
        resultados.append({
            'algoritmo': nombre,
            'tiempo': tiempo,
            'costo': costo,
            'valida': valida,
            'conflictos': len(conflictos)
        })
    
    return resultados