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

def triangular(poligono):
    #TODO: memorizar triangulos elegidos
    n = len(poligono)
    triangulaciones = [[None] * n for _ in range(n)] #genero matriz dinamica
    
    for i in range(n): #seteo los valores que no pueden ser triangulos a 0
        triangulaciones[i][i] = 0
        if i < n-1:
            triangulaciones[i][i+1] = 0
    
    for poligon_len in range(2, n): 
        #itero empezando por los poligonos de menor tamaño a los de mayor tamaño
        for poligono_inicio in range(n-poligon_len):
            #por cada punto del poligono genero el poligono de tamaño poligon_len trazando
            #una linea entre el punto y el punto y poligon_len posiciones mas adelante
            triangulaciones[poligono_inicio][(poligono_inicio+poligon_len)] = \
                min([peso_poligono(triangulaciones, poligono, poligono_inicio, sub_triang, poligon_len) \
                for sub_triang in range(poligono_inicio+1,poligono_inicio+poligon_len)])
            #dentro de ese poligono itero por cada uno de sus puntos que no sean extremos y
            #formo un triangulo entre ese punto y los extremos(poligono_inicio+1,poligono_inicio+poligon_len)
            

    return triangulaciones[0][n-1] #este valor representa el peso del poligono completo

def main():
    poligono = cargar_puntos(sys.argv[1])
    peso = triangular(poligono)
    print(peso)

main()