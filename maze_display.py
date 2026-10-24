class Clr:
    GRN = '\033[92m'
    RED = '\033[91m'
    BLU = '\033[35m'
    YLW = '\033[43m'
    RST = '\033[0m'


def render_north_walls(row: list[int]) -> str:
    result: str = ""

    for cell in row:
        if (cell & 1) == 0:
            result += "+   "
        else:
            result += "+---"

    return result + "+"


def render_side_walls(
    row: list[int],
    y: int,
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: list[tuple[int, int]]
) -> str:
    result: str = ""
    marker = ""

    for x, cell in enumerate(row):
        if (x, y) == entry:
            marker = f"{Clr.GRN} E {Clr.RST}"
        elif (x, y) == exit_pos:
            marker = f"{Clr.RED} S {Clr.RST}"
        elif cell == 15:
            marker = f"{Clr.YLW}   {Clr.RST}"
        elif (x, y) in path:
            marker = f"{Clr.BLU} X {Clr.RST}"
        else:
            marker = "   "

        if (cell & 8) != 0:
            result += f"|{marker}"
        else:
            result += f" {marker}"
    if (row[-1] & 2) != 0:
        result += "|"
    else:
        result += " "

    return result


def render_south_walls(row: list[int]) -> str:
    result: str = ""
    for cell in row:
        if (cell & 4) != 0:
            result += "+---"
        else:
            result += "+   "
    return result + "+"


def render_maze(
    maze: list[list[int]],
    entry: tuple[int, int],
    exit_pos: tuple[int, int],
    path: list[tuple[int, int]]
) -> str:
    """Render the complete maze in ASCII."""
    lines: list[str] = []

    for y, row in enumerate(maze):
        lines.append(render_north_walls(row))
        lines.append(render_side_walls(row, y, entry, exit_pos, path))

    lines.append(render_south_walls(maze[-1]))

    return "\n".join(lines) + "\n"


