import heapq
import os
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter

class NodoHuffman:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        
    # Definir comparadores para que el heap sepa ordenar nodos
    def __lt__(self, other):
        return self.freq < other.freq

def calcular_frecuencias(ruta_archivo):
    """Lee el archivo y cuenta la frecuencia de cada caracter."""
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        texto = f.read()
    return Counter(texto)

def construir_arbol(frecuencias):
    """Construye el árbol de Huffman usando una cola de prioridad."""
    heap = [NodoHuffman(char, freq) for char, freq in frecuencias.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        nodo1 = heapq.heappop(heap)
        nodo2 = heapq.heappop(heap)
        
        # Crear nodo padre sumando frecuencias
        merged = NodoHuffman(None, nodo1.freq + nodo2.freq)
        merged.left = nodo1
        merged.right = nodo2
        
        heapq.heappush(heap, merged)
        
    return heap[0] # Retorna la raíz del árbol

def generar_codigos(nodo, codigo_actual="", codigos={}):
    """Recorre el árbol para asignar 0s y 1s."""
    if nodo is None:
        return
    
    if nodo.char is not None:
        codigos[nodo.char] = codigo_actual
        return codigos
    
    generar_codigos(nodo.left, codigo_actual + "0", codigos)
    generar_codigos(nodo.right, codigo_actual + "1", codigos)
    return codigos

# --- Funciones de Graficación ---

def graficar_frecuencias(frecuencias):
    """Genera un gráfico de barras con las frecuencias."""
    chars = list(frecuencias.keys())
    counts = list(frecuencias.values())
    
    # Limpiar caracteres especiales para que se vean bien en la grafica
    chars_labels = [repr(c) if c.isspace() else c for c in chars]
    
    plt.figure(figsize=(10, 5))
    plt.bar(chars_labels, counts, color='skyblue')
    plt.xlabel('Caracteres')
    plt.ylabel('Frecuencia')
    plt.title('Frecuencia de Caracteres (Huffman)')
    
    # Nombre obligatorio 
    ruta = "huffman_freq.png"
    plt.savefig(ruta, format="PNG")
    print(f"Imagen generada: {ruta}")
    plt.close()

def graficar_arbol(raiz):
    """Dibuja el árbol binario de Huffman."""
    G = nx.DiGraph()
    labels = {}
    
    def agregar_aristas(nodo, id_nodo):
        if nodo is None: return
        
        # Crear etiqueta para el nodo (Char:Freq o solo Freq)
        if nodo.char:
            etiqueta = f"'{nodo.char}'\n{nodo.freq}"
            color = 'lightgreen'
        else:
            etiqueta = f"{nodo.freq}"
            color = 'lightgray'
            
        G.add_node(id_nodo, label=etiqueta, color=color)
        labels[id_nodo] = etiqueta
        
        if nodo.left:
            id_izq = id_nodo * 2
            G.add_edge(id_nodo, id_izq)
            agregar_aristas(nodo.left, id_izq)
            
        if nodo.right:
            id_der = id_nodo * 2 + 1
            G.add_edge(id_nodo, id_der)
            agregar_aristas(nodo.right, id_der)

    agregar_aristas(raiz, 1)
    
    # Layout jerarquico simple usando graphviz_layout si es posible, 
    # sino usamos un truco manual para árboles binarios
    pos = _hierarchy_pos(G, 1) 
    
    colores = [nx.get_node_attributes(G, 'color')[n] for n in G.nodes()]
    
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, node_size=2000, node_color=colores, arrows=False)
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    
    plt.title("Árbol de Huffman")
    
    # Nombre obligatorio 
    ruta = "huffman_tree.png"
    plt.savefig(ruta, format="PNG")
    print(f"Imagen generada: {ruta}")
    plt.close()

def _hierarchy_pos(G, root=None, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5):
    """
    Función auxiliar para posicionar los nodos en forma de árbol.
    No requiere librerías extra como pydot.
    """
    pos = _hierarchy_pos_recursive(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos_recursive(G, root, width, vert_gap, vert_loc, xcenter, pos = None, parent = None):
    if pos is None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
        
    children = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        children.remove(parent)  
        
    if len(children)!=0:
        dx = width/len(children) 
        nextx = xcenter - width/2 - dx/2
        for child in children:
            nextx += dx
            pos = _hierarchy_pos_recursive(G, child, dx, vert_gap, 
                                vert_loc-vert_gap, nextx, pos, parent=root)
    return pos

if __name__ == "__main__":
    ruta = os.path.join("data", "textos", "mensaje.txt")
    print("--- Ejecutando Huffman ---")
    
    try:
        frecuencias = calcular_frecuencias(ruta)
        print("Frecuencias calculadas:", frecuencias)
        
        # 1. Generar grafica de frecuencias
        graficar_frecuencias(frecuencias)
        
        # 2. Construir arbol
        raiz = construir_arbol(frecuencias)
        
        # 3. Generar codigos (para verificar en consola)
        codigos = generar_codigos(raiz)
        print("\nCódigos generados:")
        for char, code in codigos.items():
            print(f"'{char}': {code}")
            
        # 4. Generar imagen del árbol
        graficar_arbol(raiz)
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en {ruta}")