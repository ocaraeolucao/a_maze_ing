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

