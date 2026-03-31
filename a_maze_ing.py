#!/usr/bin/env python3
from launcher import launcher
from curses import error


def main() -> None:
    try:
        launcher()
    except OSError as e:
        print(e)
    except ValueError as e:
        print(e)
    except IndexError:
        print("'ENTRY' or 'EXIT' in 42 logo")
    except FileNotFoundError as e:
        print(e)
    except KeyError:
        print("init_config.txt invalide ou illisible")
    except error:
        print("curses error: la taille de la fenetre est trop \
petite pour l'affichage")


if __name__ == "__main__":
    main()
