import sys
from maze_generator import MazeGenerator
from maze_display import render_maze

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


def get_neighbors(
    maze: list[list[int]],
    x: int,
    y: int
) -> list[tuple[int, int]]:
    neighbors: list[tuple[int, int]] = []

    height = len(maze)
    width = len(maze[0])

    directions = [
        (0, -1, 1, 4),
        (1, 0, 2, 8),
        (0, 1, 4, 1),
        (-1, 0, 8, 2)
    ]

    for dx, dy, wall, opposite in directions:
        nx = x + dx
        ny = y + dy

        if not (0 <= nx < width and 0 <= ny < height):
            continue

        current = maze[y][x]
        neighbor = maze[ny][nx]

        if (current & wall) == 0 and (neighbor & opposite) == 0:
            neighbors.append((nx, ny))

    return neighbors


def bfs_maze(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int]
) -> dict[
    tuple[int, int],
    tuple[int, int] | None
]:
    """Find parents of reachable cells using BFS."""
    queue: list[tuple[int, int]] = [entry]
    visited: set[tuple[int, int]] = {entry}
    parents: dict[
        tuple[int, int],
        tuple[int, int] | None
    ] = {entry: None}

    while queue:
        current = queue.pop(0)

        if current == exit_pos:
            break

        x, y = current

        for neighbor in get_neighbors(maze, x, y):
            if neighbor not in visited:
                visited.add((neighbor))
                queue.append(neighbor)
                parents[neighbor] = current

    return parents


def reconstruct_maze_path(
    parents: dict[
        tuple[int, int],
        tuple[int, int] | None
    ],
    exit_pos: tuple[int, int]
) -> list[tuple[int, int]]:
    """Reconstruct a path using the BFS parent dictionary."""
    path: list[tuple[int, int]] = []

    if exit_pos not in parents:
        raise ValueError("Exit is unreachable")

    current: tuple[int, int] | None = exit_pos
    while current is not None:
        path.append(current)
        current = parents[current]
    path.reverse()
    return path


def path_to_directions(
    path: list[tuple[int, int]]
) -> str:
    directions: list[str] = []

    for i in range(len(path) - 1):
        x1, y1 = path[i]
        x2, y2 = path[i + 1]

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == -1:
            directions.append("N")
        elif dx == 1 and dy == 0:
            directions.append("E")
        elif dx == 0 and dy == 1:
            directions.append("S")
        elif dx == -1 and dy == 0:
            directions.append("W")
        else:
            raise ValueError(f"Invalid movement: ({dx}, {dy})")

    return "".join(directions)


def run_menu(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: list[tuple[int, int]]
) -> None:
    """Handle interactive maze visualization."""
    show_path = False

    while True:
        visible_path = path if show_path else []
        print(render_maze(maze, entry, exit_pos, visible_path))

        option = input("1 - Toggle path | 2 - Exit: ")

        if option == "1":
            show_path = not show_path
        elif option == "2":
            break
        else:
            print("Invalid option")


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
        maze = generator.generate()

        parents = bfs_maze(maze, entry, exit_pos)

        path = reconstruct_maze_path(parents, exit_pos)

        directions = path_to_directions(path)

        write_maze(output_file, maze, entry, exit_pos, directions)

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