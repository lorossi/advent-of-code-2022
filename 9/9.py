import re

from copy import deepcopy
from motions import Motion


def parse_motion(motion: str) -> list[Motion]:
    if not motion:
        []

    m = re.match(r"(\w) (\d+)", motion)

    if m:
        direction = Motion.from_string(m.group(1))
        distance = int(m.group(2))
        return [direction] * distance


def check_orthogonal_neighbours(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return (
        (head[0] == tail[0] and abs(head[1] - tail[1]) == 1)
        or (head[1] == tail[1] and abs(head[0] - tail[0]) == 1)
        or (head == tail)
    )


def check_diagonal_neighbour(head: tuple[int, int], tail: tuple[int, int]) -> bool:
    return abs(head[0] - tail[0]) == 1 and abs(head[1] - tail[1]) == 1


def minimize_distance(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    def limit(x: int) -> int:
        if x < 0 and x < -1:
            return -1
        if x > 0 and x > 1:
            return 1

        return x

    # return dx, dy
    return limit(head[0] - tail[0]), limit(head[1] - tail[1])


def simulate_movements(
    head_movements: list[Motion], k: int = 1, print_steps: bool = False
) -> set[tuple[int, int]]:
    head_positions = []

    x, y = 0, 0
    for move in head_movements:
        x += move[0]
        y += move[1]
        head_positions.append((x, y))

    if print_steps:
        x0 = min(pos[0] for pos in head_positions)
        y0 = min(pos[1] for pos in head_positions)
        w = max(pos[0] for pos in head_positions) - x0 + 1
        h = max(pos[1] for pos in head_positions) - y0 + 1

    visited = set()
    visited.add((0, 0))
    knots_positions = [(0, 0) for _ in range(k + 1)]
    old_knots_positions = deepcopy(knots_positions)

    for i in range(len(head_movements)):
        old_knots_positions = deepcopy(knots_positions)
        knots_positions[0] = (
            knots_positions[0][0] + head_movements[i][0],
            knots_positions[0][1] + head_movements[i][1],
        )

        for j in range(1, len(knots_positions)):
            diagonal = check_diagonal_neighbour(
                knots_positions[j - 1], knots_positions[j]
            )
            ortho = check_orthogonal_neighbours(
                knots_positions[j - 1], knots_positions[j]
            )

            if diagonal or ortho:
                continue

            if not ortho:
                dx, dy = minimize_distance(knots_positions[j - 1], knots_positions[j])
                knots_positions[j] = (
                    knots_positions[j][0] + dx,
                    knots_positions[j][1] + dy,
                )
            else:
                knots_positions[j] = old_knots_positions[j - 1]

            if j == k:
                visited.add(knots_positions[j])

        if print_steps:
            # print character to clean terminal
            print("\033[2J")
            # print character to move cursor to top left
            print("\033[0;0H")
            for y in range(h):
                for x in range(w):
                    if (x + x0, y + y0) == (0, 0):
                        print("s", end="")
                    elif (x + x0, y + y0) in knots_positions:
                        i = knots_positions.index((x + x0, y + y0))

                        if i == 0:
                            c = "H"
                        else:
                            c = str(i)

                        print(c, end="")
                    else:
                        print(".", end="")
                print()

            print()

            # print character to x, y
            for y in range(h):
                for x in range(w):
                    if (x + x0, y + y0) == (0, 0):
                        print("s", end="")
                    elif (x + x0, y + y0) in visited:
                        print("#", end="")
                    else:
                        print(".", end="")
                print()

            input()

    return visited


def part_one(motions: list[Motion]) -> int:
    visited = simulate_movements(motions)
    return len(visited)


def part_two(motions: list[Motion]) -> int:
    visited = simulate_movements(motions, k=9, print_steps=False)
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
    print(f"Part two: {part_two(motions)}")


if __name__ == "__main__":
    main()
