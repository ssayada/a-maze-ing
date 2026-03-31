from pydantic import BaseModel, field_validator, ValidationError
from maze_gen.maze_generator import Maze


# Custom error if ENTRY and EXIT are on the same coordinates
class EntryExitError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


# Pydantic model which is used to verify the config.txt file
class ConfigModel(BaseModel):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_coords(cls, v: tuple) -> tuple:
        if isinstance(v, str):
            x, y = v.split(",")
            return (int(x), int(y))
        return v


def _parse_bool(s: str) -> bool:
    s = s.strip().lower()
    if s in ("true", "1", "yes", "y", "on"):
        return True
    if s in ("false", "0", "no", "n", "off"):
        return False
    raise ValueError(f"Invalid boolean value: {s}")


# Parse the config.txt file
def parse_config_file(config_file: str) -> dict:
    configs = {
                "WIDTH": 0, "HEIGHT": 0,
                "ENTRY": (), "EXIT": (),
                "OUTPUT_FILE": "maze.txt",
                "PERFECT": True}
    try:
        with open(config_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    configs[key.strip()] = value.strip()
                    if key in ("WIDTH", "HEIGHT"):
                        configs[key] = int(value)
                    elif key in ("ENTRY", "EXIT"):
                        x, y = value.split(',')
                        configs[key] = (int(x), int(y))
                    elif key == "PERFECT":
                        configs[key] = _parse_bool(value)

    except Exception as e:
        print(f"Invalid '{config_file}' file: {e}")
        return {}
    return configs if verify_config_file(configs) else {}


# Verify the config.txt file with pydantic and the custom error
def verify_config_file(configs: dict) -> bool:
    try:
        ConfigModel(**configs)
        if configs["ENTRY"] == configs["EXIT"]:
            raise EntryExitError("ENTRY and EXIT points are identic.")
        return True
    except ValidationError:
        print(f"Invalid '{configs}' file: missing/invalid keys.")
        return False
    except EntryExitError as e:
        print(f"Error: {e}")
        return False


def write_config_file(configs: dict, config_file: str = "config.txt") -> None:
    lines = [
        f"WIDTH={int(configs['WIDTH'])}",
        f"HEIGHT={int(configs['HEIGHT'])}",
        f"ENTRY={configs['ENTRY'][0]},{configs['ENTRY'][1]}",
        f"EXIT={configs['EXIT'][0]},{configs['EXIT'][1]}",
        f"OUTPUT_FILE={configs.get('OUTPUT_FILE', 'maze.txt')}",
        f"PERFECT={'True' if configs.get('PERFECT', True) else 'False'}",
    ]
    with open(config_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def maze_gen(configs: dict, maze_file: str) -> None:
    '''
    ez
    '''
    maze = Maze(configs)
    if maze.forty_two_possible():
        maze.create_forty_two()
    maze.create_path()
    if configs['PERFECT']:
        maze.complete_maze(True)
    if not configs['PERFECT']:
        maze.complete_maze(False)
    maze.verify_maze()
    maze.draw_forty_two()
    with open(maze_file, 'w') as maze_open:
        for ll in maze.get_maze():
            for c in ll:
                maze_open.write(c)
            maze_open.write('\n')
