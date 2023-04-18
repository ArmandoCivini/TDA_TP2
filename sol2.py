import sys

def distancia(p, q):
    return ((p[0] - q[0])**2 + (p[1] - q[1])**2) ** 0.5

def cargar_puntos(archivo):
    puntos = []
    with open(archivo) as f:
        for linea in f:
            coordenadas = linea.rstrip('\n').split(" ")
            puntos.append((float(coordenadas[0].replace(",",".")), float(coordenadas[1].replace(",","."))))
    
    return puntos

def calcular_peso(p1, p2, p3):
    return distancia(p1, p2) + distancia(p2, p3) + distancia(p3, p1)

def peso_poligono(triangulaciones, poligono, poligono_inicio, sub_triang, poligon_len):
    peso_triangulo = calcular_peso(poligono[poligono_inicio], poligono[sub_triang], poligono[poligono_inicio+poligon_len])
    peso_prev = triangulaciones[poligono_inicio][sub_triang]
    peso_post = triangulaciones[sub_triang][poligono_inicio+poligon_len]
    return peso_triangulo + peso_prev + peso_post

def triangular(poligono):
    n = len(poligono)
    triangulaciones = [[None] * n for _ in range(n)]
    
    for i in range(n):
        triangulaciones[i][i] = 0
        if i < n-1:
            triangulaciones[i][i+1] = 0
    
    for poligon_len in range(2, n):
        for poligono_inicio in range(n-poligon_len):
            triangulaciones[poligono_inicio][(poligono_inicio+poligon_len)] = \
                min([peso_poligono(triangulaciones, poligono, poligono_inicio, sub_triang, poligon_len) \
                for sub_triang in range(poligono_inicio+1,poligono_inicio+poligon_len)])

    return triangulaciones[0][n-1]

def main():
    poligono = cargar_puntos(sys.argv[1])
    peso = triangular(poligono)
    print(peso)

main()