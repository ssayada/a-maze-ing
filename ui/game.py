import curses
from collections.abc import Callable
from typing import Optional
from ui.colors import Colors

# render_fn returns: (maze_lines, moves, path)
RenderFn = (Callable[[],
            tuple[list[str],
            str, list[tuple[int, int]], set[tuple[int, int]]]])
RegenerateFn = Callable[[], None]


def _path_to_out_positions(
        path: list[tuple[int, int]]) -> set[tuple[int, int]]:
    pos: set[tuple[int, int]] = set()
    if not path:
        return pos

    # centre de la 1ère cellule
    x0, y0 = path[0]
    r0, c0 = 2 * y0 + 1, 2 * x0 + 1
    pos.add((r0, c0))

    for (x1, y1) in path[1:]:
        r1, c1 = 2 * y1 + 1, 2 * x1 + 1

        # ajoute le segment entre (r0,c0) et (r1,c1) : il est à mi-chemin
        rm, cm = (r0 + r1) // 2, (c0 + c1) // 2
        pos.add((rm, cm))

        # ajoute le centre de la cellule suivante
        pos.add((r1, c1))

        r0, c0 = r1, c1

    return pos


def _safe_addch(stdscr, y: int, x: int, ch: str, attr: int = 0) -> bool:
    try:
        stdscr.addch(y, x, ch, attr)
        return True
    except curses.error:
        return False


def game_screen(
    stdscr,
    render_fn: RenderFn,
    on_regenerate: Optional[RegenerateFn] = None,
    path_color_name: str = "Rouge",
    entry_color_name: str = "Vert",
    exit_color_name: str = "Jaune",
    wall_color_name: str = "Blanc",
    title: str = "A-MAZE-ING",
) -> str:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass

        path_c = Colors.to_curses(path_color_name)
        entry_c = Colors.to_curses(entry_color_name)
        exit_c = Colors.to_curses(exit_color_name)
        wall_c = Colors.to_curses(wall_color_name)
        curses.init_pair(5, wall_c, -1)
        WALL_ATTR = curses.color_pair(5) | curses.A_BOLD

        # Chemin: bloc (fond coloré)
        curses.init_pair(1, path_c, path_c)
        PATH_ATTR = curses.color_pair(1)

        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        CLOSED_ATTR = curses.color_pair(4)

        # Entry/Exit: texte coloré sur fond terminal
        curses.init_pair(2, entry_c, -1)
        ENTRY_ATTR = curses.color_pair(2) | curses.A_BOLD

        curses.init_pair(3, exit_c, -1)
        EXIT_ATTR = curses.color_pair(3) | curses.A_BOLD
    else:
        PATH_ATTR = curses.A_REVERSE
        ENTRY_ATTR = curses.A_BOLD
        EXIT_ATTR = curses.A_BOLD
        CLOSED_ATTR = curses.A_DIM
        WALL_ATTR = curses.A_BOLD

    show_path = True
    WALL_CHARS = {
        "━", "┃", "╋", "┏", "┓", "┗", "┛", "┣", "┫", "┳", "┻",
        "─", "│", "┼", "╭", "╮", "╰", "╯", "├", "┤", "┬", "┴",
        "═", "║", "╬", "╔", "╗", "╚", "╝", "╠", "╣", "╦", "╩",
        }
    while True:
        maze_lines, moves, path, closed_cells = render_fn()

        # transforme path (cell coords) => positions dans le rendu "out"
        path_pos = _path_to_out_positions(path)
        start_pos = None
        goal_pos = None
        if path:
            xs, ys = path[0]
            xg, yg = path[-1]
            start_pos = (2 * ys + 1, 2 * xs + 1)
            goal_pos = (2 * yg + 1, 2 * xg + 1)

        stdscr.erase()
        h, w = stdscr.getmaxyx()

        header = f"{title} - M: Menu - R: Regenerate - \
P: Path {'ON' if show_path else 'OFF'}"
        x0 = max(0, (w - len(header)) // 2)
        try:
            stdscr.addstr(0, x0, header, curses.A_BOLD)
        except curses.error:
            pass

        maze_h = len(maze_lines)
        maze_w = max((len(ll) for ll in maze_lines), default=0)

        needed_h = 2 + maze_h + 2
        needed_w = max(len(header), maze_w, 20)

        if h < needed_h or w < needed_w:
            msg1 = "Terminal trop petit pour afficher le labyrinthe."
            msg2 = f"Taille mini ~ {needed_w}x{needed_h}  (actuel: {w}x{h})"
            msg3 = "Agrandis la fenêtre, puis appuie sur S. Q pour quitter."
            for (yy, msg, attr) in [(3, msg1, curses.A_BOLD),
                                    (5, msg2, 0), (7, msg3, 0)]:
                try:
                    stdscr.addstr(yy, max(0, (w - len(msg)) // 2), msg, attr)
                except curses.error:
                    pass
            stdscr.refresh()
        else:
            top = 2
            left = max(0, (w - maze_w) // 2)

            for r, line in enumerate(maze_lines):
                y = top + r
                if y >= h - 2:
                    break
            # dessine caractère par caractère pour pouvoir colorer le chemin
                for c, ch in enumerate(line):
                    x = left + c
                    if x >= w - 1:
                        break
                    # Priorité: ENTRY -> EXIT -> PATH -> normal
                    if start_pos is not None and (r, c) == start_pos:
                        _safe_addch(stdscr, y, x, ch, ENTRY_ATTR)
                    elif goal_pos is not None and (r, c) == goal_pos:
                        _safe_addch(stdscr, y, x, ch, EXIT_ATTR)
                    elif show_path and (r, c) in path_pos:
                        _safe_addch(stdscr, y, x, " ", PATH_ATTR)
                    elif (r, c) in closed_cells:
                        _safe_addch(stdscr, y, x, " ", CLOSED_ATTR)
                    else:
                        if ch in WALL_CHARS:
                            _safe_addch(stdscr, y, x, ch, WALL_ATTR)
                        else:
                            _safe_addch(stdscr, y, x, ch)

            footer = f"Moves: {moves}"
            try:
                stdscr.addstr(h - 2, 1, footer[: max(0, w - 2)])
            except curses.error:
                pass

            stdscr.refresh()

        key = stdscr.getch()
        if key in (ord("p"), ord("P")):
            show_path = not show_path
            continue
        if key in (ord("m"), ord("M"), 27):
            return "back"
        if key in (ord("r"), ord("R")) and on_regenerate is not None:
            on_regenerate()
