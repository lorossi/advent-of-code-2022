import re


def load_assignments() -> list[tuple]:
    assignments = []
    with open("input", "r") as f:
        for line in f:
            groups = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
            assignments.append(
                (int(groups[1]), int(groups[2]), int(groups[3]), int(groups[4]))
            )

    return assignments


def full_overlap(assignment: tuple[int, int, int, int]) -> bool:
    a, b, c, d = assignment
    return (a <= c and b >= d) or (c <= a and d >= b)


def partial_overlap(assignment: tuple[int, int, int, int]) -> bool:
    a, b, c, d = assignment
    return (a <= c and b >= c) or (c <= a and d >= a)


def part_1(assignments: list[tuple]) -> int:
    return sum(full_overlap(a) for a in assignments)


def part_2(assignments: list[tuple]) -> int:
    return sum(partial_overlap(a) for a in assignments)


def main():
    assignments = load_assignments()
    print(f"Part 1: {part_1(assignments)}")
    print(f"Part 2: {part_2(assignments)}")


if __name__ == "__main__":
    main()
