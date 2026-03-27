from time import sleep
from random import randint


class Maze:
    '''
    ez
    '''
    maze: list
    hexa: list
    config: dict
    backtrack: list

    def __init__(self, config: dict) -> None:
        self.config = config
        self.maze = []
        for w in range(config['HEIGHT']):
            new_row = []
            for h in range(config['WIDTH']):
                new_row.append('F')
            self.maze.append(new_row)
        self.hexa = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
        self.backtrack = []


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
    

    def is_forty_two(self, x, y) -> bool:
        if self.maze[y][x] not in self.hexa:
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
        if self.is_forty_two(x, y - 1):
            return False
        return True


    def break_north(self, x, y) -> None:
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
        if self.is_forty_two(x + 1, y):
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
        if self.is_forty_two(x, y + 1):
            return False
        return True


    def break_south(self, x, y) -> None:
        self.maze[y][x] = self.hexa[self.hexa.index(self.maze[y][x]) - 4]


    def south_open(self, x, y) -> bool:
        if ((0 <= self.hexa.index(self.maze[y][x]) <= 3
            or 8 <= self.hexa.index(self.maze[y][x]) <= 11)
            and y < self.config['HEIGHT'] - 1):
            return True
        return False


    def west_possible(self, x, y) -> bool:
        if x <= 0:
            return False
        if self.is_visited(x - 1, y):
            return False
        if self.is_forty_two(x - 1, y):
            return False
        return True


    def break_west(self, x, y) -> None:
        self.maze[y][x] = self.hexa[self.hexa.index(self.maze[y][x]) - 8]


    def west_open(self, x, y) -> bool:
        if (0 <= self.hexa.index(self.maze[y][x]) <= 7
            and x > 0):
            return True
        return False


    def move_back(self, x, y) -> tuple:
        while self.adjacents_visited(x, y):
            direction = self.backtrack.pop()
            if direction == 'N':
                y += 1
            if direction == 'E':
                x -= 1
            if direction == 'S':
                y -= 1
            if direction == 'W':
                x += 1
        return x, y


    def create_path(self) -> None:
        x, y = self.get_entry()
        x_ex, y_ex = self.get_exit()
        while not (x == x_ex and y == y_ex):
            movement = randint(0, 3)
            if self.adjacents_visited(x, y):
                x, y = self.move_back(x, y)
            elif (movement == 0):
                if self.north_possible(x, y) and not self.is_forty_two(x, y - 1):
                    self.break_north(x, y)
                    y -= 1
                    self.break_south(x, y)
                    self.backtrack.append('N')
            elif (movement == 1):
                if self.east_possible(x, y) and not self.is_forty_two(x + 1, y):
                    self.break_east(x, y)
                    x += 1
                    self.break_west(x, y)
                    self.backtrack.append('E')
            elif (movement == 2):
                if self.south_possible(x, y) and not self.is_forty_two(x, y + 1):
                    self.break_south(x, y)
                    y += 1
                    self.break_north(x, y)
                    self.backtrack.append('S')
            elif (movement == 3):
                if self.west_possible(x, y) and not self.is_forty_two(x - 1, y):
                    self.break_west(x, y)
                    x -= 1
                    self.break_east(x, y)
                    self.backtrack.append('W')


    def is_complete(self) -> bool:
        for m in self.maze:
            for c in m:
                if c == 'F':
                    return False
        return True


    def open_path_perfect(self, x, y) -> None:
        while True:
            move = randint(0, 3)
            if move == 0:
                if y > 0:
                    if not self.is_forty_two(x, y - 1) and self.is_visited(x, y - 1):
                        self.break_north(x, y)
                        self.break_south(x, y - 1)
                        return
            elif move == 1:
                if x < self.config['WIDTH'] - 1:
                    if (not self.is_forty_two(x + 1, y) and self.is_visited(x + 1, y)
                        and not self.is_forty_two(x + 1, y)):
                        self.break_east(x, y)
                        self.break_west(x + 1, y)
                        return
            elif move == 2:
                if y < self.config['HEIGHT'] - 1:
                    if (not self.is_forty_two(x, y + 1) and self.is_visited(x, y + 1)
                        and not self.is_forty_two(x, y + 1)):
                        self.break_south(x, y)
                        self.break_north(x, y + 1)
                        return
            elif move == 3:
                if x > 0:
                    if (not self.is_forty_two(x - 1, y) and self.is_visited(x - 1, y)
                        and not self.is_forty_two(x - 1, y)):
                        self.break_west(x, y)
                        self.break_east(x - 1, y)
                        return


    def connect_cases(self, x: int, y: int, dir: int) -> None:
        if dir == 0:
            if y > 0:
                if self.maze[y - 1][x] != 'F':
                    self.break_north(x, y)
                    self.break_south(x, y - 1)
        if dir == 1:
            if x < self.config['WIDTH'] - 1:
                if self.maze[y][x + 1] != 'F':
                    self.break_east(x, y)
                    self.break_west(x + 1, y)
        if dir == 2:
            if y < self.config['HEIGHT'] - 1:
                if self.maze[y + 1][x] != 'F':
                    self.break_south(x, y)
                    self.break_north(x, y + 1)
        if dir == 3:
            if x > 0:
                if self.maze[y][x - 1] != 'F':
                    self.break_west(x, y)
                    self.break_east(x - 1, y)


    def complete_maze(self, perfect: bool) -> None:
        if self.maze[0][0] == 'F':
            move = randint(1, 2)
            if move == 1:
                self.break_east(0, 0)
                self.break_west(1, 0)
            else:
                self.break_south(0, 0)
                self.break_north(0, 1)
        for y in range(0, len(self.maze)):
            for x in range(0, len(self.maze[y])):
                if not self.is_visited(x, y):
                    self.open_path_perfect(x, y)
    

    def forty_two_possible(self) -> bool:
        if self.config['WIDTH'] > 9 and self.config['HEIGHT'] > 7:
            return True
        return False
    

    def get_forty_two(self) -> tuple:
        return int((self.config['WIDTH'] / 2) - 3), int((self.config['HEIGHT'] / 2) - 2)


    def create_forty_two(self, left_top_42: tuple) -> None:
        x, y = left_top_42
        base_x = x
        forty_two = [
            ['G', 'F', 'F', 'F', 'G', 'G', 'G', 'F'],
            ['G', 'F', 'F', 'D', '5', 'B', 'G', 'F'],
            ['G', 'G', 'G', 'F', 'G', 'G', 'G', 'F'],
            ['F', 'F', 'G', 'F', 'G', 'D', '5', '7'],
            ['F', 'F', 'G', 'F', 'G', 'G', 'G', 'F']
        ]
        for l in forty_two:
            for c in l:
                self.maze[y][x] = c
                x += 1
            y += 1
            x = base_x
    

    def draw_forty_two(self) -> None:
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if (self.maze[y - 1][x] == 'G'
                    and self.maze[y + 1][x] == 'G'
                    and self.maze[y][x - 1] != 'G'
                    and self.maze[y][x + 1] != 'G'
                    and self.maze[y][x + 2] != 'G'
                    and self.maze[y][x] != 'G'):
                    self.break_east(x - 1, y)
                if (self.maze[y - 1][x] == 'G'
                    and self.maze[y + 1][x] == 'G'
                    and self.maze[y][x - 1] != 'G'
                    and self.maze[y][x + 1] != 'G'
                    and self.maze[y][x - 2] != 'G'
                    and self.maze[y][x] != 'G'):
                    self.break_west(x + 1, y)
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if self.maze[y][x] == 'G':
                    self.maze[y][x] = 'F'


def maze_gen(configs: dict, maze_file: str) -> None:
    '''
    ez
    '''
    maze = Maze(configs)
    if maze.forty_two_possible():
        maze.create_forty_two(maze.get_forty_two())
    maze.create_path()
    if configs['PERFECT'] == True:
        maze.complete_maze(1)
    if configs['PERFECT'] == False:
        maze.complete_maze(0)
    maze.draw_forty_two()
    with open(maze_file, 'w') as maze_open:
        for l in maze.get_maze():
            for c in l:
                maze_open.write(c)
            maze_open.write('\n')
