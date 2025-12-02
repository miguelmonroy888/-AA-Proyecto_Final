import os
import sys

# Importamos las funciones de nuestros scripts en src
# Usamos alias (as) para evitar conflictos porque todos tienen una funcion "leer_grafo"
import src.prim as prim
import src.kruskal as kruskal
import src.dijkstra as dijkstra
import src.huffman as huffman

def limpiar_pantalla():
    """Limpia la consola para que se vea ordenado."""
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def ejecutar_prim():
    print("\n--- 1. ALGORITMO DE PRIM ---")
    ruta = os.path.join("data", "grafos", "grafo.csv")
    try:
        # Usamos las funciones del archivo prim.py
        grafo, aristas = prim.leer_grafo(ruta)
        nodo_inicio = list(grafo.keys())[0] # Tomamos el primero por defecto
        
        mst = prim.algoritmo_prim(grafo, nodo_inicio)
        print(f"MST calculado iniciando en {nodo_inicio}.")
        print("Aristas del MST:", mst)
        
        prim.graficar_prim(aristas, mst)
        print("Imagen 'prim_mst.png' actualizada correctamente.")
    except Exception as e:
        print(f"Error ejecutando Prim: {e}")
    input("\nPresione Enter para continuar...")

def ejecutar_kruskal():
    print("\n--- 2. ALGORITMO DE KRUSKAL ---")
    ruta = os.path.join("data", "grafos", "grafo.csv")
    try:
        nodos, aristas = kruskal.leer_grafo(ruta)
        
        mst = kruskal.algoritmo_kruskal(nodos, aristas)
        print("MST calculado con Kruskal.")
        print("Aristas del MST:", mst)
        
        kruskal.graficar_kruskal(aristas, mst)
        print("Imagen 'kruskal_mst.png' actualizada correctamente.")
    except Exception as e:
        print(f"Error ejecutando Kruskal: {e}")
    input("\nPresione Enter para continuar...")

def ejecutar_dijkstra():
    print("\n--- 3. ALGORITMO DE DIJKSTRA ---")
    ruta = os.path.join("data", "grafos", "grafo.csv")
    try:
        adj, aristas, nodos = dijkstra.leer_grafo(ruta)
        
        print(f"Nodos disponibles: {nodos}")
        origen = input("Ingrese el nodo de origen: ").strip().upper()
        
        if origen not in adj:
            print(f"Error: El nodo '{origen}' no existe.")
        else:
            dist, padres = dijkstra.algoritmo_dijkstra(adj, origen)
            print("\nDistancias mínimas:")
            for nodo, d in dist.items():
                print(f"A {nodo}: {d}")
            
            dijkstra.graficar_dijkstra(aristas, padres, origen)
            print("Imagen 'dijkstra_paths.png' actualizada correctamente.")
            
    except Exception as e:
        print(f"Error ejecutando Dijkstra: {e}")
    input("\nPresione Enter para continuar...")

def ejecutar_huffman():
    print("\n--- 4. ALGORITMO DE HUFFMAN ---")
    ruta = os.path.join("data", "textos", "mensaje.txt")
    try:
        print(f"Leyendo archivo: {ruta}")
        frecuencias = huffman.calcular_frecuencias(ruta)
        print("Frecuencias calculadas.")
        
        huffman.graficar_frecuencias(frecuencias)
        print("Grafica de frecuencias generada.")
        
        raiz = huffman.construir_arbol(frecuencias)
        codigos = huffman.generar_codigos(raiz)
        
        print("Códigos generados (muestra primeros 5):", list(codigos.items())[:5])
        
        huffman.graficar_arbol(raiz)
        print("Imagen del árbol generada correctamente.")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {ruta}")
    except Exception as e:
        print(f"Error ejecutando Huffman: {e}")
    input("\nPresione Enter para continuar...")

def menu():
    while True:
        limpiar_pantalla()
        print("========================================")
        print("   PROYECTO FINAL - ANALISIS DE ALGORITMOS")
        print("========================================")
        print("1. Ejecutar Prim")
        print("2. Ejecutar Kruskal")
        print("3. Ejecutar Dijkstra")
        print("4. Ejecutar Huffman")
        print("0. Salir")
        print("========================================")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == '1':
            ejecutar_prim()
        elif opcion == '2':
            ejecutar_kruskal()
        elif opcion == '3':
            ejecutar_dijkstra()
        elif opcion == '4':
            ejecutar_huffman()
        elif opcion == '0':
            print("Saliendo del programa...")
            break
        else:
            input("Opción no válida. Presione Enter para intentar de nuevo.")

if __name__ == "__main__":
    menu()