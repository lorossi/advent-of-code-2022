def load_grid() -> list[list[int]]:
    with open("input") as f:
        return [[int(c) for c in line.strip()] for line in f.readlines()]


def check_line(row: list[int]) -> list[int]:
    return [1 if x == 0 or h > max(row[:x]) else 0 for x, h in enumerate(row)]


def extract_col(grid: list[list[int]], x: int) -> list[int]:
    return [row[x] for row in grid]


def create_visible_map(grid: list[list[int]]) -> list[list[int]]:
    visible = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for y, row in enumerate(grid):
        from_left = check_line(row)
        from_right = check_line(row[::-1])[::-1]

        for x in range(len(visible)):
            visible[y][x] |= from_left[x] | from_right[x]

    for x in range(len(grid)):
        col = extract_col(grid, x)
        from_top = check_line(col)
        from_bottom = check_line(col[::-1])[::-1]

        for y in range(len(visible)):
            visible[y][x] |= from_top[y] | from_bottom[y]

    return visible


def max_distance(height: int, line: list[int]) -> int:
    dist = 0

    for h in line:
        dist += 1

        if h >= height:
            break

    return dist


def check_scene(grid: list[list[int]], x: int, y: int) -> int:
    height = grid[y][x]
    left = max_distance(height, grid[y][:x][::-1])
    right = max_distance(height, grid[y][x + 1 :])
    up = max_distance(height, extract_col(grid, x)[:y][::-1])
    down = max_distance(height, extract_col(grid, x)[y + 1 :])

    return left * right * up * down


def create_scene_map(grid: list[list[int]]) -> list[list[int]]:
    scene = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for y in range(len(grid)):
        for x in range(len(grid[0])):
            scene[y][x] = check_scene(grid, x, y)

    return scene


def part_one(grid: list[list[int]]) -> int:
    visible = create_visible_map(grid)
    return sum(sum(row) for row in visible)


def part_two(grid: list[list[int]]) -> int:
    scene = create_scene_map(grid)
    return max(max(row) for row in scene)


def main():
    grid = load_grid()
    print(f"Part one: {part_one(grid)}")
    print(f"Part two: {part_two(grid)}")


if __name__ == "__main__":
    main()
