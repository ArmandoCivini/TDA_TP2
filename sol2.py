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

def triangular(poligono):
    n = len(poligono)
    triangulaciones = [[None] * n for _ in range(n)]
    
    for i in range(n):
        triangulaciones[i][i] = 0
        if i < n-1:
            triangulaciones[i][i+1] = 0
    
    for i in range(2, n):
        for j in range(n-i):
            triangulaciones[j][(j+i)] = min([calcular_peso(poligono[j], poligono[k], poligono[j+i]) + triangulaciones[j][k] + triangulaciones[k][j+i] for k in range(j+1,j+i)])

    print(triangulaciones)
    return triangulaciones[0][n-1]

def main():
    poligono = cargar_puntos(sys.argv[1])
    peso = triangular(poligono)
    print(peso)

main()