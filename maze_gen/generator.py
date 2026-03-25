from pydantic import BaseModel, field_validator, ValidationError


class EntryExitError(Exception):
    def __init__(self, message) -> None:
        self.message = message
        super().__init__(self.message)


class ConfigModel(BaseModel):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_coords(cls, v):
        if isinstance(v, str):
            x, y = v.split(",")
            return (int(x), int(y))
        return v


def parse_config_file() -> dict:
    configs = {}
    try:
        with open("config.txt") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=")
                    configs[key.strip()] = value.strip()
    except ValueError:
        print(f"Invalid 'config.txt' file: too many '=' in 'line {line}'.")
        return {}
    return configs


def verify_config_file(configs: dict) -> None:
    try:
        verif = ConfigModel(**configs)
        if configs['ENTRY'] == configs['EXIT']:
            raise EntryExitError("ENTRY and EXIT points are identic.")
        return True
    except ValidationError:
        print("Invalid 'config.txt' file: missing a mandatory key.")
        return False
    except EntryExitError as e:
        print(f"Error: {e}")


def maze_generator() -> None:
    pass


def main() -> None:
    conf_dict = parse_config_file()
    if not conf_dict:
        return
    if not verify_config_file(conf_dict):
        return


if __name__ == '__main__':
    main()
