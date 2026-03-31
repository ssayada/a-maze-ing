#!/usr/bin/env python3
from launcher import launcher
import sys
from maze_gen.generator import parse_config_file, verify_config_file
from curses import error


def main() -> None:
    init_config = """WIDTH=25
HEIGHT=20
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False"""
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    else:
        config_file = "config.txt"
    try:
        with open(config_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open("config.txt", "w") as file:
            file.write(init_config)
    configs = parse_config_file(config_file)
    if not verify_config_file(configs):
        print("config.txt invalide ou illisible")
        return
    try:
        launcher()
    except OSError as e:
        print(e)
    except ValueError as e:
        print(e)
    except KeyError:
        print("config.txt invalide ou illisible")
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
