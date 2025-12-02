import csv
import networkx as nx
import matplotlib.pyplot as plt
import os

class UnionFind:
    """
    Estructura de datos para manejar conjuntos disjuntos.
    Necesaria para verificar ciclos en el algoritmo de Kruskal.
    """
    def __init__(self, nodos):
        self.parent = {nodo: nodo for nodo in nodos}
    
    def find(self, nodo):
        if self.parent[nodo] != nodo:
            self.parent[nodo] = self.find(self.parent[nodo])
        return self.parent[nodo]
    
    def union(self, nodo1, nodo2):
        root1 = self.find(nodo1)
        root2 = self.find(nodo2)
        if root1 != root2:
            self.parent[root1] = root2
            return True
        return False

def leer_grafo(ruta_archivo):
    """
    Lee el archivo CSV. Reutilizamos la lógica.
    """
    aristas = []
    nodos = set()
    
    with open(ruta_archivo, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Saltar cabecera
        
        for fila in reader:
            if not fila: continue
            u, v, p = fila[0], fila[1], int(fila[2])
            aristas.append((u, v, p))
            nodos.add(u)
            nodos.add(v)
            
    return list(nodos), aristas

def algoritmo_kruskal(nodos, aristas):
    """
    Implementa el algoritmo de Kruskal.
    1. Ordena aristas por peso.
    2. Usa Union-Find para agregar aristas si no forman ciclo.
    
    Complejidad: O(E log E) o O(E log V).
    """
    mst = []
    uf = UnionFind(nodos)
    
    # Ordenar aristas por peso (de menor a mayor)
    # x[2] es el peso en la tupla (u, v, peso)
    aristas_ordenadas = sorted(aristas, key=lambda x: x[2])
    
    for u, v, peso in aristas_ordenadas:
        # Si u y v no están conectados, unirlos y agregar al MST
        if uf.union(u, v):
            mst.append((u, v, peso))
            
    return mst

def graficar_kruskal(aristas_originales, mst_aristas):
    """
    Genera la imagen kruskal_mst.png con el diseño mejorado.
    """
    G = nx.Graph()
    
    # Añadir todas las aristas base
    for u, v, w in aristas_originales:
        G.add_edge(u, v, weight=w)
        
    pos = nx.spring_layout(G, seed=42)
    
    plt.figure(figsize=(8, 6))
    
    # Dibujar base
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgreen') 
    nx.draw_networkx_edges(G, pos, width=1, alpha=0.4, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    
    # Dibujar MST
    mst_edges = [(u, v) for u, v, w in mst_aristas]
    nx.draw_networkx_edges(G, pos, edgelist=mst_edges, width=3, edge_color='blue') # Azul para Kruskal
    
    # Etiquetas de peso con fondo blanco
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                 font_color='black', 
                                 bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))
    
    plt.title("Algoritmo de Kruskal - MST (Azul)")
    plt.axis('off')
    
    # Nombre obligatorio de imagen 
    ruta_salida = "kruskal_mst.png"
    plt.savefig(ruta_salida, format="PNG")
    print(f"Imagen generada exitosamente: {ruta_salida}")
    plt.close()

if __name__ == "__main__":
    # Prueba rápida
    ruta = os.path.join("data", "grafos", "grafo.csv")
    print("--- Ejecutando Kruskal ---")
    
    nodos, aristas_totales = leer_grafo(ruta)
    mst_resultado = algoritmo_kruskal(nodos, aristas_totales)
    
    print("Aristas del MST:", mst_resultado)
    graficar_kruskal(aristas_totales, mst_resultado)