import curses

def _clamp_int(value: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, value))

def option_screen(stdscr, settings: dict) -> dict:
    curses.curs_set(0)
    stdscr.nodelay(False)
    stdscr.keypad(True)

    # NOTE: settings contient déjà ENTRY et EXIT sous forme tuple (x,y)
    fields = [
        "WIDTH", "HEIGHT",
        "ENTRY_X", "ENTRY_Y",
        "EXIT_X", "EXIT_Y",
        "SYMBOL_THEME", "BEAUTIFY", "PATH_COLOR",
        "Back",
    ]
    idx = 0

    while True:
        stdscr.erase()
        h, w = stdscr.getmaxyx()
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
                line = f"HEIGHT: {settings['HEIGHT']}"
            elif f == "ENTRY_X":
                line = f"ENTRY_X: {ex}"
            elif f == "ENTRY_Y":
                line = f"ENTRY_Y: {ey}"
            elif f == "EXIT_X":
                line = f"EXIT_X: {sx}"
            elif f == "EXIT_Y":
                line = f"EXIT_Y: {sy}"
            elif f == "SYMBOL_THEME":
                line = f"SYMBOL_THEME: {settings['SYMBOL_THEME']}"
            elif f == "BEAUTIFY":
                line = f"BEAUTIFY: {'ON' if settings['BEAUTIFY'] else 'OFF'}"
            elif f == "PATH_COLOR":
                line = f"PATH_COLOR: {settings['PATH_COLOR']}"
            else:
                line = f

            stdscr.addstr(start_y + i, max(0, (w - len(line)) // 2), line, attr)

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
            settings["PATH_COLOR"] = "Rouge"

        elif key in (curses.KEY_LEFT, curses.KEY_RIGHT, ord('a'), ord('d')):
            f = fields[idx]
            delta = -1 if key in (curses.KEY_LEFT, ord('a')) else 1

            ex, ey = settings["ENTRY"]
            sx, sy = settings["EXIT"]

            if f == "WIDTH":
                settings["WIDTH"] = _clamp_int(settings["WIDTH"] + 2 * delta, 9, 199)
                if settings["WIDTH"] % 2 == 0:
                    settings["WIDTH"] += 1
            elif f == "HEIGHT":
                settings["HEIGHT"] = _clamp_int(settings["HEIGHT"] + 2 * delta, 9, 199)
                if settings["HEIGHT"] % 2 == 0:
                    settings["HEIGHT"] += 1

            elif f == "ENTRY_X":
                settings["ENTRY"] = (ex + delta, ey)
            elif f == "ENTRY_Y":
                settings["ENTRY"] = (ex, ey + delta)
            elif f == "EXIT_X":
                settings["EXIT"] = (sx + delta, sy)
            elif f == "EXIT_Y":
                settings["EXIT"] = (sx, sy + delta)

            elif f == "SYMBOL_THEME":
                themes = ["A", "B", "C"]
                cur = themes.index(settings["SYMBOL_THEME"])
                settings["SYMBOL_THEME"] = themes[(cur + delta) % len(themes)]
            elif f == "BEAUTIFY":
                settings["BEAUTIFY"] = not settings["BEAUTIFY"]
            elif f == "PATH_COLOR":
                colors = ["Rouge", "Bleu", "Vert", "Jaune", "Cyan", "Blanc", "Noir"]
                cur = colors.index(settings["PATH_COLOR"]) if settings["PATH_COLOR"] in colors else 0
                settings["PATH_COLOR"] = colors[(cur + delta) % len(colors)]

        elif key in (curses.KEY_ENTER, 10, 13):
            if fields[idx] == "Back":
                return settings