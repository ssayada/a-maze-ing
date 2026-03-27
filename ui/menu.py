import curses


def menu_screen(stdscr, title="A-MAZE-ING") -> str:
    curses.curs_set(0)  # affichage du curseur
    stdscr.nodelay(False)  # bloque en attendant qu'une touche soit presse
    stdscr.keypad(True)  # traduit les touches speciales
    items = ["Start", "Options", "Quit"]
    selected = 0

    while True:
        stdscr.erase()  # efface le contenu afficher a chaque boucle
        h, w = stdscr.getmaxyx()  # recup taille fenetre

        # titre
        y = 2
        x = max(0, (w - len(title)) // 2)
        stdscr.addstr(y, x, title, curses.A_BOLD)
        # affiche title A_BOLD = gras

        # aide a la navigation
        help_txt = "↑/↓ pour naviguer — Entrée pour valider — Q pour quitter"
        stdscr.addstr(y + 2, max(0, (w - len(help_txt)) // 2), help_txt)

        # menu items
        start_y = y + 5
        for i, it in enumerate(items):
            line = f"{'▶ ' if i == selected else '  '}{it}"
            attr = curses.A_REVERSE if i == selected else curses.A_NORMAL
            # ↑ surbrillance de l'option selectionnee
            stdscr.addstr(start_y + i,
                          max(0, (w - len(line)) // 2), line, attr)

        stdscr.refresh()  # met a jour l'affichage reel du terminal

        key = stdscr.getch()  # sert a lire une touche du clavier
        if key in (ord('q'), ord('Q'), 27):  # ord() converti carac en ASCII
            return "quit"
        if key in (curses.KEY_UP, ord('w')):  # sert a se deplacer dans menu
            selected = (selected - 1) % len(items)  # len(items) boucle
        elif key in (curses.KEY_DOWN, ord('s')):
            selected = (selected + 1) % len(items)
        elif key in (curses.KEY_ENTER, 10, 13):  # 10,13 code pour return enter
            if items[selected] == "Start":
                return "start"
            if items[selected] == "Options":
                return "options"
            return "quit"
