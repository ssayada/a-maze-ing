#! /usr/bin/python3
import curses


def recup_config() -> dict[str, str]:
    config: dict[str, str] = {}
    with open("config.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            config[key] = value
    return config


def afficher_labyrinthe_murs(fichier="maze.txt"):
    with open(fichier, "r", encoding="utf-8") as f:
        lignes = [ligne.rstrip("\n") for ligne in f]
    maze_coord = recup_config()
    x = int(maze_coord["LENGTH"])
    y = int(maze_coord["WIDTH"])
    length = x * 2 + 1
    width = y * 2 + 1
    j = 0
    list_maze = []
    while j < width:
        i = 0
        if j % 2 == 0:
            while i < length:
                if i == 0:
                    if j == 0:
                        list_maze.append("┏")
                    elif j > 0 and j < width - 1:
                        list_maze.append("┣")
                    else:
                        list_maze.append("┗")
                elif i == length - 1:
                    if j == 0:
                        list_maze.append("┓")
                    elif j > 0 and j < width - 1:
                        list_maze.append("┫")
                    else:
                        list_maze.append("┛")
                else:
                    if i % 2 == 0 and j == 0:
                        list_maze.append("┳")
                    elif i % 2 == 0 and j == width - 1:
                        list_maze.append("┻")
                    elif i % 2 == 0:
                        list_maze.append("╋")
                    else:
                        list_maze.append("━")
                i += 1
        else:
            while i < length:
                if i % 2 == 0:
                    list_maze.append("┃")
                else:
                    list_maze.append(" ")
                i += 1
        list_maze.append("\n")
        j += 1
    i = 0
    for c in list_maze:
        print(f"{c}", end="")


def launcher() -> None:
    afficher_labyrinthe_murs()


if __name__ == "__main__":
    launcher()
