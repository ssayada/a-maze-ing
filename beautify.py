from symbol import Symbol

def beautify_junctions(out: list[list[str]], symb_type: str) -> None:
    symbol = Symbol(symb_type, 2)
    h = len(out)
    w = len(out[0])

    def is_hwall(ch: str) -> bool:
        return ch == symbol.H_WALL

    def is_vwall(ch: str) -> bool:
        return ch == symbol.V_WALL

    for r in range(0, h, 2):
        for c in range(0, w, 2):
            up = (r - 1 >= 0) and is_vwall(out[r - 1][c])
            down = (r + 1 < h) and is_vwall(out[r + 1][c])
            left = (c - 1 >= 0) and is_hwall(out[r][c - 1])
            right = (c + 1 < w) and is_hwall(out[r][c + 1])

            mask = (up, right, down, left)

            # coins arrondis
            if mask == (False, True, True, False):
                out[r][c] = symbol.ULCOIN
            elif mask == (False, False, True, True):
                out[r][c] = symbol.URCOIN
            elif mask == (True, True, False, False):
                out[r][c] = symbol.DLCOIN
            elif mask == (True, False, False, True):
                out[r][c] = symbol.DRCOIN

            # jonctions / croix
            elif up and right and down and left:
                out[r][c] = symbol.DOT
            elif up and down and left and not right:
                out[r][c] = symbol.RIGHT
            elif up and down and right and not left:
                out[r][c] = symbol.LEFT
            elif left and right and up and not down:
                out[r][c] = symbol.DOWN
            elif left and right and down and not up:
                out[r][c] = symbol.UP

            # segments simples
            elif up and down and not left and not right:
                out[r][c] = symbol.V_WALL
            elif left and right and not up and not down:
                out[r][c] = symbol.H_WALL

            # bouts
            elif down and right and not up and not left:
                out[r][c] = symbol.ULCOIN
            elif down and left and not up and not right:
                out[r][c] = symbol.URCOIN
            elif up and right and not down and not left:
                out[r][c] = symbol.DLCOIN
            elif up and left and not down and not right:
                out[r][c] = symbol.DRCOIN
            else:
                out[r][c] = " "  # aucune connexion, on enlève le point