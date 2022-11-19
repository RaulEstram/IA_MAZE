import random


def getlinesFromDefaultMaze():
    try:
        with open("cleanMaze.csv", "r") as file:
            list_data = file.readlines()
            return list_data
    except:
        return False


def generateWallsForMaze(defaultMaze: list, numberWalls: int):
    print(defaultMaze[64])
    count = 0
    while count != numberWalls:
        cell_number = random.randint(1, 64)
        new_data = putWall(defaultMaze[cell_number])
        if new_data:
            defaultMaze[cell_number] = new_data
            count += 1
    return defaultMaze


def putWall(data: str):
    cell_data = data.split(",")
    if '1' not in cell_data:
        return False
    index = []
    for index_data in range(len(cell_data)):
        if cell_data[index_data] == "1" or cell_data[index_data] == "1\n":
            index.append(index_data)

    i = random.choice(index)
    if cell_data[i] == "1":
        cell_data[i] = "0"
    if cell_data[i] == "1\n":
        cell_data[i] = "0\n"
    return ",".join(cell_data)


def generateMaze(numbersWalls: int):
    default_maze = getlinesFromDefaultMaze()

    if not default_maze: return False

    maze_with_walls = generateWallsForMaze(default_maze, numbersWalls)


generateMaze(10)
