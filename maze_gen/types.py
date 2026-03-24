from enum import IntEnum


class Dir(IntEnum):
    N = 1
    E = 2
    S = 4
    W = 8


ALL_DIRS = (Dir.N, Dir.E, Dir.S, Dir.W)


DIR_VECT = {
    Dir.N: (0, -1),
    Dir.E: (1, 0),
    Dir.S: (0, 1),
    Dir.W: (-1, 0)
}


OPPOSITE = {
    Dir.N: Dir.S,
    Dir.E: Dir.W,
    Dir.S: Dir.N,
    Dir.W: Dir.E
}
