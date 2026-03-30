#!/usr/bin/env python3
from launcher import launcher


def main():
    try:
        launcher()
    except OSError as e:
        print(e)
    except ValueError as e:
        print(e)
    except IndexError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    except KeyError as e:
        print("init_config.txt invalide ou illisible")


if __name__ == "__main__":
    main()
