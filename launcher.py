#! /usr/bin/python3
import curses
from typing import Any
from maze_gen.ourtypes import Dir
from solver import a_star, path_to_moves
from ui.symbol import Symbol
from ui.beautify import beautify_junctions
from ui.cinematique_launch import title_screen
from ui.game import game_screen
from ui.menu import menu_screen
from ui.option import option_screen
from maze_gen.generator import parse_config_file, write_config_file, maze_gen


def normalize_points(settings: dict) -> None:
    w = settings["WIDTH"]
    h = settings["HEIGHT"]

    def clamp(p: tuple[int, int]) -> tuple[int, int]:
        x, y = p
        x = max(0, min(w - 1, x))
        y = max(0, min(h - 1, y))
        return (x, y)

    settings["ENTRY"] = clamp(settings["ENTRY"])
    settings["EXIT"] = clamp(settings["EXIT"])

    if settings["ENTRY"] == settings["EXIT"]:
        ex, ey = settings["ENTRY"]
        candidates = [(ex + 1, ey), (ex, ey + 1), (ex - 1, ey), (ex, ey - 1)]
        for cx, cy in candidates:
            if 0 <= cx < w and 0 <= cy < h:
                settings["EXIT"] = (cx, cy)
                break


def add_info_maze(moves: str) -> None:
    def my_trim(s: str) -> str:
        return s[1:-1]
    conf = parse_config_file("config.txt")
    entry = str(conf.get("ENTRY"))
    entry = my_trim(entry)
    entry_x, entry_y = entry.split(" ")
    exit = str(conf.get("EXIT"))
    exit = my_trim(exit)
    exit_x, exit_y = exit.split(" ")
    with open("maze.txt", "a") as file:
        file.write("\n")
        file.write(f"{entry_x}{entry_y}\n")
        file.write(f"{exit_x}{exit_y}\n")
        file.write(f"{moves}")


def read_maze_bits(path: Any = "maze.txt") -> list[list[int]]:

    grid: list[list[int]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line == "\n":
                break
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
            raise ValueError(f"maze.txt: ligne {y} de longueur \
{len(row)} au lieu de {length}")

    return grid


def show_maze_walls(
    fichier: str = "maze.txt",
    symb_type: str = "C",
    beautify: bool = False,
    show_closed: bool = False,
) -> tuple[list[str], str, list[tuple[int, int]], set[tuple[int, int]]]:
    conf_file = parse_config_file("config.txt")
    if not conf_file:
        raise ValueError("config.txt invalide ou illisible")
    if fichier is None:
        fichier = conf_file.get("OUTPUT_FILE", "maze.txt")

    symbol = Symbol(symb_type, 1)

    ex, ey = conf_file["ENTRY"]
    sx, sy = conf_file["EXIT"]

    grid = read_maze_bits(fichier)

    height = len(grid)
    width = len(grid[0])
    closed_cells: set[tuple[int, int]] = set()
    if show_closed:
        for y in range(height):
            for x in range(width):
                if grid[y][x] == 0xF:  # totalement fermée (N+E+S+W)
                    closed_cells.add((2 * y + 1, 2 * x + 1))

    if not (0 <= ex < width and 0 <= ey < height):
        raise ValueError(f"ENTRY hors labyrinthe: \
({ex},{ey}) pour width={width}, height={height}")
    if not (0 <= sx < width and 0 <= sy < height):
        raise ValueError(f"EXIT hors labyrinthe: \
({sx},{sy}) pour width={width}, height={height}")

    out = [[" " for _ in range(2 * width + 1)] for _ in range(2 * height + 1)]

    for yy in range(0, 2 * height + 1, 2):
        for xx in range(0, 2 * width + 1, 2):
            out[yy][xx] = symbol.DOT

    for y in range(height):
        for x in range(width):
            cell = grid[y][x]
            out[2 * y + 1][2 * x + 1] = symbol.FILL

            out[2 * y][2 * x + 1] = (
                symbol.H_WALL if (cell & Dir.N) else symbol.FILL
                )
            out[2 * y + 2][2 * x + 1] = (
                symbol.H_WALL if (cell & Dir.S) else symbol.FILL
                )
            out[2 * y + 1][2 * x] = (
                symbol.V_WALL if (cell & Dir.W) else symbol.FILL
                )
            out[2 * y + 1][2 * x + 2] = (
                symbol.V_WALL if (cell & Dir.E) else symbol.FILL
                )

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
    with open("maze.txt", "r") as file:
        if moves not in file:
            add_info_maze(moves)

    if beautify:
        beautify_junctions(out, symb_type)

    maze_lines = ["".join(row) for row in out]
    return (maze_lines, moves, path, closed_cells)


def launcher() -> None:
    def _run(stdscr: Any) -> None:
        title_screen(stdscr, duration=3.0, fps=30)

        conf = parse_config_file("init_config.txt")
        settings = {
            "WIDTH": int(conf["WIDTH"]),
            "HEIGHT": int(conf["HEIGHT"]),
            "SYMBOL_THEME": "A",
            "BEAUTIFY": False,
            "PATH_COLOR": "Rouge",
            "ENTRY_COLOR": "Rouge",
            "EXIT_COLOR": "Vert",
            "WALL_COLOR": "Blanc",
            "ENTRY": conf["ENTRY"],
            "EXIT": conf["EXIT"],
            "OUTPUT_FILE": conf.get("OUTPUT_FILE", "maze.txt"),
            "PERFECT": conf.get("PERFECT", True),
        }

        def regenerate() -> None:
            normalize_points(settings)
            stdscr.erase()
            stdscr.addstr(
                2, 2, "Generating maze... please wait", curses.A_BOLD
                )
            stdscr.refresh()
            new_conf = {
                "WIDTH": settings["WIDTH"],
                "HEIGHT": settings["HEIGHT"],
                "ENTRY": settings["ENTRY"],
                "EXIT": settings["EXIT"],
                "OUTPUT_FILE": settings["OUTPUT_FILE"],
                "PERFECT": settings["PERFECT"],
            }

            write_config_file(new_conf, "config.txt")
            conf2 = parse_config_file("config.txt")
            if not conf2:
                raise ValueError("Config invalide après \
écriture (regenerate).")
            maze_gen(conf2, conf2.get("OUTPUT_FILE", "maze.txt"))

        # 1) nouveau maze au lancement (obligatoire)
        while True:
            action = menu_screen(stdscr, title="A-MAZE-ING")
            if action == "quit":
                with open("init_config.txt", "r") as init_file:
                    content = init_file.read()
                    with open("config.txt", "w") as file:
                        for line in content:
                            file.write(f"{line}")
                return

            if action == "options":
                option_screen(stdscr, settings)
                normalize_points(settings)
                # si tu veux que changer WIDTH/HEIGHT regen direct:
                regenerate()
                continue

            if action == "start":
                regenerate()
                def render() -> tuple[list[str], str,
                                      list[tuple[int, int]],
                                      set[tuple[int, int]]]:
                    return show_maze_walls(
                        fichier=settings["OUTPUT_FILE"],
                        symb_type=settings["SYMBOL_THEME"],
                        beautify=settings["BEAUTIFY"],
                        show_closed=settings.get("COLOR_42", False),
                    )

                game_screen(
                    stdscr,
                    render_fn=render,
                    on_regenerate=regenerate,  # 2) regen dans le jeu sur "R"
                    path_color_name=settings["PATH_COLOR"],
                    entry_color_name=settings["ENTRY_COLOR"],
                    exit_color_name=settings["EXIT_COLOR"],
                    wall_color_name=settings["WALL_COLOR"],
                    title="A-MAZE-ING",
                )
                continue

    curses.wrapper(_run)


if __name__ == "__main__":
    launcher()
