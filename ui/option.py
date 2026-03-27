import curses


def _clamp_int(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))


def _normalize_entry_exit(settings: dict) -> None:
    w = settings["WIDTH"]
    h = settings["HEIGHT"]

    def clamp(p: tuple[int, int]) -> tuple[int, int]:
        x, y = p
        x = max(0, min(w - 1, x))
        y = max(0, min(h - 1, y))
        return (x, y)

    settings["ENTRY"] = clamp(settings["ENTRY"])
    settings["EXIT"] = clamp(settings["EXIT"])

    # évite ENTRY == EXIT (décale EXIT)
    if settings["ENTRY"] == settings["EXIT"]:
        ex, ey = settings["ENTRY"]
        candidates = [(ex + 1, ey), (ex, ey + 1), (ex - 1, ey), (ex, ey - 1)]
        for cx, cy in candidates:
            if 0 <= cx < w and 0 <= cy < h:
                settings["EXIT"] = (cx, cy)
                break


def _wrap_int(value: int, lo: int, hi: int) -> int:
    if value > hi:
        return lo
    if value < lo:
        return hi
    return value


def _make_odd(n: int) -> int:
    return n if (n % 2 == 1) else (n + 1)


def option_screen(stdscr, settings: dict) -> dict:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    fields = [
        "WIDTH", "HEIGHT",
        "ENTRY_X", "ENTRY_Y",
        "EXIT_X", "EXIT_Y",
        "PERFECT", "COLOR_42", "WALL_COLOR",
        "PATH_COLOR", "SYMBOL_THEME", "BEAUTIFY",
        "Back",
    ]
    idx = 0

    while True:
        stdscr.erase()
        _normalize_entry_exit(settings)
        h, w = stdscr.getmaxyx()
        MIN_W = 9
        MIN_H = 9
        header = "A-MAZE-ING — Q: Menu  R: Regenerate"
        max_height = (h - 5) // 2
        max_width_from_term = (w - 1) // 2
        max_width_from_header = (w - max(len(header), 20) - 1) // 2
        max_width = min(max_width_from_term, max_width_from_header)
        if max_width < MIN_W:
            max_width = MIN_W
        if max_height < MIN_H:
            max_height = MIN_H
        if max_width % 2 == 0:
            max_width -= 1
        if max_height % 2 == 0:
            max_height -= 1

        title = "Options"
        stdscr.addstr(2, max(0, (w - len(title)) // 2), title, curses.A_BOLD)
        help_txt = "↑/↓: choisir — ←/→: modifier — Entrée: back — R: reset"
        stdscr.addstr(4, max(0, (w - len(help_txt)) // 2), help_txt)

        ex, ey = settings["ENTRY"]
        sx, sy = settings["EXIT"]

        start_y = 7
        for i, f in enumerate(fields):
            selected = (i == idx)
            attr = curses.A_REVERSE if selected else curses.A_NORMAL

            if f == "Back":
                line = "Back"
            elif f == "WIDTH":
                line = f"WIDTH: {settings['WIDTH']}"
            elif f == "HEIGHT":
                line = f" HEIGHT: {settings['HEIGHT']}"
            elif f == "ENTRY_X":
                line = f" ENTRY_X: {ex}"
            elif f == "ENTRY_Y":
                line = f" ENTRY_Y: {ey}"
            elif f == "EXIT_X":
                line = f" EXIT_X: {sx}"
            elif f == "EXIT_Y":
                line = f" EXIT_Y: {sy}"
            elif f == "PERFECT":
                line = f"   PERFECT: \
{'ON' if settings.get('PERFECT', True) else 'OFF'}"
            elif f == "COLOR_42":
                line = f"    COLOR_42: \
{'ON' if settings.get('COLOR_42', False) else 'OFF'}"
            elif f == "WALL_COLOR":
                line = f"        WALL_COLOR: \
{settings.get('WALL_COLOR', 'Blanc')}"
            elif f == "SYMBOL_THEME":
                line = f"      SYMBOL_THEME: \
{settings['SYMBOL_THEME']}"
            elif f == "BEAUTIFY":
                line = f"   BEAUTIFY: \
{'ON' if settings['BEAUTIFY'] else 'OFF'}"
            elif f == "PATH_COLOR":
                line = f"        PATH_COLOR: {settings['PATH_COLOR']}"

            stdscr.addstr(start_y + i, max(0,
                                           (w - len(line)) // 2), line, attr)

        stdscr.refresh()

        key = stdscr.getch()
        if key in (ord('q'), ord('Q'), 27):
            return settings

        if key in (curses.KEY_UP, ord('w')):
            idx = (idx - 1) % len(fields)
        elif key in (curses.KEY_DOWN, ord('s')):
            idx = (idx + 1) % len(fields)

        elif key in (ord('r'), ord('R')):
            settings["WIDTH"] = 25
            settings["HEIGHT"] = 20
            settings["ENTRY"] = (0, 0)
            settings["EXIT"] = (19, 14)
            settings["SYMBOL_THEME"] = "A"
            settings["BEAUTIFY"] = True
            settings["PERFECT"] = False
            settings["COLOR_42"] = False
            settings["WALL_COLOR"] = "Blanc"
            settings["PATH_COLOR"] = "Rouge"
            _normalize_entry_exit(settings)

        elif key in (curses.KEY_LEFT, curses.KEY_RIGHT, ord('a'), ord('d')):
            f = fields[idx]
            delta = -1 if key in (curses.KEY_LEFT, ord('a')) else 1

            ex, ey = settings["ENTRY"]
            sx, sy = settings["EXIT"]

            if f == "WIDTH":
                new_w = settings["WIDTH"] + 2 * delta
                new_w = _wrap_int(new_w, MIN_W, max_width)
                new_w = _make_odd(new_w)
                settings["WIDTH"] = new_w
            elif f == "HEIGHT":
                new_h = settings["HEIGHT"] + 2 * delta
                new_h = _wrap_int(new_h, MIN_H, max_height)
                new_h = _make_odd(new_h)
                settings["HEIGHT"] = new_h
            elif f == "ENTRY_X":
                settings["ENTRY"] = (ex + delta, ey)
            elif f == "ENTRY_Y":
                settings["ENTRY"] = (ex, ey + delta)
            elif f == "EXIT_X":
                settings["EXIT"] = (sx + delta, sy)
            elif f == "EXIT_Y":
                settings["EXIT"] = (sx, sy + delta)
            elif f == "PERFECT":
                settings["PERFECT"] = not settings.get("PERFECT", False)
            elif f == "COLOR_42":
                settings["COLOR_42"] = not settings.get("COLOR_42", False)
            elif f == "SYMBOL_THEME":
                themes = ["A", "B", "C"]
                cur = themes.index(settings["SYMBOL_THEME"])
                settings["SYMBOL_THEME"] = themes[(cur + delta) % len(themes)]
            elif f == "BEAUTIFY":
                settings["BEAUTIFY"] = not settings["BEAUTIFY"]
            elif f == "PATH_COLOR":
                colors = [
                    "Rouge", "Bleu", "Vert", "Jaune",
                    "Cyan", "Blanc", "Noir"]
                cur = (colors.index(settings["PATH_COLOR"])
                       if settings["PATH_COLOR"] in colors else 0)
                settings["PATH_COLOR"] = colors[(cur + delta) % len(colors)]
            elif f == "WALL_COLOR":
                colors = [
                    "Rouge", "Bleu", "Vert", "Jaune",
                    "Cyan", "Blanc", "Noir"]
                cur = (colors.index(settings["WALL_COLOR"])
                       if settings.get("WALL_COLOR") in colors else 0)
                settings["WALL_COLOR"] = colors[(cur + delta) % len(colors)]
            _normalize_entry_exit(settings)

        elif key in (curses.KEY_ENTER, 10, 13):
            if fields[idx] == "Back":
                return settings
