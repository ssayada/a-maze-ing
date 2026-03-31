*This project has been created as part of the 42 curriculum by Ssayada and Avally*

# A-MAZE-ING

## Description

**A-MAZE-ING** is a terminal (TUI) maze generator and maze visualizer written in **Python** using **curses**.

The program:
- Reads a configuration file (`config.txt`) describing the maze size, entry/exit points, output file, and whether the maze is *perfect*.
- Generates a maze and stores it in `maze.txt` using an **hexadecimal cell encoding** (each cell stores wall bits).
- Displays the maze in the terminal with multiple **symbol themes** and optional **beautification** of junctions.
- Computes and can display the shortest path between ENTRY and EXIT using an **A\*** solver (Manhattan heuristic).
- Provides an interactive menu: **Start**, **Options**, **Quit**.

---

## Instructions

### Prerequisites
- **Python 3**
- A Unix-like terminal supporting **curses** (Linux/macOS recommended)

### Install dependencies
Using the Makefile:
```bash
make install
```

Or manually:
```bash
pip3 install -r requirements.txt
```

### Run
Using the Makefile:
```bash
make run
```

Or manually:
```bash
python3 a_maze_ing.py config.txt
```

### Controls (in the TUI)
- **Menu**
  - `↑ / ↓` to navigate
  - `Enter` to validate
  - `Q` (or `Esc`) to quit/back
- **Game screen**
  - `M` (or `Esc`) : back to menu
  - `R` : regenerate a new maze
  - `P` : toggle path display ON/OFF
- **Options**
  - `↑ / ↓` : select a setting
  - `← / →` (or `A` / `D`) : change value
  - `R` : reset to defaults
  - `Enter` on **Back** : return

---

## Config file format (required)

The project uses a simple `KEY=VALUE` format in `config.txt` (and `init_config.txt` for initial defaults).

Example (`config.txt`):
```txt
WIDTH=25
HEIGHT=20
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
```

### Fields
- `WIDTH` (int): maze width (in cells)
- `HEIGHT` (int): maze height (in cells)
- `ENTRY` (x,y): entry cell coordinates
- `EXIT` (x,y): exit cell coordinates
- `OUTPUT_FILE` (str): output file (usually `maze.txt`)
- `PERFECT` (bool):  
  - `True`  => perfect maze (single unique path between any two cells)
  - `False` => imperfect maze (extra openings may exist)

Validation:
- The config is validated with **pydantic**.
- `ENTRY` and `EXIT` **must not** be identical (custom error handling).

---

## Maze generation algorithm (required)

### Encoding
The maze is stored in `maze.txt` as a grid of **hex characters** (`0`-`9`, `A`-`F`).
Each cell value encodes the presence of walls using bit flags (N/E/S/W).  
A value of `F` means “all walls present”.

### Generation approach
The generator builds a path starting from `ENTRY` and carving walls while tracking a backtrack history:
- It randomly tries directions (N/E/S/W).
- If the current cell is blocked (all adjacent cells already visited), it backtracks until it finds a cell with an unvisited neighbour.
- It continues until reaching the `EXIT`, then completes the rest of the maze.

For imperfect mazes (`PERFECT=False`), the generator may open additional walls while applying constraints (notably avoiding “too open” 3x3 areas).

---

## Why this algorithm? (required)

This approach is a good fit here because:
- It is **simple to implement** and works well with a **bit/hex wall representation**.
- It naturally supports **backtracking**, which guarantees progress even when the path hits a dead-end.
- It produces mazes that are visually interesting and can be extended to support **perfect** vs **imperfect** behaviours.
- It’s compatible with later steps like **A\*** solving (grid-based, 4-neighbour movement).

---

## What part of the code is reusable, and how? (required)

Several parts are reusable as standalone modules:

- **Config parsing & validation** (`maze_gen/generator.py`)
  - `parse_config_file()` / `write_config_file()` can be reused in any project needing a small validated config format.
  - `ConfigModel` (pydantic) provides a clean validation layer.

- **Maze generation engine** (`maze_gen/maze_generator.py`)
  - The `Maze` class and helpers can be reused to generate hex-encoded mazes for other renderers (GUI, web, etc.).

- **Pathfinding** (`solver.py`)
  - `a_star()` + `neighbors_from_bits()` is reusable for any grid represented as wall bits.
  - `path_to_moves()` converts a cell path into `N/S/E/W` instructions.

- **Terminal UI components** (`ui/`)
  - `menu.py`, `option.py`, `game.py` can be reused as a base for other curses-based UIs.
  - `symbol.py` provides a simple theme system for rendering.

---

## mazegen-1.0.0.tar.gz module

To rebuild the .gz file you can use the command "python3 -m build".
To install and use the .gz file later you can use the command "make install".
It contains the Maze class that has all methods required to build the randomly generated maze.

---

## Team and project management (required)

### Team members & roles
- **ssayada and Avally**
  - Maze generation logic & file format (hex encoding) by Avally
  - Project packaging & Makefile tooling by Avally
  - TUI integration (menu/options/game screens) by Ssayada
  - A\* solver integration and path visualization by Ssayada
  - Bonuses by Ssayada


### Planning (anticipated vs actual)
- Initial plan:
  - Implement config parsing → maze generation → display in terminal as ASCII symbols.
- Evolution:
  - Implement curses for displays
  - Added options screen (colors/themes, perfect/imperfect, dimensions).
  - Added A\* solver and path visualization toggle (`P`).
  - Added regeneration workflow (`R`) and config rewrite.

### What worked well / what could be improved
**Worked well**
- Clear separation between generation (`maze_gen/`), solving (`solver.py`) and rendering (`ui/`).
- Fast iteration thanks to Makefile commands (`install`, `run`, `lint`, etc.).

**Could be improved**
- Add automated tests for config parsing, maze validity, and solver correctness.
- Improve documentation of the hex bit layout (N/E/S/W mapping) in the code and README.
- Add CI (lint + type-check) and pre-commit hooks.

### Tools used
- **Python** + **curses** for terminal UI
- **pydantic** for config validation
- **mypy** for type checking
- **flake8** for linting
- **Makefile** for common commands

---

## Resources

### References (topic)
- Curses (terminal UI): official Python documentation
- A\* pathfinding: standard algorithm references (grid + Manhattan heuristic)
- Maze generation techniques: depth-first/backtracking family of approaches

### AI usage (required)
- AI was used to **draft and structure this README.md and the docstrings** according to the provided 42 requirements (sections, wording, checklists).
- No AI-generated code was added automatically to the repository as part of writing this README.

---