import sys


def distancia(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


def sumar_lados(triangulo):
    return (
        distancia(triangulo[0], triangulo[1])
        + distancia(triangulo[0], triangulo[2])
        + distancia(triangulo[1], triangulo[2])
    )


def calcular_peso(triangulo, poligono):
    return sumar_lados([poligono[i] for i in triangulo])


def crear_triangulo(i, j, k):
    return tuple(sorted((i, j, k)))


def es_triangulo_valido(triangulo, indices_subpoligono):
    for indice in triangulo:
        if indice not in indices_subpoligono:
            return False
    return True


def mapear_indices_a_vertices(poligono, triangulacion):
    triangulos = []
    for triangulo in triangulacion:
        triangulos.append(
            (poligono[triangulo[0]], poligono[triangulo[1]],
                poligono[triangulo[2]])
        )

    return triangulos


def cargar_puntos(archivo):
    puntos = []
    with open(archivo) as f:
        for linea in f:
            coordenadas = linea.rstrip("\n").split(" ")
            puntos.append(
                (
                    float(coordenadas[0].replace(",", ".")),
                    float(coordenadas[1].replace(",", ".")),
                )
            )

    return puntos


def imprimir_resultado(triangulacion, peso):
    print("Triángulos a armar: \n")
    for i in range(len(triangulacion)):
        print(f"Triángulo {i+1}: {triangulacion[i]}")
    print(f"Sumatoria total de la triangulacion: {peso}")


def crear_subpoligono(poligono, indices_subpoligono):
    return [poligono[i] for i in indices_subpoligono]


def triangular(poligono):
    triangulaciones = {}
    triangulaciones[0] = {}
    n = len(poligono)
    indice = {}

    for i in range(n):
        indice[poligono[i]] = i
        triangulo = crear_triangulo(
            i, (i + 1) % n, (i + 2) % n
        )  # cada triangulo esta formado por los indices
        # de los vertices en poligono

        triangulaciones[0][(triangulo,)] = {
            "peso": calcular_peso(triangulo, poligono),
            "indices_subpoligono": {k for k in range(n) if k != (i + 1) % n},
        }

    for i in range(1, n - 2):
        triangulaciones[i] = {}

        for triangulos, info in triangulaciones[i - 1].items():
            indices_subpoligono = info["indices_subpoligono"]
            peso = info["peso"]
            subpoligono = crear_subpoligono(poligono, indices_subpoligono)
            m = len(subpoligono)

            for j in range(m):
                nuevo_triangulo = crear_triangulo(
                    indice[subpoligono[j]],
                    indice[subpoligono[(j + 1) % m]],
                    indice[subpoligono[(j + 2) % m]],
                )
                if nuevo_triangulo not in triangulos:
                    triangulaciones[i][
                        tuple(sorted(list(triangulos) + [nuevo_triangulo]))
                    ] = {
                        "peso":
                            peso + calcular_peso(nuevo_triangulo, poligono),
                        "indices_subpoligono": indices_subpoligono
                        - {indice[subpoligono[(j + 1) % m]]},
                    }

    triangulacion_minima = min(
        triangulaciones[n - 3].keys(),
        key=lambda triangulacion:
        triangulaciones[n - 3][triangulacion]["peso"],
    )
    peso_minimo = triangulaciones[n - 3][triangulacion_minima]["peso"]

    return triangulacion_minima, peso_minimo


def main():
    poligono = cargar_puntos(sys.argv[1])
    triangulacion, peso = triangular(poligono)
    triangulacion = mapear_indices_a_vertices(poligono, triangulacion)
    imprimir_resultado(triangulacion, peso)


main()
