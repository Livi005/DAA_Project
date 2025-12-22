import random
import numpy as np 
from grafo import Grafo

def crear_problema(n_torres, k_frecuencias):
    """Crea problema aleatorio sin resolver"""
    grafo = Grafo(n_torres)
    
    # Conectar algunas torres aleatoriamente
    for i in range(n_torres):
        for j in range(i+1, n_torres):
            if random.random() < 0.3:  # 30% de probabilidad
                grafo.conectar(i, j)
    
    # Generar costos aleatorios
    costos = np.random.rand(n_torres, k_frecuencias) * 100
    
    return {
        'grafo': grafo,
        'k': k_frecuencias,
        'costos': costos,
        'n': n_torres
    }