#! /usr/bin/python3
import curses
from maze_gen.ourtypes import Dir
from maze_gen.generator import parse_config_file
from solver import a_star, path_to_moves, draw_path_on_out
from symbol import Symbol
symbol = Symbol("C")

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
            # Ton message personnalisé
            raise ValueError(f"maze.txt: ligne {y} de longueur {len(row)} au lieu de {length}")

    return grid


def afficher_labyrinthe_murs(fichier="maze.txt") -> list[str]:
    conf_file = parse_config_file()
    if fichier is None:
        fichier = conf_file.get("OUTPUT_FILE", "maze.txt")

    # ENTRY / EXIT attendus en coordonnées "cellules" : x,y sur grid
    ex, ey = map(int, conf_file.get("ENTRY").split(","))
    sx, sy = map(int, conf_file.get("EXIT").split(","))

    try:
        grid = lire_maze_bits(fichier)
    except ValueError as e:
        print(e)
        return

    height = len(grid)        # nb de lignes (Y)
    width = len(grid[0])      # nb de colonnes (X)

    # Validation des bornes
    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError(f"ENTRY hors labyrinthe: ({ex},{ey}) pour width={width}, height={height}")
    if not (0 <= sx < width and 0 <= sy < height):
        raise ValueError(f"EXIT hors labyrinthe: ({sx},{sy}) pour width={width}, height={height}")

    out = [[" " for _ in range(2 * width + 1)] for _ in range(2 * height + 1)]

    # intersections
    for yy in range(0, 2 * height + 1, 2):
        for xx in range(0, 2 * width + 1, 2):
            out[yy][xx] = symbol.DOT

    # murs
    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            out[2 * y + 1][2 * x + 1] = symbol.FILL

            out[2 * y][2 * x + 1]     = symbol.H_WALL if (cell & Dir.N) else symbol.FILL
            out[2 * y + 2][2 * x + 1] = symbol.H_WALL if (cell & Dir.S) else symbol.FILL
            out[2 * y + 1][2 * x]     = symbol.V_WALL if (cell & Dir.W) else symbol.FILL
            out[2 * y + 1][2 * x + 2] = symbol.V_WALL if (cell & Dir.E) else symbol.FILL

    # Placement direct sur l'affichage (centre de cellule)
    entry_r, entry_c = 2 * ey + 1, 2 * ex + 1
    exit_r, exit_c = 2 * sy + 1, 2 * sx + 1
    out[entry_r][entry_c] = symbol.ENTRY
    out[exit_r][exit_c] = symbol.EXIT

    start = (ex, ey)
    goal = (sx, sy)
    path = a_star(grid, start, goal)
    if path is None:
        raise ValueError("Aucun chemin trouve entre ENTRY et EXIT")
    moves = path_to_moves(path)
    draw_path_on_out(out, path, symbol.PATH)

    return (["".join(row) for row in out], moves)


def launcher() -> None:
    maze_lines, moves = afficher_labyrinthe_murs()
    for line in maze_lines:
        print(line)
    print(moves)


if __name__ == "__main__":
    launcher()
