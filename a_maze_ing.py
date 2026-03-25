#! /usr/bin/python3
import curses
from maze_gen.ourtypes import Dir

H_WALL = "━"
V_WALL = "┃"
FILL = " "
DOT = "╋"  # intersection (simple)


def lire_maze_bits(path="maze.txt") -> list[list[int]]:
    grid: list[list[int]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid.append([int(ch, 16) for ch in line])

    if not grid:
        raise ValueError("maze.txt est vide")

    # Vérifie que toutes les lignes ont la même longueur
    length = len(grid[0])
    for y, row in enumerate(grid):
        if len(row) != length:
            raise ValueError(f"maze.txt: ligne {y} de longueur {len(row)} au lieu de {length}")

    return grid


def afficher_labyrinthe_murs(fichier="maze.txt") -> None:
    grid = lire_maze_bits(fichier)
    width = len(grid)        # nb de lignes (Y)
    length = len(grid[0])    # nb de colonnes (X)

    out = [[FILL for _ in range(2 * length + 1)] for _ in range(2 * width + 1)]

    # intersections (optionnel)
    for yy in range(0, 2 * width + 1, 2):
        for xx in range(0, 2 * length + 1, 2):
            out[yy][xx] = DOT

    for y in range(width):
        for x in range(length):
            cell = grid[y][x]

            # intérieur de la cellule
            out[2 * y + 1][2 * x + 1] = FILL

            # murs selon bits
            out[2 * y][2 * x + 1] = H_WALL if (cell & Dir.N) else FILL        # haut
            out[2 * y + 2][2 * x + 1] = H_WALL if (cell & Dir.S) else FILL    # bas
            out[2 * y + 1][2 * x] = V_WALL if (cell & Dir.W) else FILL        # gauche
            out[2 * y + 1][2 * x + 2] = V_WALL if (cell & Dir.E) else FILL    # droite

    print("\n".join("".join(row) for row in out))


def launcher() -> None:
    afficher_labyrinthe_murs()


if __name__ == "__main__":
    launcher()
