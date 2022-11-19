from pyamaze import *
from queue import PriorityQueue
import generateMaze

# duncion para obtener la distancia entre celdas
def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


# funcion con la logica del algoritmo A*
def aStar(laberintoData, xInicial, yInicial, xFinal, yFinal):
    # comprobacion de que los datos ingresados son correctos
    if xInicial > laberintoData.rows:
        return False
    if yInicial > laberintoData.cols:
        return False
    # almacenamos las cordenadas iniciales
    start = (xInicial, yInicial)

    # variables para calcular el costo o distancia
    g_score = {cell: float('inf') for cell in laberintoData.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in laberintoData.grid}
    f_score[start] = h(start, (xFinal, yFinal))

    # definimos algunas variables que utilizaremos posteriormente
    open = PriorityQueue()
    open.put((h(start, (xFinal, yFinal)), h(start, (xFinal, yFinal)), start))
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]
        # comprobamos si llegamos a la meta
        if currCell == (xFinal, yFinal):
            break
        # comrpbamos para donde nos podemos mover y nos movemos
        for d in 'ESNW':
            if laberintoData.maze_map[currCell][d] == True:
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                if d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                if d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                if d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                # variables temporales que ocuparemos
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, (xFinal, yFinal)) #TODO: cambiar si tan mal

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, h(childCell, (xFinal, yFinal)), childCell))
                    aPath[childCell] = currCell
    fwdPath = {}
    cell = (xFinal, yFinal)
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    return fwdPath


if __name__ == '__main__':
    m = maze(8, 8)
    generateMaze.generateMaze(60)
    #m.CreateMaze(x=1, y=1, saveMaze=False, loadMaze="maze--2022-11-19--14-19-44.csv")
    m.CreateMaze(x=1, y=1, saveMaze=False, loadMaze="maze.csv")
    path = aStar(m, 8, 8 , 1, 1)

    a = agent(m, footprints=True)
    m.tracePath({a: path})
    l = textLabel(m, 'A Star Path Length', len(path) + 1)

    m.run()
