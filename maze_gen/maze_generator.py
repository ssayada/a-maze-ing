from time import sleep
from random import randint
from a_maze_ing import launcher


class Maze:
    '''
    ez
    '''
    maze: list
    hexa: list
    config: dict

    def __init__(self, config: dict) -> None:
        self.config = config
        self.maze = []
        for w in range(config['HEIGHT']):
            new_row = []
            for h in range(config['WIDTH']):
                new_row.append('F')
            self.maze.append(new_row)
        self.hexa = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']


    def get_maze(self) -> list:
        return self.maze


    def get_walls(self, x, y) -> str:
        return self.maze[y][x]


    def get_hexa(self) -> list:
        return self.hexa


    def get_entry(self) -> bool:
        return self.config['ENTRY']

    
    def get_exit(self) -> bool:
        return self.config['EXIT']


    def get_width(self) -> int:
        return self.config['WIDTH']


    def get_height(self) -> int:
        return self.config['HEIGHT']


    def is_visited(self, x, y) -> bool:
        if self.maze[y][x] != 'F':
            return True
        return False


    def adjacents_visited(self, x, y) -> bool:
        if y < self.config['HEIGHT'] - 1:
            if not self.is_visited(x, y + 1):
                return False
        if y > 0:
            if not self.is_visited(x, y - 1):
                return False
        if x < self.config['WIDTH'] - 1:
            if not self.is_visited(x + 1, y):
                return False
        if x > 0:
            if not self.is_visited(x - 1, y):
                return False
        return True


    def north_possible(self, x, y) -> bool:
        if y <= 0:
            return False
        if self.is_visited(x, y - 1):
            return False
        return True


    def break_north(self, x, y) -> None:
        print(y, x)
        self.maze[y][x] = self.hexa[self.hexa.index(self.maze[y][x]) - 1]


    def north_open(self, x, y) -> bool:
        if (self.hexa.index(self.maze[y][x]) % 2 == 0
            and y > 0):
            return True
        return False


    def east_possible(self, x, y) -> bool:
        if x >= self.config['WIDTH'] - 1:
            return False
        if self.is_visited(x + 1, y):
            return False
        return True


    def break_east(self, x, y) -> None:
        self.maze[y][x] = self.hexa[self.hexa.index(self.maze[y][x]) - 2]


    def east_open(self, x, y) -> bool:
        if ((0 <= self.hexa.index(self.maze[y][x]) <= 1
            or 4 <= self.hexa.index(self.maze[y][x]) <= 6
            or 8 <= self.hexa.index(self.maze[y][x]) <= 9
            or 12 <= self.hexa.index(self.maze[y][x]) <= 13)
            and x < self.config['WIDTH'] - 1):
            return True
        return False


    def south_possible(self, x, y) -> bool:
        if y >= self.config['HEIGHT'] - 1:
            return False
        if self.is_visited(x, y + 1):
            return False
        return True


    def break_south(self, x, y) -> None:
        self.maze[y][x] = self.hexa[self.hexa.index(self.maze[y][x]) - 4]


    def south_open(self, x, y) -> bool:
        if ((0 <= self.hexa.index(self.maze[y][x]) <= 3
            or 8 <= self.hexa.index(self.maze[y][x]) <= 11)
            and x < self.config['HEIGHT'] - 1):
            return True
        return False


    def west_possible(self, x, y) -> bool:
        if x <= 0:
            return False
        if self.is_visited(x - 1, y):
            return False
        return True


    def break_west(self, x, y) -> None:
        self.maze[y][x] = self.hexa[self.hexa.index(self.maze[y][x]) - 8]


    def west_open(self, x, y) -> bool:
        if (0 <= self.hexa.index(self.maze[y][x]) <= 7
            and x > 0):
            return True
        return False


    def move_back(self, x, y) -> None:
        while self.adjacents_visited(x, y):
            move = randint(0, 3)
            if move == 0 and self.north_open(x, y):
                y -= 1
            if move == 1 and self.east_open(x, y):
                x += 1
            if move == 2 and self.south_open(x, y):
                y += 1
            if move == 3 and self.west_open(x, y):
                x -= 1
            print(f"x: {x}, y: {y}")
            for m in self.get_maze():
                print(m)
            print()
            sleep(0.01)
        return x, y


def create_path(maze: Maze) -> None:
    x, y = maze.get_entry()
    x_ex, y_ex = maze.get_exit()
    #for i in range(100):
    while not (x == x_ex and y == y_ex):
        movement = randint(0, 3)
        if maze.adjacents_visited(x, y):
            x, y = maze.move_back(x, y)
        elif (movement == 0):
            if maze.north_possible(x, y):
                maze.break_north(x, y)
                y -= 1
                maze.break_south(x, y)
        elif (movement == 1):
            if maze.east_possible(x, y):
                maze.break_east(x, y)
                x += 1
                maze.break_west(x, y)
        elif (movement == 2):
            if maze.south_possible(x, y):
                maze.break_south(x, y)
                y += 1
                maze.break_north(x, y)
        elif (movement == 3):
            if maze.west_possible(x, y):
                maze.break_west(x, y)
                x -= 1
                maze.break_east(x, y)
    print(x, y)


def maze_gen(configs: dict, maze_file: str) -> None:
    '''
    ez
    '''
    try:
        maze = Maze(configs)
        create_path(maze)
    except KeyboardInterrupt:
        print("wait bro")
    finally:
        with open(maze_file, 'w') as maze_open:
            for l in maze.get_maze():
                for c in l:
                    maze_open.write(c)
                maze_open.write('\n')
