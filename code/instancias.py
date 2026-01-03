import random
import numpy as np
from grafo import Grafo

def crear_problema(n_torres, k_frecuencias, densidad=0.3, semilla=None):
    """
    Crea problema aleatorio sin resolver
    
    Args:
        n_torres: número de torres
        k_frecuencias: número de frecuencias disponibles
        densidad: probabilidad de conexión (0 a 1)
        semilla: semilla para reproducibilidad
    """
    if semilla is not None:
        random.seed(semilla)
        np.random.seed(semilla)
    
    grafo = Grafo(n_torres)
    
    # Conectar algunas torres aleatoriamente con probabilidad dada por densidad
    for i in range(n_torres):
        for j in range(i+1, n_torres):
            if random.random() < densidad:
                grafo.conectar(i, j)
    
    # Generar costos más realistas: cada torre tiene una frecuencia preferida más barata
    costos = np.zeros((n_torres, k_frecuencias))
    
    for i in range(n_torres):
        # Cada torre tiene una frecuencia "preferida" (más barata)
        freq_preferida = random.randint(0, k_frecuencias-1)
        
        for j in range(k_frecuencias):
            if j == freq_preferida:
                # Frecuencia preferida: más barata
                costos[i][j] = random.uniform(5, 30)
            else:
                # Otras frecuencias: más caras
                costos[i][j] = random.uniform(30, 100)
    
    return {
        'grafo': grafo,
        'k': k_frecuencias,
        'costos': costos,
        'n': n_torres,
        'densidad': densidad
    }

def crear_problema_especial(tipo='arbol', n_torres=10, k_frecuencias=3, semilla=None):
    """
    Crea problemas especiales para pruebas
    
    Args:
        tipo: 'arbol', 'bipartito', 'completo'
        n_torres: número de torres
        k_frecuencias: número de frecuencias
        semilla: semilla para reproducibilidad
    """
    if semilla is not None:
        random.seed(semilla)
        np.random.seed(semilla)
    
    grafo = Grafo(n_torres)
    
    if tipo == 'arbol':
        # Crear un árbol (n-1 aristas, siempre 2-coloreable)
        for i in range(1, n_torres):
            padre = random.randint(0, i-1)
            grafo.conectar(i, padre)
    
    elif tipo == 'bipartito':
        # Grafo bipartito (también 2-coloreable)
        mitad = n_torres // 2
        for i in range(mitad):
            for j in range(mitad, n_torres):
                if random.random() < 0.5:  # 50% de probabilidad
                    grafo.conectar(i, j)
    
    elif tipo == 'completo':
        # Grafo completo (muy difícil para coloración)
        for i in range(n_torres):
            for j in range(i+1, n_torres):
                grafo.conectar(i, j)
    
    # Generar costos
    costos = np.random.rand(n_torres, k_frecuencias) * 100
    
    return {
        'grafo': grafo,
        'k': k_frecuencias,
        'costos': costos,
        'n': n_torres,
        'tipo': tipo
    }