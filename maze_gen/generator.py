"""Lecture/validation de la configuration et génération d'un labyrinthe.

Ce module fournit :
- un modèle Pydantic pour valider les clés de configuration ;
- des fonctions de parsing/écriture de ``config.txt`` ;
- un point d'entrée pour générer un labyrinthe via :class:`maze_gen.Maze`.
"""
from pydantic import BaseModel, field_validator, ValidationError
from maze_gen.maze_generator import Maze


# Custom error if ENTRY and EXIT are on the same coordinates
class EntryExitError(Exception):
    """Erreur levée si ENTRY et EXIT sont identiques après validation."""
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


# Pydantic model which is used to verify the config.txt file
class ConfigModel(BaseModel):
    """Modèle Pydantic représentant les paramètres attendus dans config.txt."""
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool

    @field_validator("ENTRY", "EXIT", mode="before")
    @classmethod
    def parse_coords(cls, v: tuple) -> tuple:
        """Convertit une coordonnée "x,y" en tuple d'entiers.

        Parameters
        ----------
        v : tuple
            Valeur brute (souvent une chaîne "x,y" avant parsing).

        Returns
        -------
        tuple
            Coordonnées converties.
        """
        if isinstance(v, str):
            x, y = v.split(",")
            return (int(x), int(y))
        return v


def _parse_bool(s: str) -> bool:
    """Convertit une chaîne en booléen.

    Parameters
    ----------
    s : str
        Valeur à convertir.

    Returns
    -------
    bool
        Booléen correspondant.

    Raises
    ------
    ValueError
        Si la valeur n'est pas reconnue.
    """
    s = s.strip().lower()
    if s in ("true", "1", "yes", "y", "on"):
        return True
    if s in ("false", "0", "no", "n", "off"):
        return False
    raise ValueError(f"Invalid boolean value: {s}")


# Parse the config.txt file
def parse_config_file(config_file: str) -> dict:
    """Parse un fichier de configuration KEY=VALUE.

    Parameters
    ----------
    config_file : str
        Chemin du fichier (ex. ``config.txt``).

    Returns
    -------
    dict
        Dictionnaire de configuration. Retourne ``{}`` si parsing/validation
        échoue.
    """
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
                    elif key == "SEED":
                        configs.update({key: int(value)})

    except Exception as e:
        print(f"Invalid '{config_file}' file: {e}")
        return {}
    return configs if verify_config_file(configs) else {}


def verify_config_file(configs: dict) -> bool:
    """Valide une configuration avec Pydantic et des règles additionnelles.

    Parameters
    ----------
    configs : dict
        Configuration à vérifier.

    Returns
    -------
    bool
        True si la configuration est valide, sinon False.
    """
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
    """Écrit un fichier de configuration (config.txt) à partir d'un dict.

    Parameters
    ----------
    configs : dict
        Configuration à écrire.
    config_file : str, default="config.txt"
        Chemin du fichier cible.

    Returns
    -------
    None
    """
    if "SEED" in configs.keys():
        lines = [
            f"WIDTH={int(configs['WIDTH'])}",
            f"HEIGHT={int(configs['HEIGHT'])}",
            f"ENTRY={configs['ENTRY'][0]},{configs['ENTRY'][1]}",
            f"EXIT={configs['EXIT'][0]},{configs['EXIT'][1]}",
            f"OUTPUT_FILE={configs.get('OUTPUT_FILE', 'maze.txt')}",
            f"PERFECT={'True' if configs.get('PERFECT', True) else 'False'}",
            f"SEED={configs['SEED']}"
        ]
    else:
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
    """Génère un labyrinthe et l'écrit dans un fichier.

    Parameters
    ----------
    configs : dict
        Configuration (dimensions, entry/exit, perfect, etc.).
    maze_file : str
        Chemin du fichier de sortie (écriture).

    Returns
    -------
    None
    """
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
