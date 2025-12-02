import heapq
import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

def leer_grafo(ruta_archivo):
    """
    Lee el grafo y devuelve la lista de adyacencia y todas las aristas.
    """
    adj = {}
    aristas = []
    nodes = set()
    
    with open(ruta_archivo, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        
        for fila in reader:
            if not fila: continue
            u, v, p = fila[0], fila[1], int(fila[2])
            
            if u not in adj: adj[u] = []
            if v not in adj: adj[v] = []
            
            adj[u].append((v, p))
            adj[v].append((u, p))
            aristas.append((u, v, p))
            nodes.add(u)
            nodes.add(v)
            
    return adj, aristas, sorted(list(nodes))

def algoritmo_dijkstra(adj, inicio):
    """
    Calcula las distancias más cortas desde 'inicio' a todos los nodos.
    Retorna: distancias y diccionario de padres para reconstruir rutas.
    """
    distancias = {nodo: float('inf') for nodo in adj}
    distancias[inicio] = 0
    padres = {nodo: None for nodo in adj}
    pq = [(0, inicio)]
    
    while pq:
        d_actual, u = heapq.heappop(pq)
        
        if d_actual > distancias[u]:
            continue
            
        for v, peso in adj[u]:
            distancia = d_actual + peso
            if distancia < distancias[v]:
                distancias[v] = distancia
                padres[v] = u
                heapq.heappush(pq, (distancia, v))
                
    return distancias, padres

def obtener_aristas_camino(padres, nodo_destino):
    """Reconstruye el camino desde el destino hasta el origen usando los padres."""
    camino = []
    actual = nodo_destino
    while padres[actual] is not None:
        u = padres[actual]
        camino.append((u, actual))
        actual = u
    return camino

def graficar_dijkstra(aristas_originales, padres, inicio):
    """
    Genera una imagen resaltando los caminos más cortos desde el nodo inicio.
    Nombre obligatorio: dijkstra_paths.png
    """
    G = nx.Graph()
    for u, v, w in aristas_originales:
        G.add_edge(u, v, weight=w)
        
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    
    # Dibujar todo el grafo en gris
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgray')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.4, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12)
    
    # Identificar todas las aristas que forman parte de los caminos cortos
    aristas_cortas = []
    nodos_visitados = set()
    
    # Reconstruir caminos hacia todos los nodos alcanzables
    for nodo in padres:
        if padres[nodo] is not None:
            aristas_cortas.append((padres[nodo], nodo))
            nodos_visitados.add(nodo)
            nodos_visitados.add(padres[nodo])

    # Resaltar caminos cortos en NARANJA
    nx.draw_networkx_edges(G, pos, edgelist=aristas_cortas, width=3, edge_color='orange')
    nx.draw_networkx_nodes(G, pos, nodelist=list(nodos_visitados), node_size=700, node_color='orange')
    
    # Resaltar nodo origen en verde
    nx.draw_networkx_nodes(G, pos, nodelist=[inicio], node_size=800, node_color='#00FF00')

    # Etiquetas de peso con fondo blanco
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                 font_color='black', 
                                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    plt.title(f"Dijkstra - Caminos cortos desde '{inicio}' (Naranja)")
    plt.axis('off')
    
    ruta_salida = "dijkstra_paths.png"
    plt.savefig(ruta_salida, format="PNG")
    print(f"Imagen generada exitosamente: {ruta_salida}")
    plt.close()

if __name__ == "__main__":
    ruta = os.path.join("data", "grafos", "grafo.csv")
    print("--- Ejecutando Dijkstra ---")
    
    adj, aristas, nodos = leer_grafo(ruta)
    
    # Interacción obligatoria
    print(f"Nodos disponibles: {nodos}")
    origen = input("Ingrese el nodo de origen: ").strip().upper()
    
    if origen not in adj:
        print(f"Error: El nodo '{origen}' no existe en el grafo.")
    else:
        dist, padres = algoritmo_dijkstra(adj, origen)
        
        print("\nDistancias mínimas:")
        for nodo, d in dist.items():
            print(f"A {nodo}: {d}")
            
        graficar_dijkstra(aristas, padres, origen)