import heapq
from typing import Optional
from maze_gen.ourtypes import Dir

Cell = tuple[int, int]


def manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# permet de check si bit == 0 pour passer
def neighbors_from_bits(grid: list[list[int]], x: int, y: int) -> list[Cell]:
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
    path = [cur]
    while cur in came_from:
        cur = came_from[cur]
        path.append(cur)
    path.reverse()
    return path


# Algo A-star
def a_star(grid: list[list[int]], start: Cell, goal: Cell) -> Optional[list[Cell]]:
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
                heapq.heappush(open_heap, (tentative_g + manhattan(nb, goal), tentative_g, nb))

    return None


# sert a convertir le chemin de la win en NSWE
def path_to_moves(path: list[Cell]) -> str:
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
            raise ValueError(f"Pas un déplacement 4-directionnel: {(x0,y0)} -> {(x1,y1)}")
    return "".join(moves)

# permet de marquer le chemin dans l'affichage
def draw_path_on_out(out: list[list[str]], path: list[Cell], symbol: str = "%") -> None:
    for x, y in path:
        r, c = 2 * y + 1, 2 * x + 1
        if out[r][c] not in ("#", "$"):
            out[r][c] = symbol
