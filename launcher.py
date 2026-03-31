#! /usr/bin/python3
"""Lanceur principal (curses) et rendu du labyrinthe.

Ce module orchestre :
- l'écran titre, le menu et les options ;
- la génération d'un nouveau labyrinthe ;
- le rendu ASCII/Unicode des murs à partir de la grille hexadécimale ;
- le calcul du chemin solution (A*) et son affichage.
"""
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
    """Normalise les coordonnées ENTRY/EXIT dans les limites du labyrinthe.

    Les points sont "clampés" dans [0, WIDTH-1] et [0, HEIGHT-1]. Si ENTRY et
    EXIT deviennent identiques, EXIT est déplacé vers une case adjacente si
    possible.

    Parameters
    ----------
    settings : dict
        Dictionnaire de paramètres (doit contenir WIDTH, HEIGHT, ENTRY, EXIT).

    Returns
    -------
    None
    """
    w = settings["WIDTH"]
    h = settings["HEIGHT"]

    def clamp(p: tuple[int, int]) -> tuple[int, int]:
        """Force un point (x, y) à rester dans les bornes du labyrinthe.

        Parameters
        ----------
        p : tuple[int, int]
            Coordonnées (x, y) à borner.

        Returns
        -------
        tuple[int, int]
            Coordonnées bornées.
        """
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
    """Ajoute des informations (ENTRY/EXIT/mouvements) à la fin de maze.txt.

    Parameters
    ----------
    moves : str
        Suite de mouvements cardinaux (N, S, E, W).

    Returns
    -------
    None
    """
    def my_trim(s: str) -> str:
        """Supprime le premier et le dernier caractère d'une chaîne.

        Parameters
        ----------
        s : str
            Chaîne à tronquer.

        Returns
        -------
        str
            Chaîne sans son premier et son dernier caractère.
        """
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
    """Lit un labyrinthe encodé en hexadécimal et retourne une grille de bits.

    Le fichier est lu ligne par ligne jusqu'à une ligne vide. Chaque caractère
    hexadécimal est converti en entier (base 16) et représente un masque de
    murs pour une cellule.

    Parameters
    ----------
    path : Any, default="maze.txt"
        Chemin du fichier (le code accepte un chemin "str-like").

    Returns
    -------
    list[list[int]]
        Grille (hauteur x largeur) d'entiers.

    Raises
    ------
    ValueError
        Si le fichier ne contient aucune ligne de grille ou si les lignes
        n'ont pas toutes la même longueur.
    """
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
    """Construit un rendu du labyrinthe et calcule le chemin solution.

    Cette fonction :
    - lit la configuration (ENTRY/EXIT, options) ;
    - lit le labyrinthe encodé en bits depuis un fichier ;
    - produit une matrice de caractères (murs/espaces) ;
    - calcule un chemin avec A* et une chaîne de mouvements ;
    - optionnellement embellit les jonctions.

    Parameters
    ----------
    fichier : str, default="maze.txt"
        Fichier contenant la grille hexadécimale.
    symb_type : str, default="C"
        Thème de symboles (A, B, C).
    beautify : bool, default=False
        Si True, remplace les points de jonction par des coins/croix.
    show_closed : bool, default=False
        Si True, marque les cellules totalement fermées.

    Returns
    -------
    tuple[list[str], str, list[tuple[int, int]], set[tuple[int, int]]]
        (lignes du rendu, mouvements, chemin (cellules), cellules fermées).

    Raises
    ------
    ValueError
        Si la configuration est invalide, si ENTRY/EXIT sont hors limites,
        si le fichier est vide, ou si aucun chemin n'existe.
    """
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
    """Point d'entrée du lanceur curses.

    Démarre l'interface curses via :func:`curses.wrapper` et orchestre le flux
    suivant : écran titre -> menu -> options -> génération -> jeu.

    Returns
    -------
    None
    """
    def _run(stdscr: Any) -> None:
        """Boucle principale curses (appelée par curses.wrapper).

        Parameters
        ----------
        stdscr : Any
            Fenêtre principale curses.

        Returns
        -------
        None
        """
        title_screen(stdscr, duration=3.0, fps=30)

        conf = parse_config_file("config.txt")
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
            """Génère un nouveau labyrinthe à partir des paramètres courants.

            Met à jour config.txt, recharge la configuration, puis écrit un
            nouveau fichier de labyrinthe.

            Returns
            -------
            None

            Raises
            ------
            ValueError
                Si la configuration devient invalide après écriture.
            """
            normalize_points(settings)
            stdscr.erase()
            stdscr.addstr(
                2, 2, "Generating maze... please wait", curses.A_BOLD
                )
            stdscr.refresh()
            if "SEED" in conf.keys():
                new_conf = {
                    "WIDTH": settings["WIDTH"],
                    "HEIGHT": settings["HEIGHT"],
                    "ENTRY": settings["ENTRY"],
                    "EXIT": settings["EXIT"],
                    "OUTPUT_FILE": settings["OUTPUT_FILE"],
                    "PERFECT": settings["PERFECT"],
                    "SEED": conf['SEED']
                }
            else:
                new_conf = {
                    "WIDTH": settings["WIDTH"],
                    "HEIGHT": settings["HEIGHT"],
                    "ENTRY": settings["ENTRY"],
                    "EXIT": settings["EXIT"],
                    "OUTPUT_FILE": settings["OUTPUT_FILE"],
                    "PERFECT": settings["PERFECT"]
                }

            write_config_file(new_conf, "config.txt")
            conf2 = parse_config_file("config.txt")
            if not conf2:
                raise ValueError("Config invalide après \
écriture (regenerate).")
            maze_gen(conf2, conf2.get("OUTPUT_FILE", "maze.txt"))

        while True:
            action = menu_screen(stdscr, title="A-MAZE-ING")
            if action == "quit":
                return

            if action == "options":
                option_screen(stdscr, settings)
                normalize_points(settings)
                regenerate()
                continue

            if action == "start":
                regenerate()

                def render() -> tuple[list[str], str,
                                      list[tuple[int, int]],
                                      set[tuple[int, int]]]:
                    """Construit le rendu du labyrinthe à afficher dans le jeu.

                    Returns
                    -------
                    tuple[list[str], str, list[tuple[int, int]],
                    set[tuple[int, int]]]
                        Même format que :func:`show_maze_walls`.
                    """
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
