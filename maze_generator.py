import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

DIRECTIONS: dict[int, tuple[int, int, int]] = {
    NORTH: (0, -1, SOUTH),
    EAST:  (1, 0, WEST),
    SOUTH: (0, 1, NORTH),
    WEST:  (-1, 0, EAST),
}

PATTERN_42: list[tuple[int, int]] = [
    (0, 0),
    (0, 1),
    (0, 2), (1, 2), (2, 2),
    (2, 3),
    (2, 4),
    (4, 0), (5, 0), (6, 0),
    (6, 1),
    (4, 2), (5, 2), (6, 2),
    (4, 3),
    (4, 4), (5, 4), (6, 4),
]


class MazeGenerator:
    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        if width < 2 or height < 2:
            raise ValueError("Dimensões do labirinto devem ser no mínimo 2x2.")
        ex, ey = entry
        xx, xy = exit_pos
        if not (0 <= ex < width and 0 <= ey < height):
            raise ValueError(f"Entrada {entry} fora dos limites do labirinto.")
        if not (0 <= xx < width and 0 <= xy < height):
            raise ValueError(
                f"Saída {exit_pos} fora dos limites do labirinto."
            )
        if entry == exit_pos:
            raise ValueError("Entrada e saída devem ter coordenadas distintas")
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_pos = exit_pos
        self.perfect = perfect
        self.rng = random.Random(seed) if seed is not None else random.Random()
        self.maze: list[list[int]] = [
            [15 for _ in range(width)] for _ in range(height)
        ]
        self.warnings: list[str] = []

    def _remove_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy, opposite_wall = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.maze[y][x] &= ~direction
            self.maze[ny][nx] &= ~opposite_wall

    def _restore_wall(self, x: int, y: int, direction: int) -> None:
        dx, dy, opposite_wall = DIRECTIONS[direction]
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.width and 0 <= ny < self.height:
            self.maze[y][x] |= direction
            self.maze[ny][nx] |= opposite_wall

    def _get_unvisited_neighbors(
        self, x: int, y: int, visited: set[tuple[int, int]]
    ) -> list[tuple[int, int, int]]:
        neighbors: list[tuple[int, int, int]] = []
        for direction, (dx, dy, _) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                if (nx, ny) not in visited:
                    neighbors.append((nx, ny, direction))
        return neighbors

    def _get_pattern_42_cells(self) -> set[tuple[int, int]]:
        self.warnings.clear()
        if self.width < 11 or self.height < 9:
            self.warnings.append(
                "Warning: Maze dimensions too small to draw '42' pattern."
            )
            return set()
        offset_x = (self.width // 2) - 3
        offset_y = (self.height - 5) // 2
        blocked: set[tuple[int, int]] = {
            (offset_x + dx, offset_y + dy) for dx, dy in PATTERN_42
        }
        if self.entry in blocked or self.exit_pos in blocked:
            print("Aviso: Entrada/saída conflita com o padrão '42'.")
            return set()
        return blocked

    def _generate_perfect_maze(
        self, blocked: set[tuple[int, int]] | None = None
    ) -> None:
        visited: set[tuple[int, int]] = set(blocked) if blocked else set()
        start_x, start_y = self.entry
        visited.add((start_x, start_y))
        stack: list[tuple[int, int]] = [(start_x, start_y)]
        while stack:
            curr_x, curr_y = stack[-1]
            neighbors = self._get_unvisited_neighbors(curr_x, curr_y, visited)
            if neighbors:
                nx, ny, direction = self.rng.choice(neighbors)
                self._remove_wall(curr_x, curr_y, direction)
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

    def _has_open_3x3(self) -> bool:
        for by in range(self.height - 2):
            for bx in range(self.width - 2):
                all_open = True
                for r in range(by, by + 3):
                    for c in range(bx, bx + 2):
                        if self.maze[r][c] & EAST:
                            all_open = False
                            break
                    if not all_open:
                        break
                if not all_open:
                    continue
                for r in range(by, by + 2):
                    for c in range(bx, bx + 3):
                        if self.maze[r][c] & SOUTH:
                            all_open = False
                            break
                    if not all_open:
                        break
                if all_open:
                    return True
        return False

    def _make_imperfect(self, blocked: set[tuple[int, int]]) -> None:
        dead_end_values = {7, 11, 13, 14}
        coords = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in blocked
        ]
        for _ in range(3):
            self.rng.shuffle(coords)
            for x, y in coords:
                if self.maze[y][x] in dead_end_values:
                    candidates: list[int] = []
                    for direction, (dx, dy, _) in DIRECTIONS.items():
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < self.width
                            and 0 <= ny < self.height
                            and (nx, ny) not in blocked
                            and (self.maze[y][x] & direction)
                        ):
                            candidates.append(direction)
                    self.rng.shuffle(candidates)
                    for direction in candidates:
                        self._remove_wall(x, y, direction)
                        if self._has_open_3x3():
                            self._restore_wall(x, y, direction)
                        else:
                            break
        extra_openings = max(3, (self.width * self.height) // 7)
        opened = 0
        self.rng.shuffle(coords)
        for x, y in coords:
            if opened >= extra_openings:
                break
            directions = list(DIRECTIONS.keys())
            self.rng.shuffle(directions)
            for direction in directions:
                dx, dy, _ = DIRECTIONS[direction]
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.width
                    and 0 <= ny < self.height
                    and (nx, ny) not in blocked
                    and (self.maze[y][x] & direction)
                ):
                    self._remove_wall(x, y, direction)
                    if self._has_open_3x3():
                        self._restore_wall(x, y, direction)
                    else:
                        opened += 1
                        break

    def generate(self) -> list[list[int]]:
        self.maze = [
            [15 for _ in range(self.width)] for _ in range(self.height)
        ]
        blocked_cells = self._get_pattern_42_cells()
        self._generate_perfect_maze(blocked=blocked_cells)
        if not self.perfect:
            self._make_imperfect(blocked=blocked_cells)
        return self.maze
