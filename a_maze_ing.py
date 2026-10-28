import sys
import random
from maze_generator import MazeGenerator
from maze_display import render_maze, Clr
from maze_solver import (
    bfs_maze,
    reconstruct_maze_path,
    path_to_directions
)


def read_config(filename: str) -> dict[str, str]:

    config: dict[str, str] = {}

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            config[key.strip()] = value.strip()

    return config


def parse_dimensions(
    config: dict[str, str]
) -> tuple[int, int]:

    width_conf: int = int(config["WIDTH"])
    height_conf: int = int(config["HEIGHT"])

    return width_conf, height_conf


def parse_coordinates(
        config: dict[str, str],
        key: str
) -> tuple[int, int]:
    temp: str = config[key]
    coordinate_x, coordinate_y = temp.split(',')
    return int(coordinate_x), int(coordinate_y)


def parse_perfect(config: dict[str, str]) -> bool:
    perfect: str = config["PERFECT"].lower()

    if perfect in ("true", "false"):
        if perfect == "true":
            return True
        return False
    raise ValueError("Invalid PERFECT value")


def parse_seed(config: dict[str, str]) -> int | None:
    seed = config.get("SEED")
    if seed is None or seed == "":
        return None
    if not seed.isdigit():
        raise ValueError("Invalid SEED value")
    return int(seed)


def validate_config(
    width: int,
    height: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int]
) -> None:

    if width <= 0 or height <= 0:
        raise ValueError("Invalid maze dimensions")

    if entry == exit_pos:
        raise ValueError("Invalid maze dimensions")

    entry_x, entry_y = entry
    exit_x, exit_y = exit_pos

    if not (0 <= entry_x < width and 0 <= entry_y < height):
        raise ValueError("Entry outside maze bounds")

    if not (0 <= exit_x < width and 0 <= exit_y < height):
        raise ValueError("Exit outside maze bounds")


def encode_row(row: list[int]) -> str:
    list_row: list[str] = []
    for cell in row:
        list_row.append(format(cell, "X"))
    return "".join(list_row)


def encode_maze(maze: list[list[int]]) -> str:
    cell_maze: list[str] = []
    for row in maze:
        cell_maze.append(encode_row(row))
    return "\n".join(cell_maze) + "\n"


def write_maze(
        filename: str,
        maze: list[list[int]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: str
) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        maze_co = encode_maze(maze)
        entry_x, entry_y = entry
        exit_x, exit_y = exit_pos
        file.write(maze_co)
        file.write("\n")
        file.write(f"{entry_x},{entry_y}\n")
        file.write(f"{exit_x},{exit_y}\n")
        file.write(f"{path}\n")


def run_menu(
    generator: MazeGenerator,
    output_file: str
) -> None:
    """Handle interactive maze visualization."""
    show_path = False
    wall_colors = [Clr.WHT, Clr.CYN, Clr.WYLW]
    color_index = 0

    maze = generator.generate()

    parents = bfs_maze(maze, generator.entry, generator.exit_pos)

    path = reconstruct_maze_path(parents, generator.exit_pos)

    directions = path_to_directions(path)

    write_maze(
        output_file, maze, generator.entry, generator.exit_pos, directions
    )

    while True:
        visible_path = path if show_path else []
        print("\033[2J\033[H", end="")
        print(
            render_maze(
                maze,
                generator.entry,
                generator.exit_pos,
                visible_path,
                wall_colors[color_index]
            )
        )
        if generator.warnings:
            for warn in generator.warnings:
                print(f"{Clr.RED}{warn}{Clr.RST}")

        print(f"{Clr.BOL}=== A-Maze-ing ==={Clr.RST}")
        print(
            "1. Re-generate a new maze\n"
            "2. Show / Hide the shortest path\n"
            "3. Rotate the wall colours\n"
            "4. Quit"
        )
        option = input(f"{Clr.GRN}Choice? (1-4): _ {Clr.RST}")
        if option == "1":
            generator.rng = random.Random()
            maze = generator.generate()
            parents = bfs_maze(maze, generator.entry, generator.exit_pos)
            path = reconstruct_maze_path(parents, generator.exit_pos)
            directions = path_to_directions(path)
            write_maze(
                output_file, maze,
                generator.entry, generator.exit_pos, directions
            )
        elif option == "2":
            show_path = not show_path
        elif option == "3":
            color_index = (color_index + 1) % len(wall_colors)
        elif option == "4":
            break
        else:
            input("Invalid option. Press Enter to continue...")


def main() -> int:
    """Read and validate the maze configuration."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return 1

    try:
        config = read_config(sys.argv[1])

        width, height = parse_dimensions(config)
        entry = parse_coordinates(config, "ENTRY")
        exit_pos = parse_coordinates(config, "EXIT")
        perfect = parse_perfect(config)
        seed = parse_seed(config)

        output_file = config["OUTPUT_FILE"]

        if not output_file:
            raise ValueError("OUTPUT_FILE cannot be empty")

        validate_config(width, height, entry, exit_pos)
        generator = MazeGenerator(
            width,
            height,
            entry,
            exit_pos,
            perfect,
            seed
        )
        run_menu(generator, output_file)

    except (OSError, ValueError, KeyError, UnicodeError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1
    
    run_menu(maze, entry, exit_pos, path)
    print("Configuration validated successfully!")
    print(f"Dimensions: {width}x{height}")
    print(f"Entry: {entry}")
    print(f"Exit: {exit_pos}")
    print(f"Perfect: {perfect}")
    print(f"Seed: {seed}")
    print(f"Output: {output_file}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
