from pydantic import BaseModel, field_validator, ValidationError


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
    with open("../config.txt") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                key, value = line.split("=")
                configs[key.strip()] = value.strip()
    return configs


def verify_config_file(configs: dict) -> None:
    try:
        verif = ConfigModel(**configs)
        print(verif)
    except ValidationError as e:
        print(e)


def maze_generator() -> None:
    pass


def main() -> None:
    conf_dict = parse_config_file()
    print(conf_dict)
    verify_config_file(conf_dict)


if __name__ == '__main__':
    main()
