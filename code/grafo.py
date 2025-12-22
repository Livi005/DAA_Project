class Grafo:
    """Solo guarda conexiones entre torres"""
    def __init__(self, n):
        self.n = n  # número de torres
        self.vecinos = [[] for _ in range(n)]
    
    def conectar(self, i, j):
        """Añade interferencia entre torres i y j"""
        self.vecinos[i].append(j)
        self.vecinos[j].append(i)
    
    def son_vecinos(self, i, j):
        """Verifica si dos torres interfieren"""
        return j in self.vecinos[i]
    
    def obtener_vecinos(self, i):
        """Retorna torres que interfieren con i"""
        return self.vecinos[i]