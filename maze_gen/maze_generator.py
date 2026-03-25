from random import randint
from a_maze_ing import launcher


hex_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


def create_path(configs: dict, maze: list) -> None:
    x, y = configs['ENTRY']
    cursor = [x, y]
    x_ex, y_ex = configs['EXIT']
    exit_coords = [x_ex, y_ex]
    while x != x_ex and y != y_ex:
        movement = randint(0, 3)
        if movement == 0:
            if x > 0:
                maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 1]
                x -= 1
                if (hex_numbers.index(maze[x][y]) > 3
                    and hex_numbers.index(maze[x][y]) < 8
                    or hex_numbers.index(maze[x][y]) > 11):
                    maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 4]
        elif movement == 1:
            if y < configs['WIDTH'] - 1:
                maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 2]
                y += 1
                if hex_numbers.index(maze[x][y]) > 7:
                    maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 8]
        elif movement == 2:
            if x < configs['HEIGHT'] - 1:
                maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 4]
                x += 1
                if hex_numbers.index(maze[x][y]) % 2 != 0:
                    maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 1]
        elif movement == 3:
            if y > 0:
                maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 8]
                y -= 1
                if (2 <= hex_numbers.index(maze[x][y]) <= 3
                    or 6 <= hex_numbers.index(maze[x][y]) <= 7
                    or 10 <= hex_numbers.index(maze[x][y]) <= 11
                    or 14 <= hex_numbers.index(maze[x][y]) <= 15):
                    maze[x][y] = hex_numbers[hex_numbers.index(maze[x][y]) - 2]


def maze_gen(configs: dict, maze_file: str) -> None:
    maze = []
    for h in range(configs['HEIGHT']):
        new_list = []
        for w in range(configs['WIDTH']):
            new_list.append('F')
        maze.append(new_list)
    with open(maze_file, 'w') as maze_open:
        create_path(configs, maze)
        for l in maze:
            for c in l:
                maze_open.write(c)
            maze_open.write('\n')
    for m in maze:
        print(m)
