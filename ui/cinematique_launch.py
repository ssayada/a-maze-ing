import curses
import random
import time


TITLE_ART = [
    r"    ___          __  __    _    ______  _____       _____ _   _   ____ ",
    r"   / _ \        |  \/  |  / \  |___  / | ____|     |_   _| \ | | / ___|",
    r"  / /_\ \   ___ | |\/| | / _ \    / /  |  _|   ___   | | |  \| || |  _ ",
    r" / / _ \ \ |___|| |  | |/ ___ \  / /__ | |___ |___|  | | | |\  || |_| |",
    r"/_/     \_\     |_|  |_/_/   \_\/_____||_____|      |___||_| \_| \____|",
    r"                           BY  A - M A Z E - T E A M                 ",
]


def title_screen(stdscr, duration: float = 2.8, fps: int = 30) -> None:
    """
    Affiche un écran titre 'A-MAZE-ING' en ASCII qui bouge gauche/droite,
    avec des étoiles autour (scintillement).
    Quitte si une touche est pressée, sinon après `duration` secondes.
    ASCII only.
    """
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    h, w = stdscr.getmaxyx()

    # étoiles (positions fixes) + scintillement
    star_count = max(40, (h * w) // 120)
    stars = []
    for _ in range(star_count):
        sr = random.randint(0, max(0, h - 2))
        sc = random.randint(0, max(0, w - 2))
        stars.append([sr, sc])

    star_chars = ["*", ".", "+", "x"]

    title_h = len(TITLE_ART)
    title_w = max(len(line) for line in TITLE_ART)

    frame = 0

    while True:

        # touche pour passer
        ch = stdscr.getch()
        if ch != -1:
            break

        stdscr.erase()
        h, w = stdscr.getmaxyx()

        # oscillation horizontale (petit mouvement)
        # amplitude limitée pour rester visible
        amp = max(1, min(6, (w - title_w) // 4 if w > title_w else 1))
        xoff = int(amp * (1 if ((frame // 20) % 2 == 0) else -1))

        top = max(0, (h // 2) - (title_h // 2))
        left = max(0, (w // 2) - (title_w // 2) + xoff)

        # étoiles: scintillent + bougent un peu
        for i, (sr, sc) in enumerate(stars):
            # scintillement
            ch_star = star_chars[(frame + i) % len(star_chars)]

            # petit drift horizontal très lent
            if frame % 8 == 0 and random.random() < 0.15:
                sc = sc + random.choice([-1, 1])
                sc = max(0, min(w - 1, sc))
                stars[i][1] = sc

            # évite de dessiner sur le titre (zone approximative)
            if (top - 1 <= sr <= top + title_h and left - 2
                    <= sc <= left + title_w + 2):
                continue

            if 0 <= sr < h and 0 <= sc < w:
                try:
                    stdscr.addch(sr, sc, ch_star)
                except curses.error:
                    pass

        # dessine le titre
        for r, line in enumerate(TITLE_ART):
            rr = top + r
            if 0 <= rr < h:
                try:
                    stdscr.addstr(rr, left, line[: max(0, w - left)])
                except curses.error:
                    pass

        # texte "Press any key"
        hint = "Press any key to start"
        hr = min(h - 1, top + title_h + 2)
        hc = max(0, (w // 2) - (len(hint) // 2))  # emplacement du texte
        if frame % 20 < 12:  # clignotement
            try:
                stdscr.addstr(hr, hc, hint[: max(0, w - hc)])
            except curses.error:
                pass

        stdscr.refresh()

        frame += 1
        time.sleep(1.0 / fps)
