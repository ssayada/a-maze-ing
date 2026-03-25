from pydantic import BaseModel, field_validator, ValidationError


class ConfigModel(BaseModel):
    width: int
    length: int
    entry_point: tuple[int, int]
    exit_point: tuple[int, int]
    output_file: str
    perfect: bool

    @field_validator("entry_point", "exit_point", mode="before")
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
