import sys


def distancia(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2) ** 0.5

def sumar_lados(triangulo):
    return distancia(triangulo[0], triangulo[1]) + distancia(triangulo[0], triangulo[2]) + distancia(triangulo[1], triangulo[2])

def crear_subpoligono(poligono, vertices_excluidos):
    return [v for v in poligono if v not in [poligono[u] for u in vertices_excluidos]]

def calcular_peso(triangulo, poligono):
    return sumar_lados([poligono[i] for i in triangulo])

def crear_triangulo(i, j, k):
    return tuple(sorted((i, j, k)))

def es_triangulo_valido(triangulo, vertices_excluidos):
    for indice in triangulo:
        if indice in vertices_excluidos:
            return False
    return True

def mapear_indices_a_vertices(poligono, triangulacion):
    triangulos = []
    for triangulo in triangulacion:
        triangulos.append((poligono[triangulo[0]], poligono[triangulo[1]], poligono[triangulo[2]]))

    return triangulos


def cargar_puntos(archivo):
    puntos = []
    with open(archivo) as f:
        for linea in f:
            coordenadas = linea.rstrip('\n').split(" ")
            puntos.append((float(coordenadas[0].replace(",",".")), float(coordenadas[1].replace(",","."))))
    
    return puntos

def imprimir_resultado(triangulacion, peso):
    print("Triángulos a armar: \n")
    for i in range(len(triangulacion)):
        print(f"Triángulo {i+1}: {triangulacion[i]}")
    print(f"Sumatoria total de la triangulacion: {peso}") 


def triangular(poligono): 
    triangulaciones = {}
    triangulaciones[0] = {}
    n = len(poligono)
    indice = {}
    
    for i in range(n):
        indice[poligono[i]] = i
        triangulo = crear_triangulo(i, (i+1)%n, (i+2)%n)  # cada triangulo esta formado por los los indices de los vertices en poligono
        triangulaciones[0][(triangulo, )] = {"peso": calcular_peso(triangulo, poligono), "excluidos": {(i+1)%n}}
    
    for i in range(1, n-2):
        triangulaciones[i] = {}
            
        for triangulos, info in triangulaciones[i-1].items():
            excluidos = info["excluidos"]
            peso = info["peso"]
            subpoligono = crear_subpoligono(poligono, excluidos)
            m = len(subpoligono)
            
            for j in range(m):
                nuevo_triangulo = crear_triangulo(indice[subpoligono[j]], indice[subpoligono[(j+1)%m]], indice[subpoligono[(j+2)%m]])
                if es_triangulo_valido(nuevo_triangulo, excluidos):
                    if nuevo_triangulo not in triangulos:
                        triangulaciones[i][tuple(sorted(list(triangulos) + [nuevo_triangulo]))] = {"peso" : peso + calcular_peso(nuevo_triangulo, poligono), "excluidos" : excluidos.union({indice[subpoligono[(j+1)%m]]})}

    triangulacion_minima = min(triangulaciones[n-3].keys(), key=lambda triangulacion: triangulaciones[n-3][triangulacion]["peso"])
    peso_minimo = triangulaciones[n-3][triangulacion_minima]["peso"]

    return triangulacion_minima, peso_minimo




def main():
    poligono = cargar_puntos(sys.argv[1])

    triangulacion, peso = triangular(poligono)
    triangulacion = mapear_indices_a_vertices(poligono, triangulacion)
    
    imprimir_resultado(triangulacion, peso)


main()