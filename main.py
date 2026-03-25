from maze_gen.generator import parse_config_file
from maze_gen.maze_generator import maze_gen
from amazing_anil import launcher


def main():
    print("Hello from a-maze-ing!")
    configs = parse_config_file("config.txt")
    maze_gen(configs, "maze.txt")
    launcher()


if __name__ == "__main__":
    main()
