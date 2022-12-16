import enum
from copy import deepcopy
from functools import cmp_to_key
from json import loads


class Result(enum.IntEnum):
    CORRECT = 1
    INCORRECT = -1
    UNKNOWN = 0


def compare(a: list[int] | int, b: list[int] | int) -> Result:
    if isinstance(a, int) and isinstance(b, int):
        if a < b:
            return Result.CORRECT
        if a > b:
            return Result.INCORRECT
        return Result.UNKNOWN

    if isinstance(a, int) and isinstance(b, list):
        return compare([a], b)

    if isinstance(a, list) and isinstance(b, int):
        return compare(a, [b])

    if isinstance(a, list) and isinstance(b, list):
        while a and b:
            if (result := compare(a.pop(0), b.pop(0))) != Result.UNKNOWN:
                if result == Result.CORRECT:
                    return Result.CORRECT
                return Result.INCORRECT

        if a and not b:
            return Result.INCORRECT

        if not a and not b:
            return Result.UNKNOWN

    return Result.CORRECT


def compare_copy(a: list[int] | int, b: list[int] | int) -> Result:
    aa = deepcopy(a)
    bb = deepcopy(b)

    return compare(aa, bb)


def parse_input(part_two=False) -> list[tuple[list[int], list[int]]]:
    with open("input", "r") as f:
        text = f.read()

    out = []
    groups = text.split("\n\n")

    for group in groups:
        lines = group.splitlines()

        if part_two:
            out.extend([loads(x) for x in lines])
        else:
            out.append([loads(x) for x in lines])

    return out


def part_one() -> int:
    groups = parse_input()
    answer = 0
    for x, group in enumerate(groups):
        if compare(*group) == Result.CORRECT:
            answer += 1 + x

    return answer


def part_two() -> int:
    # sort the groups
    groups = parse_input(part_two=True)
    groups.append([[2]])
    groups.append([[6]])

    groups.sort(key=cmp_to_key(compare_copy), reverse=True)

    answer = 1
    for x, group in enumerate(groups):
        if group == [[2]] or group == [[6]]:
            answer *= x + 1

    return answer


def main() -> None:
    print(f"Part one: {part_one()}")
    print(f"Part two: {part_two()}")


if __name__ == "__main__":
    main()
