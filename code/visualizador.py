def dibujar_solucion(problema, asignacion, titulo=""):
    """
    Muestra grafo con colores según frecuencia asignada
    
    Solo para visualización, no modifica datos
    """
    import matplotlib.pyplot as plt
    import networkx as nx
    
    grafo = problema['grafo']
    G = nx.Graph()
    
    # Añadir nodos con colores
    for i in range(problema['n']):
        G.add_node(i, color=asignacion[i] if i < len(asignacion) else 0)
    
    # Añadir aristas
    for i in range(problema['n']):
        for j in grafo.obtener_vecinos(i):
            if i < j:
                G.add_edge(i, j)
    
    # Dibujar
    pos = nx.spring_layout(G)
    colores = [G.nodes[i]['color'] for i in G.nodes()]
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, node_color=colores, with_labels=True, 
            cmap=plt.cm.tab20, node_size=500)
    
    plt.title(f"{titulo}\nCosto: {analizar_solucion(problema, asignacion)['costo_total']:.2f}")
    plt.show()