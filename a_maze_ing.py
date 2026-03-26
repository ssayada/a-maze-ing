#! /usr/bin/python3
import curses
from maze_gen.ourtypes import Dir
from maze_gen.generator import parse_config_file
from solver import a_star, path_to_moves
from ui.symbol import Symbol
from ui.beautify import beautify_junctions
from ui.cinematique_launch import title_screen
from ui.game import game_screen
from ui.menu import menu_screen
from ui.option import option_screen



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


def afficher_labyrinthe_murs(
    fichier: str = "maze.txt",
    symb_type: str = "C",
    beautify: bool = False,
) -> tuple[list[str], str, list[tuple[int,int]]]:
    conf_file = parse_config_file("config.txt")
    if fichier is None:
        fichier = conf_file.get("OUTPUT_FILE", "maze.txt")

    symbol = Symbol(symb_type, 1)

    ex, ey = map(int, conf_file.get("ENTRY"))
    sx, sy = map(int, conf_file.get("EXIT"))

    grid = lire_maze_bits(fichier)

    height = len(grid)
    width = len(grid[0])

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError(f"ENTRY hors labyrinthe: ({ex},{ey}) pour width={width}, height={height}")
    if not (0 <= sx < width and 0 <= sy < height):
        raise ValueError(f"EXIT hors labyrinthe: ({sx},{sy}) pour width={width}, height={height}")

    out = [[" " for _ in range(2 * width + 1)] for _ in range(2 * height + 1)]

    for yy in range(0, 2 * height + 1, 2):
        for xx in range(0, 2 * width + 1, 2):
            out[yy][xx] = symbol.DOT

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            out[2 * y + 1][2 * x + 1] = symbol.FILL

            out[2 * y][2 * x + 1]     = symbol.H_WALL if (cell & Dir.N) else symbol.FILL
            out[2 * y + 2][2 * x + 1] = symbol.H_WALL if (cell & Dir.S) else symbol.FILL
            out[2 * y + 1][2 * x]     = symbol.V_WALL if (cell & Dir.W) else symbol.FILL
            out[2 * y + 1][2 * x + 2] = symbol.V_WALL if (cell & Dir.E) else symbol.FILL

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
    """draw_path_on_out(out, path, symbol.PATH)"""

    if beautify:
        beautify_junctions(out, symb_type)

    maze_lines = ["".join(row) for row in out]
    return (maze_lines, moves, path)


def launcher() -> None:
    def _run(stdscr):
        title_screen(stdscr, duration=3.0, fps=30)

        # init settings depuis config.txt
        conf = parse_config_file("config.txt")
        settings = {
            "WIDTH": int(conf["WIDTH"]),
            "HEIGHT": int(conf["HEIGHT"]),
            "SYMBOL_THEME": "A",
            "BEAUTIFY": False,
            "PATH_COLOR": "Rouge",
        }

        """def regenerate() -> None:
            # 1) écrit config.txt
            write_config_file(settings, "config.txt")
            # 2) relit + valide
            conf2 = parse_config_file("config.txt")
            # 3) génère maze.txt
            maze_gen(conf2, conf2["OUTPUT_FILE"])

        regenerate()"""

        while True:
            action = menu_screen(stdscr, title="A-MAZE-ING")
            if action == "quit":
                return

            if action == "options":
                option_screen(stdscr, settings)
                """regenerate()"""
                continue

            if action == "start":
                def render():
                    return afficher_labyrinthe_murs(
                        fichier="maze.txt",
                        symb_type=settings["SYMBOL_THEME"],
                        beautify=settings["BEAUTIFY"],
                    )

                game_screen(
                    stdscr,
                    render_fn=render,
                    on_regenerate=None,  # touche R dans game_screen
                    path_color_name=settings["PATH_COLOR"],
                    title="A-MAZE-ING",
                )
                # retour game_screen -> menu
                continue

    curses.wrapper(_run)


if __name__ == "__main__":
    launcher()
