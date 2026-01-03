import matplotlib
# Usar backend que no requiera interfaz gráfica
matplotlib.use('Agg')  # Esto evita el warning de FigureCanvasAgg

import matplotlib.pyplot as plt
import networkx as nx
from analizador import analizar_solucion
from verificador import verificar_solucion

def dibujar_solucion(problema, asignacion, titulo="", guardar_archivo=True):
    """
    Muestra grafo con colores según frecuencia asignada
    
    Args:
        problema: diccionario con el problema
        asignacion: lista de frecuencias
        titulo: título del gráfico
        guardar_archivo: si True, guarda la imagen en lugar de mostrarla
    
    Solo para visualización, no modifica datos
    """
    
    grafo = problema['grafo']
    n = problema['n']
    G = nx.Graph()
    
    # Añadir nodos con colores
    for i in range(n):
        G.add_node(i, color=asignacion[i] if i < len(asignacion) else 0)
    
    # Añadir aristas
    for i in range(n):
        for j in grafo.obtener_vecinos(i):
            if i < j:
                G.add_edge(i, j)
    
    # Verificar solución para añadir información al título
    valida, costo, conflictos = verificar_solucion(problema, asignacion)
    
    # Dibujar
    pos = nx.spring_layout(G, seed=42)  # seed para reproducibilidad
    colores = [G.nodes[i]['color'] for i in G.nodes()]
    
    plt.figure(figsize=(12, 10))
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, node_color=colores, 
                          cmap=plt.cm.tab20, node_size=600, alpha=0.8)
    
    # Dibujar aristas
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.5)
    
    # Etiquetas de nodos
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
    
    # Añadir información de costos en los nodos
    for i in range(n):
        x, y = pos[i]
        costo_torre = problema['costos'][i][asignacion[i]]
        plt.text(x, y-0.05, f'{costo_torre:.1f}', 
                fontsize=8, ha='center', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Resaltar aristas con conflictos
    if conflictos and len(conflictos) > 0 and isinstance(conflictos[0], tuple):
        # Extraer solo las tuplas de conflictos
        aristas_conflicto = [(i, j) for i, j in conflictos if isinstance(i, int) and isinstance(j, int)]
        nx.draw_networkx_edges(G, pos, edgelist=aristas_conflicto, 
                              width=3, alpha=0.8, edge_color='red')
    
    # Configurar título
    titulo_completo = f"{titulo}\n"
    titulo_completo += f"Costo: {costo:.2f} | "
    titulo_completo += f"Válida: {valida} | "
    titulo_completo += f"Conflictos: {len([c for c in conflictos if isinstance(c, tuple)])}"
    
    plt.title(titulo_completo, fontsize=14, fontweight='bold')
    
    # Añadir barra de colores para las frecuencias
    sm = plt.cm.ScalarMappable(cmap=plt.cm.tab20, 
                              norm=plt.Normalize(vmin=0, vmax=problema['k']-1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca(), shrink=0.8)
    cbar.set_label('Frecuencia', fontsize=12)
    
    plt.axis('off')
    plt.tight_layout()
    
    if guardar_archivo:
        # Generar nombre de archivo
        import time
        timestamp = int(time.time())
        nombre_archivo = f"solucion_n{n}_k{problema['k']}_{timestamp}.png"
        
        plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"  Gráfico guardado como: {nombre_archivo}")
        return nombre_archivo
    else:
        plt.show()
        return None

def visualizar_evolucion(problema, soluciones_intermedias, costos_intermedios):
    """
    Visualiza la evolución de la búsqueda local
    
    Args:
        problema: diccionario con el problema
        soluciones_intermedias: lista de soluciones en cada iteración
        costos_intermedios: lista de costos correspondientes
    """
    plt.figure(figsize=(12, 5))
    
    # Gráfico de evolución del costo
    plt.subplot(1, 2, 1)
    plt.plot(costos_intermedios, 'b-', linewidth=2)
    plt.xlabel('Iteración', fontsize=12)
    plt.ylabel('Costo', fontsize=12)
    plt.title('Evolución del Costo', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    
    # Gráfico de mejoras (diferencia entre iteraciones)
    mejoras = [0]
    for i in range(1, len(costos_intermedios)):
        mejora = costos_intermedios[i-1] - costos_intermedios[i]
        mejoras.append(mejora if mejora > 0 else 0)
    
    plt.subplot(1, 2, 2)
    plt.bar(range(len(mejoras)), mejoras, color='green', alpha=0.7)
    plt.xlabel('Iteración', fontsize=12)
    plt.ylabel('Mejora', fontsize=12)
    plt.title('Mejoras por Iteración', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # Guardar gráfico
    import time
    timestamp = int(time.time())
    nombre_archivo = f"evolucion_busqueda_{timestamp}.png"
    plt.savefig(nombre_archivo, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"  Gráfico de evolución guardado como: {nombre_archivo}")
    return nombre_archivo