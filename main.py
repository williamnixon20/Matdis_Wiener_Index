import math

graph = dict()
visited = dict()
carbon_path = dict()

dist_matrix = ""
carbon = ""


def addEdge(node1, node2):
    if node1 not in graph:
        graph[node1] = []
    if node2 not in graph:
        graph[node2] = []

    graph[node1].append(node2)


def addToMatrix(srcNode, child, path):
    global dist_matrix
    srcNode = int(srcNode.strip("C"))
    child = int(child.strip("C"))
    dist_matrix[srcNode - 1][child - 1] = path


def dfs(srcNode, currNode, path):
    if currNode in visited:
        return
    else:
        visited[currNode] = True
    children = graph[currNode]
    for child in children:
        if child not in visited:
            setBaru = frozenset([srcNode, child])

            if setBaru not in carbon_path:
                carbon_path[setBaru] = path + 1

            addToMatrix(srcNode, child, path + 1)
            dfs(srcNode, child, path + 1)


def getDeltaBoiling(numCarbon, deltaWiener, deltaPol):
    return 98 / (numCarbon * numCarbon) * deltaWiener + (5.5 * deltaPol)


def getNormalParaffin(numCarbon):
    weight = 1 / 6 * (numCarbon - 1) * numCarbon * (numCarbon + 1)
    polarity = numCarbon - 3
    temp = (745.42 * math.log(numCarbon + 4.4, 10)) - 689.4
    return temp, weight, polarity


def getWienerIndexAndPolarityFromMatrix():
    global dist_matrix
    wiener_idx = 0
    polarity_number = 0
    for baris in dist_matrix:
        for elemen in baris:
            wiener_idx += elemen
            if elemen == 3:
                polarity_number += 1
    return (wiener_idx / 2, polarity_number / 2)


def setupGraph():
    global visited, dist_matrix, carbon
    print("Mengandung berapa atom karbon molekul parafinmu? (n >= 4)")
    carbon = input()

    print("Berikut merupakan atom karbon yang dapat digunakan.")
    for i in range(1, int(carbon) + 1):
        print("C{}".format(str(i)), end=" ")

    print("")
    dist_matrix = [[0 for x in range(int(carbon))] for y in range(int(carbon))]

    print("Silakan masukan banyak ikatan antar atom alkana Cn H2n+2")
    edges = input()
    print(
        "Terimakasih! Silakan masukan ikatan-ikatan tersebut (e.g: C1 C2, C2 C3, dst)"
    )
    for _ in range(int(edges)):
        carbon1, carbon2 = input().upper().split()
        addEdge(carbon1, carbon2)
        addEdge(carbon2, carbon1)


def getWienerIndexAndPolarityFromHashMap():
    wiener_idx = 0
    polarity_number = 0
    for key, val in carbon_path.items():
        set_carbon = list(key)
        # print(f"Ikatan karbon {set_carbon} memiliki jarak {val} ikatan.")
        wiener_idx += val
        if val == 3:
            polarity_number += 1
    return (wiener_idx, polarity_number)


def main():
    global visited, dist_matrix, carbon

    setupGraph()

    for key, val in graph.items():
        dfs(key, key, 0)
        visited = {}

    wiener_idx, polarity_number = getWienerIndexAndPolarityFromMatrix()
    temp_ref, wiener_ref, pol_ref = getNormalParaffin(int(carbon))
    delta = getDeltaBoiling(
        int(carbon), wiener_ref - wiener_idx, pol_ref - polarity_number
    )

    print("Distance matrix molekul:")
    for baris in dist_matrix:
        print(baris)

    print("Wiener indeks molekul adalah: ", wiener_idx)
    print("Polarity number molekul adalah: ", polarity_number)
    print("Temperatur titik didih referensi senyawa normal: ", temp_ref)
    print("Delta temperatur: ", delta)
    print(
        "Titik didih parafin anda adalah: ",
        round(temp_ref - delta, 1),
        "derajat Celcius",
    )


def predictCarbonAtoms(temperature):
    threshold = 10
    for i in range(4, 40):
        curr_temp, _, _ = getNormalParaffin(i)
        if abs(curr_temp - temperature) < threshold:
            print(
                "Senyawa ini mungkin memiliki {i} atom karbon dan memiliki rumus C{i}H{l}".format(
                    i=i, l=i * 2 + 2
                )
            )


if __name__ == "__main__":
    print("Berapa titik didih dari zat alkanamu?")
    boiling_point = input()
    predictCarbonAtoms(int(boiling_point))
    print(getNormalParaffin(30))
    main()
