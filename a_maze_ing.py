#!/usr/bin/env python3
from launcher import launcher
from curses import error


def main() -> None:
    init_config = """WIDTH=25
HEIGHT=20
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False"""
    try:
        launcher()
    except OSError as e:
        print(e)
    except ValueError as e:
        print(e)
    except KeyError:
        print("init_config.txt invalide ou illisible")
    except IndexError:
        print("'ENTRY' or 'EXIT' in 42 logo")
    except FileNotFoundError as e:
        print(e)
    except error:
        print("curses error: la taille de la fenetre est trop \
petite pour l'affichage")
    finally:
        with open("config.txt", "w") as file:
            file.write(init_config)


if __name__ == "__main__":
    main()
