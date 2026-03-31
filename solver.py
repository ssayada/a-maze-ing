"""Résolution de labyrinthe avec l'algorithme A*.

Le labyrinthe est représenté par une grille d'entiers où chaque cellule encode
ses murs via des bits (voir :class:`maze_gen.ourtypes.Dir`). Un bit présent
indique un mur dans la direction correspondante.

Ce module fournit :
- une heuristique Manhattan ;
- une extraction de voisins accessibles ;
- une recherche A* ;
- des fonctions utilitaires de conversion et d'annotation du rendu.
"""
import heapq
from typing import Optional
from maze_gen.ourtypes import Dir

Cell = tuple[int, int]


def manhattan(a: Cell, b: Cell) -> int:
    """Calcule la distance de Manhattan entre deux cellules.

    Parameters
    ----------
    a : Cell
        Coordonnées (x, y) de la première cellule.
    b : Cell
        Coordonnées (x, y) de la seconde cellule.

    Returns
    -------
    int
        Distance de Manhattan ``|dx| + |dy|``.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors_from_bits(grid: list[list[int]], x: int, y: int) -> list[Cell]:
    """Liste les voisins accessibles depuis une cellule.

    Une direction est praticable si le mur correspondant n'est pas présent
    dans le masque de bits de la cellule courante.

    Parameters
    ----------
    grid : list[list[int]]
        Grille des cellules (masques de murs).
    x : int
        Colonne de la cellule courante.
    y : int
        Ligne de la cellule courante.

    Returns
    -------
    list[Cell]
        Liste des cellules voisines accessibles.
    """
    h = len(grid)
    w = len(grid[0])
    cell = grid[y][x]
    out: list[Cell] = []

    if y > 0 and not (cell & Dir.N):
        out.append((x, y - 1))
    if x < w - 1 and not (cell & Dir.E):
        out.append((x + 1, y))
    if y < h - 1 and not (cell & Dir.S):
        out.append((x, y + 1))
    if x > 0 and not (cell & Dir.W):
        out.append((x - 1, y))

    return out


def reconstruct_path(came_from: dict[Cell, Cell], cur: Cell) -> list[Cell]:
    """Reconstruit un chemin à partir de la table des prédécesseurs.

    Parameters
    ----------
    came_from : dict[Cell, Cell]
        Dictionnaire associant une cellule à sa cellule précédente.
    cur : Cell
        Cellule d'arrivée.

    Returns
    -------
    list[Cell]
        Chemin de `start` à `cur` (inclus).
    """
    path = [cur]
    while cur in came_from:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    return path


# Algo A-star
def a_star(
        grid: list[list[int]], start: Cell, goal: Cell
        ) -> Optional[list[Cell]]:
    """Trouve un chemin entre deux cellules avec l'algorithme A*.

    Parameters
    ----------
    grid : list[list[int]]
        Grille des cellules (masques de murs).
    start : Cell
        Cellule de départ (x, y).
    goal : Cell
        Cellule d'arrivée (x, y).

    Returns
    -------
    list[Cell] | None
        Le chemin sous forme de liste de cellules si trouvé, sinon ``None``.
    """
    open_heap: list[tuple[int, int, Cell]] = []
    heapq.heappush(open_heap, (manhattan(start, goal), 0, start))

    came_from: dict[Cell, Cell] = {}
    g_score: dict[Cell, int] = {start: 0}
    closed: set[Cell] = set()

    while open_heap:
        f, g, cur = heapq.heappop(open_heap)
        if cur in closed:
            continue
        closed.add(cur)

        if cur == goal:
            return reconstruct_path(came_from, cur)

        cx, cy = cur
        for nb in neighbors_from_bits(grid, cx, cy):
            tentative_g = g + 1
            if tentative_g < g_score.get(nb, 10**18):
                came_from[nb] = cur
                g_score[nb] = tentative_g
                heapq.heappush(
                    open_heap, (tentative_g + manhattan(nb, goal),
                                tentative_g, nb))

    return None


def path_to_moves(path: list[Cell]) -> str:
    """Convertit un chemin en déplacements cardinaux (N, S, E, W).

    Parameters
    ----------
    path : list[Cell]
        Chemin sous forme de cellules successives.

    Returns
    -------
    str
        Chaîne de déplacements composée de ``N``, ``S``, ``E`` et ``W``.

    Raises
    ------
    ValueError
        Si deux cellules consécutives ne sont pas voisines en 4 directions.
    """
    moves: list[str] = []
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        dx, dy = x1 - x0, y1 - y0
        if dx == 0 and dy == -1:
            moves.append("N")
        elif dx == 0 and dy == 1:
            moves.append("S")
        elif dx == 1 and dy == 0:
            moves.append("E")
        elif dx == -1 and dy == 0:
            moves.append("W")
        else:
            raise ValueError(f"Pas un déplacement 4-directionnel: \
{(x0, y0)} -> {(x1, y1)}")
    return "".join(moves)


def draw_path_on_out(
        out: list[list[str]], path: list[Cell],
        symbol: str = "%") -> None:
    """Marque un chemin dans une matrice de rendu.

    Parameters
    ----------
    out : list[list[str]]
        Matrice de caractères représentant le labyrinthe rendu.
    path : list[Cell]
        Chemin sous forme de cellules (x, y).
    symbol : str, default="%"
        Symbole utilisé pour marquer le chemin.

    Notes
    -----
    Les cellules d'entrée ``#`` et de sortie ``$`` ne sont pas écrasées.
    """
    for x, y in path:
        r, c = 2 * y + 1, 2 * x + 1
        if out[r][c] not in ("#", "$"):
            out[r][c] = symbol
