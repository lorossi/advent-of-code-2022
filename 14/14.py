from enum import Enum
from math import inf


class Cell(Enum):
    AIR = "."
    SAND = "o"
    ROCK = "#"


def parse_input(part_two: bool = False) -> list[list[Cell]]:
    with open("input", "r") as f:
        text = f.read()

    x0 = 500
    x1 = -inf
    y0 = 0
    y1 = -inf

    points = []

    for line in text.splitlines():
        current_line = []
        coords = line.split(" -> ")
        for c in coords:
            x, y = map(int, c.split(","))
            x0 = min(x0, x)
            x1 = max(x1, x)
            y0 = min(y0, y)
            y1 = max(y1, y)
            current_line.append((x, y))
        points.append(current_line)

    w = x1 - x0 + 1
    h = y1 - y0 + 1
    grid = [[Cell.AIR for _ in range(w)] for _ in range(h)]

    for line in points:
        for i in range(1, len(line)):
            line_x0 = line[i - 1][0]
            line_y0 = line[i - 1][1]
            line_x1 = line[i][0]
            line_y1 = line[i][1]

            if line_x0 == line_x1:
                for y in range(min(line_y0, line_y1), max(line_y0, line_y1) + 1):
                    grid[y - y0][line_x0 - x0] = Cell.ROCK
            else:
                for x in range(min(line_x0, line_x1), max(line_x0, line_x1) + 1):
                    grid[line_y0 - y0][x - x0] = Cell.ROCK

    if part_two:
        grid.append([Cell.AIR for _ in range(w)])
        grid.append([Cell.ROCK for _ in range(w)])

    return grid, 500 - x0, 0


def print_grid(grid: list[list[Cell]]):
    print("\033c", end="")

    for row in grid:
        print("".join(c.value for c in row))


def next_move(grid: list[list[Cell]], x: int, y: int) -> tuple[int | None, int | None]:
    if y + 1 >= len(grid):
        return None, x

    if grid[y + 1][x] == Cell.AIR:
        return x, y + 1

    if x == 0:
        return y, None
    if grid[y + 1][x - 1] == Cell.AIR:
        return x - 1, y + 1

    if x == len(grid[0]) - 1:
        return y, None
    if grid[y + 1][x + 1] == Cell.AIR:
        return x + 1, y + 1

    return x, y


def add_columns(grid: list[list[Cell]]):
    for y, row in enumerate(grid):
        if y == len(grid) - 1:
            n = Cell.ROCK
        else:
            n = Cell.AIR

        row.append(n)
        row.insert(0, n)


def part_one() -> int:
    grid, x0, y0 = parse_input()
    fallen_out = False

    count = 0

    while not fallen_out:
        count += 1
        particle = (x0, y0)
        falling = True

        while falling:
            grid[particle[1]][particle[0]] = Cell.SAND

            new_particle = next_move(grid, particle[0], particle[1])

            if any(x is None for x in new_particle):
                grid[particle[1]][particle[0]] = Cell.AIR
                count -= 1
                falling = False
                fallen_out = True
            elif new_particle == particle:
                falling = False
            else:
                grid[particle[1]][particle[0]] = Cell.AIR
                grid[new_particle[1]][new_particle[0]] = Cell.SAND

                particle = new_particle

    return count


def part_two() -> int:
    grid, x0, y0 = parse_input(part_two=True)
    count = 0
    complete = False

    while not complete:
        count += 1
        particle = (x0, y0)

        if grid[y0][x0] == Cell.SAND:
            complete = True
            count -= 1
            break

        falling = True
        while falling:
            grid[particle[1]][particle[0]] = Cell.SAND
            new_particle = next_move(grid, particle[0], particle[1])

            if new_particle[1] is None:
                add_columns(grid)
                x0 += 1
                particle = (particle[0] + 1, particle[1])
                continue

            if new_particle[0] is None or new_particle == (None, None):
                falling = False
            elif new_particle == particle:
                falling = False
            else:
                grid[particle[1]][particle[0]] = Cell.AIR
                grid[new_particle[1]][new_particle[0]] = Cell.SAND

                particle = new_particle

    return count


def main():
    print(f"Part one: {part_one()}")
    print(f"Part two: {part_two()}")


if __name__ == "__main__":
    main()
