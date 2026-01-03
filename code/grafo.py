class Grafo:
    """Solo guarda conexiones entre torres"""
    def __init__(self, n):
        self.n = n  # número de torres
        self.vecinos = [[] for _ in range(n)]
    
    def conectar(self, i, j):
        """Añade interferencia entre torres i y j"""
        # Validación de índices
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            raise ValueError(f"Índices fuera de rango: ({i}, {j}) con n={self.n}")
        if i == j:
            return  # No conectamos un nodo consigo mismo
        
        # Evitar duplicados
        if j not in self.vecinos[i]:
            self.vecinos[i].append(j)
        if i not in self.vecinos[j]:
            self.vecinos[j].append(i)
    
    def son_vecinos(self, i, j):
        """Verifica si dos torres interfieren"""
        if i < 0 or i >= self.n or j < 0 or j >= self.n:
            return False
        return j in self.vecinos[i]
    
    def obtener_vecinos(self, i):
        """Retorna torres que interfieren con i"""
        if i < 0 or i >= self.n:
            return []
        return self.vecinos[i]
    
    # Métodos adicionales para análisis
    def grado_maximo(self):
        """Retorna el grado máximo del grafo"""
        if not self.vecinos:
            return 0
        return max(len(vecinos) for vecinos in self.vecinos)
    
    def numero_interferencias(self):
        """Retorna el número total de interferencias (aristas)"""
        total = sum(len(vecinos) for vecinos in self.vecinos)
        return total // 2  # Cada arista se cuenta dos veces
    
    def densidad(self):
        """Retorna la densidad del grafo (0 a 1)"""
        if self.n <= 1:
            return 0
        max_aristas = self.n * (self.n - 1) / 2
        return self.numero_interferencias() / max_aristas