import heapq
import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

def leer_grafo(ruta_archivo):
    """
    Lee un archivo CSV y retorna una lista de adyacencia.
    
    Argumentos:
        ruta_archivo (str): Ruta relativa al archivo CSV.
        
    Retorna:
        dict: Diccionario donde las claves son nodos y los valores 
              son listas de tuplas (vecino, peso).
        list: Lista de todas las aristas (u, v, peso) para graficar.
    """
    adj = {}
    aristas = []
    
    with open(ruta_archivo, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar cabecera: origen,destino,peso
        
        for fila in reader:
            if not fila: continue
            u, v, p = fila[0], fila[1], int(fila[2])
            
            # Agregar arista para grafo no dirigido
            if u not in adj: adj[u] = []
            if v not in adj: adj[v] = []
            
            adj[u].append((v, p))
            adj[v].append((u, p))
            aristas.append((u, v, p))
            
    return adj, aristas

def algoritmo_prim(adj, nodo_inicio):
    """
    Implementa el algoritmo de Prim para encontrar el MST.
    
    Complejidad: O(E log V) usando Binary Heap.
    
    Argumentos:
        adj (dict): Lista de adyacencia del grafo.
        nodo_inicio (str): Nodo desde el cual comenzar.
        
    Retorna:
        list: Lista de aristas que forman el MST [(u, v, peso)].
    """
    mst = []
    visitados = set()
    min_heap = [(0, nodo_inicio, None)]  # (peso, nodo_actual, padre)
    
    while min_heap:
        peso, u, padre = heapq.heappop(min_heap)
        
        if u in visitados:
            continue
            
        visitados.add(u)
        
        if padre is not None:
            mst.append((padre, u, peso))
            
        for v, w in adj[u]:
            if v not in visitados:
                heapq.heappush(min_heap, (w, v, u))
                
    return mst

def graficar_prim(aristas_originales, mst_aristas):
    """
    Genera y guarda la imagen del MST comparado con el grafo original.
    """
    G = nx.Graph()
    
    # Añadir todas las aristas
    for u, v, w in aristas_originales:
        G.add_edge(u, v, weight=w)
        
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(8, 6))
    
    # 1. Dibujar nodos y aristas base (gris)
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.4, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    
    # 2. Dibujar el MST (Rojo) 
    mst_edges = [(u, v) for u, v, w in mst_aristas]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3, edge_color='red')
    
    # 3. Dibujar etiquetas de peso de las aristas
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                 font_color='black', 
                                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7)) 
                                 # El bbox pone un fondito blanco suave tras el numero
    
    plt.title("Algoritmo de Prim - MST (Rojo)")
    plt.axis('off')
    
    ruta_salida = "prim_mst.png"
    plt.savefig(ruta_salida, format="PNG")
    print(f"Imagen generada exitosamente: {ruta_salida}")
    plt.close()

if __name__ == "__main__":
    # Bloque de prueba rapida
    ruta = os.path.join("data", "grafos", "grafo.csv")
    
    print("--- Ejecutando Prim ---")
    grafo, aristas_totales = leer_grafo(ruta)
    
    # Asumimos que inicia en el primer nodo que encuentre (ejemplo: 'A')
    primer_nodo = list(grafo.keys())[0]
    
    mst_resultado = algoritmo_prim(grafo, primer_nodo)
    
    print("Aristas del MST:", mst_resultado)
    graficar_prim(aristas_totales, mst_resultado)