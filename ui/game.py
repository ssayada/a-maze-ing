import curses
from collections.abc import Callable
from typing import Optional


RenderFn = Callable[[], tuple[list[str], str]]
RegenerateFn = Callable[[], None]


def _safe_addstr(
        stdscr, y: int, x: int,
        s: str, attr: int = 0) -> bool:
    try:
        stdscr.addstr(y, x, s, attr)
        return True
    except curses.error:
        return False


def _draw_centered_lines(
        stdscr, lines: list[str],
        top: int) -> None:
    h, w = stdscr.getmaxyx()
    for i, line in enumerate(lines):
        y = top + i
        if y >= h - 1:
            break
        #centre horizontal et coupe si trop long
        if len(line) <= w:
            x = max(0, (w - len(line)) // 2)
            _safe_addstr(stdscr, y, x, line)
        else:
            _safe_addstr(stdscr, y, 0, line[: max(0, w - 1)])


def game_screen(
    stdscr,
    render_fn: RenderFn,
    on_regenerate: Optional[RegenerateFn] = None,
    title: str = "A-MAZE-ING",
) -> str:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)
    while True:
        maze_lines, moves = render_fn()
        stdscr.erase()
        h, w = stdscr.getmaxyx()
        header = f"{title} — Q: Menu  R: Regenerate  S: Refresh"
        _safe_addstr(stdscr, 0, max(0, (w - len(header)) // 2), header, curses.A_BOLD)

        # Calcule la place nécessaire (labyrinthe + footer)
        maze_h = len(maze_lines)
        maze_w = max((len(l) for l in maze_lines), default=0)

        # message si terminal trop petit
        needed_h = 2 + maze_h + 2
        needed_w = max(len(header), maze_w, 20)
        if h < needed_h or w < needed_w:
            msg1 = "Terminal trop petit pour afficher le labyrinthe."
            msg2 = f"Taille mini ~ {needed_w}x{needed_h}  (actuel: {w}x{h})"
            msg3 = "Agrandis la fenêtre, puis appuie sur S. Q pour quitter."
            _safe_addstr(stdscr, 3, max(0, (w - len(msg1)) // 2), msg1, curses.A_BOLD)
            _safe_addstr(stdscr, 5, max(0, (w - len(msg2)) // 2), msg2)
            _safe_addstr(stdscr, 7, max(0, (w - len(msg3)) // 2), msg3)
            stdscr.refresh()
        else:
            top = 2
            _draw_centered_lines(stdscr, maze_lines, top=top)
            footer = f"Moves: {moves}"
            _safe_addstr(stdscr, h - 2, 1, footer[: max(0, w - 2)])
            stdscr.refresh()
        key = stdscr.getch()
        if key in (ord("q"), ord("Q"), 27):
            return "back"
        if key in (ord("r"), ord("R")) and on_regenerate is not None:
            on_regenerate()
        if key in (ord("s"), ord("S"), curses.KEY_RESIZE):
            continue
