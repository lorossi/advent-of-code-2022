from math import inf


def char_to_height(c: str) -> int:
    if c == "S":
        c = "a"
    elif c == "E":
        c = "z"

    if ord(c) >= ord("a"):
        # uppercase
        return ord(c) - ord("a")

    return ord(c) - ord("A") + 26


def find_char(grid: str, c: str) -> tuple[int, int]:
    for y, line in enumerate(grid.splitlines()):
        for x, char in enumerate(line):
            if char == c:
                return (x, y)


def find_all_chars(grid: str, c: str) -> list[tuple[int, int]]:
    out = []
    for y, line in enumerate(grid.splitlines()):
        for x, char in enumerate(line):
            if char == c:
                out.append((x, y))

    return out


def parse_input() -> str:
    with open("input", "r") as f:
        text = f.read()

    return text


def parse_grid(text: str) -> tuple[list[list[int]], tuple[int, int], tuple[int, int]]:
    lines = text.splitlines()
    h = len(lines)
    w = len(lines[0])

    height_map = [[0 for _ in range(w)] for _ in range(h)]

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            height_map[y][x] = char_to_height(c)

    start = find_char(text, "S")
    end = find_char(text, "E")

    return height_map, start, end


def find_path(
    grid: list[list[int]], start: tuple[int, int], end: tuple[int, int]
) -> list[tuple[int, int]]:
    w = len(grid[0])
    h = len(grid)

    dist = [[inf for _ in range(w)] for _ in range(h)]
    prev = [[None for _ in range(w)] for _ in range(h)]

    dist[start[1]][start[0]] = 0
    q = [start]

    while q:
        closest = min(q, key=lambda p: dist[p[1]][p[0]])
        q.remove(closest)

        if closest == end:
            break

        x, y = closest

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if dx + x < 0 or dx + x >= w:
                continue
            if dy + y < 0 or dy + y >= h:
                continue

            # calculate height difference
            dh = grid[y + dy][x + dx] - grid[y][x]
            # # max height difference is 1
            if dh > 1:
                continue

            alt = dist[y][x] + 1
            if alt < dist[dy + y][dx + x]:
                dist[dy + y][dx + x] = alt
                prev[dy + y][dx + x] = closest
                q.append((dx + x, dy + y))

    path = []
    current = end
    while current != start:
        if current is None:
            return None

        path.append(current)
        current = prev[current[1]][current[0]]

    return path


def part_one() -> int:
    in_file = parse_input()
    grid, start, end = parse_grid(in_file)
    path = find_path(grid, start, end)
    return len(path)


def part_two() -> int:
    in_file = parse_input()
    grid, _, end = parse_grid(in_file)
    starts = find_all_chars(in_file, "S")
    starts.extend(find_all_chars(in_file, "a"))

    best = inf
    for start in starts:
        path = find_path(grid, start, end)
        if path is not None and len(path) < best:
            best = len(path)

    return best


def main() -> None:
    print(f"Part one: {part_one()}")
    print(f"Part two: {part_two()}")


if __name__ == "__main__":
    main()
