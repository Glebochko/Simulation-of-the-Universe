def main():
    objCount = 4
    distance = [[0] * objCount for i in range(objCount)]
    for i in range(objCount):
        for j in range(i + 1, objCount):
            distance[i][j] = (i + 1) * 10 + j + 1
            distance[j][i] = distance[i][j]
        distance[i][i] = 0


    for i in range(objCount):
        for j in range(objCount):
            print(distance[i][j])



main()
                