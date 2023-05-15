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
    #el peso del poligono es el peso del triangulo mas el peso de los poligonos que quedan
    #entre el punto y los extremos
    peso_triangulo = calcular_peso(poligono[poligono_inicio], poligono[sub_triang], poligono[poligono_inicio+poligon_len])
    peso_prev = triangulaciones[poligono_inicio][sub_triang]
    peso_post = triangulaciones[sub_triang][poligono_inicio+poligon_len]
    return peso_triangulo + peso_prev + peso_post


def imprimir_triangulacion(triangulacion, peso):
    print(f"Sumatoria obtenida: {peso}\n")
    print("Triangulos a armar: \n")
    for i in range(len(triangulacion)):
        print(f"triángulo {i+1} -> {triangulacion[i]}")


def triangular(poligono):
    n = len(poligono)
    infinito = float('inf')
    OPT = [[None]*n for _ in range(n)]
    triangulacion = [[[]]*n for _ in range(n)]

    for i in range(n):
        OPT[i][i] = 0
        triangulacion[i][i] = []
        if i < n - 1:
            OPT[i][i+1] = 0
            triangulacion[i][i+1] = []

    for tamanio in range(2,n):
        for i in range(n-tamanio):
            j = i + tamanio
            OPT[i][j] = infinito
            
            for k in range(i+1, j):
                peso = OPT[i][k] + OPT[k][j] + calcular_peso(poligono[i], poligono[j],poligono[k])
                if peso < OPT[i][j]:
                    OPT[i][j] = peso
                    # agrego como triangulacion a la triangulacion de los poligonos
                    # y al triangulo i,j,k
                    triangulacion[i][j] = triangulacion[i][k] + triangulacion[k][j] + [(poligono[i], poligono[j], poligono[k])]
    
    return OPT[0][n-1], triangulacion[0][n-1]





def main():
    poligono = cargar_puntos(sys.argv[1]) 
    
    peso, triangulacion = triangular(poligono)
    imprimir_triangulacion(triangulacion, peso)

main()