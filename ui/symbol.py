"""Définition des jeux de caractères utilisés pour dessiner le labyrinthe."""


class Symbol:
    """Jeu de symboles (murs, coins, entrée/sortie) pour un thème donné."""
    def __init__(self, name: str, round: int):
        """Initialise un thème de symboles.

        Parameters
        ----------
        name : str
            Identifiant du thème ("A", "B" ou "C").
        round : int
            Paramètre conservé pour compatibilité ; utilisé par l'appelant.

        Notes
        -----
        Les attributs (``H_WALL``, ``V_WALL``, ``DOT``, etc.) sont définis en
        fonction du thème.
        """
        self.name = name
        self.round = round
        if self.name == "A":
            self.H_WALL = "━"
            self.V_WALL = "┃"
            self.FILL = " "
            self.DOT = "╋"
            self.ENTRY = "#"
            self.EXIT = "$"
            self.PATH = "%"
            self.ULCOIN = "┏"
            self.URCOIN = "┓"
            self.DLCOIN = "┗"
            self.DRCOIN = "┛"
            self.LEFT = "┣"
            self.RIGHT = "┫"
            self.UP = "┳"
            self.DOWN = "┻"
        elif self.name == "B":
            self.H_WALL = "─"
            self.V_WALL = "│"
            self.FILL = " "
            self.DOT = "┼"
            self.ENTRY = "#"
            self.EXIT = "$"
            self.PATH = "%"
            self.ULCOIN = "╭"
            self.URCOIN = "╮"
            self.DLCOIN = "╰"
            self.DRCOIN = "╯"
            self.LEFT = "├"
            self.RIGHT = "┤"
            self.UP = "┬"
            self.DOWN = "┴"
        elif self.name == "C":
            self.H_WALL = "═"
            self.V_WALL = "║"
            self.FILL = " "
            self.DOT = "╬"
            self.ENTRY = "#"
            self.EXIT = "$"
            self.PATH = "%"
            self.ULCOIN = "╔"
            self.URCOIN = "╗"
            self.DLCOIN = "╚"
            self.DRCOIN = "╝"
            self.LEFT = "╠"
            self.RIGHT = "╣"
            self.UP = "╦"
            self.DOWN = "╩"
