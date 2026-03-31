"""Conversion de noms de couleurs en constantes curses."""
import curses


class Colors:
    """Table de correspondance entre noms de couleurs (FR) et curses."""
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
        """Convertit un nom de couleur en constante curses.

        Parameters
        ----------
        name : str
            Nom de couleur (ex. "Rouge", "Bleu", "Vert").

        Returns
        -------
        int
            Constante ``curses.COLOR_*``. Par défaut, retourne ``COLOR_RED``.
        """
        return Colors.MAP.get(name, curses.COLOR_RED)
