import random
from mapeo import data_walls


def getlinesFromDefaultMaze():
    try:
        with open("cleanMaze.csv", "r") as file:
            list_data = file.readlines()
            return list_data
    except:
        return False


def generateWallsForMaze(defaultMaze: list, numberWalls: int):
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


def finishWalls(maze):
    walls = data_walls.copy()
    # mapeamos todos los obstaculos
    for index in range(1, len(maze)):
        data = list(maze[index])
        y = data[2]
        x = data[5]
        walls[f"{x}"][f"{y}"]["n"] = data[13]
        walls[f"{x}"][f"{y}"]["s"] = data[15]
        walls[f"{x}"][f"{y}"]["e"] = data[9]
        walls[f"{x}"][f"{y}"]["w"] = data[11]
    # asignamos correctamente los obstaculos
    for xkey in walls:
        for ykey in walls[xkey]:
            for cordinada in walls[xkey][ykey]:
                try:
                    value = walls[xkey][ykey][cordinada]
                    if value == "0":
                        if cordinada == "n":
                            new_y_key = f"{int(ykey) - 1}"
                            walls[xkey][new_y_key]["s"] = "0"
                        if cordinada == "s":
                            new_y_key = f"{int(ykey) + 1}"
                            walls[xkey][new_y_key]["n"] = "0"
                        if cordinada == "e":
                            new_x_key = f"{int(xkey) + 1}"
                            walls[new_x_key][ykey]["w"] = "0"
                        if cordinada == "w":
                            new_x_key = f"{int(xkey) - 1}"
                            walls[new_x_key][ykey]["e"] = "0"
                except KeyError:
                    pass
    return walls


def finishDictWithWallsToList(walls):
    clean_data = ["  cell  ,E,W,N,S\n"]
    for xkey in walls:
        for ykey in walls[xkey]:
            cor = walls[xkey][ykey]
            data = f'"({ykey}, {xkey})",{cor["e"]},{cor["w"]},{cor["n"]},{cor["s"]}\n'
            clean_data.append(data)
    return clean_data


def generateCsvFileMaze(maze_csv):
    with open("maze.csv", "w") as file:
        data = "".join(maze_csv)
        file.write(data)


def generateMaze(numbersWalls: int):
    default_maze = getlinesFromDefaultMaze()

    if not default_maze: return False

    maze_with_walls = generateWallsForMaze(default_maze, numbersWalls)

    finished_maze = finishWalls(maze_with_walls)

    definitive_maze = finishDictWithWallsToList(finished_maze)

    generateCsvFileMaze(definitive_maze)


