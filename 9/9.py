import re

from motions import Motion


def parse_motion(motion: str) -> list[Motion]:
    m = re.match(r"(\w) (\d+)", motion)

    if m:
        direction = Motion.from_string(m.group(1))
        distance = int(m.group(2))
        return [direction] * distance


def check_neighbours(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return (
        (head[0] == tail[0] and abs(head[1] - tail[1]) == 1)
        or (head[1] == tail[1] and abs(head[0] - tail[0]) == 1)
        or (head == tail)
    )


def check_diagonal(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return abs(head[0] - tail[0]) == 1 and abs(head[1] - tail[1]) == 1


def simulate_grid(head_movements: list[Motion]) -> set[tuple[int, int]]:
    head_positions = []

    x, y = 0, 0
    for motion in head_movements:
        x += motion[0]
        y += motion[1]
        head_positions.append((x, y))

    # x0 = min(h[0] for h in head_positions)
    # y0 = min(h[1] for h in head_positions)
    # w = max(h[0] for h in head_positions) - x0 + 1
    # h = max(h[1] for h in head_positions) - y0 + 1
    # grid = [[False for _ in range(w)] for _ in range(h)]

    visited = set()

    tail_position = (
        head_positions[0][0] - head_movements[0][0],
        head_positions[0][1] - head_movements[0][1],
    )

    visited.add(tail_position)

    for x in range(len(head_movements)):
        diagonal_movement = check_diagonal(head_positions[x], tail_position)
        neighbours = check_neighbours(head_positions[x], tail_position)

        if diagonal_movement or neighbours:
            continue

        tail_position = head_positions[x - 1]
        visited.add(tail_position)

        # grid[tail_position[1] - y0][tail_position[0] - x0] = True

        # for line in grid:
        #     print("".join("#" if x else "." for x in line))
        # print("\n\n", end="")

    return visited


def part_one(motions: list[Motion]) -> int:
    visited = simulate_grid(motions)
    return len(visited)


def parse_input() -> list[Motion]:
    motions = []
    with open("input") as f:
        for line in f:
            motions.extend(parse_motion(line))

    return motions


def main():
    motions = parse_input()
    print(f"Part one: {part_one(motions)}")
    # WRONG: 6092
    # COULD BE: 6087


if __name__ == "__main__":
    main()
