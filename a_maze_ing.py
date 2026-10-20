import sys


def read_config(filename: str) -> dict[str, str]:
    """Read configuration values from a file."""
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
    seed = int(seed)
    return seed


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

    except (OSError, ValueError, KeyError, UnicodeError) as error:
        print(f"Configuration error: {error}", file=sys.stderr)
        return 1

    print("Configuration validated successfully!")
    print(f"Dimensions: {width}x{height}")
    print(f"Entry: {entry}")
    print(f"Exit: {exit_pos}")
    print(f"Perfect: {perfect}")
    print(f"Seed: {seed}")
    print(f"Output: {output_file}")
    print(format(10, "X"))

    return 0


if __name__ == "__main__":
    # sys.exit(main())

    maze = [
        [15, 10, 3, 0],
        [1, 2, 3, 4],
        [8, 9, 10, 11]
    ]
    write_maze(
        "teste.txt",
        maze,
        (0, 0),
        (1, 0),
        "E"
    )

