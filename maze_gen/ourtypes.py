"""Types et constantes pour manipuler les directions et murs du labyrinthe.

Les directions sont encodées via :class:`Dir` (bits). Ces constantes sont
utilisées pour interpréter les masques de murs et naviguer sur la grille.
"""
from enum import IntEnum


class Dir(IntEnum):
    """Directions cardinales encodées sous forme de bits (IntEnum)."""
    N = 1
    E = 2
    S = 4
    W = 8

# Tuple des directions dans l'ordre N, E, S, W.
ALL_DIRS = (Dir.N, Dir.E, Dir.S, Dir.W)

# Vecteurs (dx, dy) associés à chaque direction.
DIR_VECT = {
    Dir.N: (0, -1),
    Dir.E: (1, 0),
    Dir.S: (0, 1),
    Dir.W: (-1, 0)
}

# Direction opposée pour chaque direction.
OPPOSITE = {
    Dir.N: Dir.S,
    Dir.E: Dir.W,
    Dir.S: Dir.N,
    Dir.W: Dir.E
}
