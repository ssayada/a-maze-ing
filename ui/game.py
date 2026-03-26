import curses
from collections.abc import Callable
from typing import Optional
from ui.colors import Colors

# render_fn returns: (maze_lines, moves, path)
RenderFn = Callable[[], tuple[list[str], str, list[tuple[int, int]]]]
RegenerateFn = Callable[[], None]


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
    path_color_name = "Rouge",
    title: str = "A-MAZE-ING",
) -> str:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    # couleurs
    if curses.has_colors():
        curses.start_color()
        try:
            curses.use_default_colors()
        except curses.error:
            pass
        c = Colors.to_curses(path_color_name)
        curses.init_pair(1, c, c)
        PATH_ATTR = curses.color_pair(1)
    else:
        PATH_ATTR = curses.A_REVERSE  # fallback

    while True:
        maze_lines, moves, path = render_fn()

        # transforme path (cell coords) => positions dans le rendu "out"
        path_pos = {(2 * y + 1, 2 * x + 1) for (x, y) in path}

        stdscr.erase()
        h, w = stdscr.getmaxyx()

        header = f"{title} — Q: Menu  R: Regenerate  S: Refresh"
        x0 = max(0, (w - len(header)) // 2)
        try:
            stdscr.addstr(0, x0, header, curses.A_BOLD)
        except curses.error:
            pass

        maze_h = len(maze_lines)
        maze_w = max((len(l) for l in maze_lines), default=0)

        needed_h = 2 + maze_h + 2
        needed_w = max(len(header), maze_w, 20)

        if h < needed_h or w < needed_w:
            msg1 = "Terminal trop petit pour afficher le labyrinthe."
            msg2 = f"Taille mini ~ {needed_w}x{needed_h}  (actuel: {w}x{h})"
            msg3 = "Agrandis la fenêtre, puis appuie sur S. Q pour quitter."
            for (yy, msg, attr) in [(3, msg1, curses.A_BOLD), (5, msg2, 0), (7, msg3, 0)]:
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
                    if (r, c) in path_pos:
                        _safe_addch(stdscr, y, x, " ", PATH_ATTR)
                    else:
                        _safe_addch(stdscr, y, x, ch)

            footer = f"Moves: {moves}"
            try:
                stdscr.addstr(h - 2, 1, footer[: max(0, w - 2)])
            except curses.error:
                pass

            stdscr.refresh()

        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return "back"
        if key in (ord("r"), ord("R")) and on_regenerate is not None:
            on_regenerate()
        if key in (ord("s"), ord("S"), curses.KEY_RESIZE):
            continue