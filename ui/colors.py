import curses

class Colors:
    MAP = {
        "Rouge": curses.COLOR_RED,
        "Bleu": curses.COLOR_BLUE,
        "Vert": curses.COLOR_GREEN,
        "Jaune": curses.COLOR_YELLOW,
        "Cyan": curses.COLOR_CYAN,
        "Noir": curses.COLOR_BLACK,
        "Blanc": curses.COLOR_WHITE,
    }

    @staticmethod
    def to_curses(name: str) -> int:
        return Colors.MAP.get(name, curses.COLOR_RED)