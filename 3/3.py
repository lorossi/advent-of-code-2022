def load_rucksack() -> list[tuple[set, set]]:
    rucksacks = []
    with open("input", "r") as f:
        for line in f:
            current = []
            current.append(set(line[len(line) // 2 :].strip()))
            current.append(set(line[: len(line) // 2].strip()))
            rucksacks.append(current)
    return rucksacks


def load_groups() -> list[tuple[set, set, set]]:
    groups = []
    with open("input", "r") as f:
        current = []
        for line in f:
            current.append(set(line.strip()))

            if len(current) == 3:
                groups.append(current)
                current = []

    return groups


def chr_to_val(c: str) -> int:
    if ord(c) > 96:
        # lowercase
        return ord(c) - 96
    # uppercase
    return ord(c) - 38


def part_1(rucksacks: list[tuple[set, set]]) -> int:
    return sum(chr_to_val(i) for r in rucksacks for i in r[0] & r[1])


def part_2(groups: list[tuple[set, set, set]]) -> int:
    return sum(chr_to_val(i) for g in groups for i in g[0] & g[1] & g[2])


if __name__ == "__main__":
    rucksacks = load_rucksack()
    print(f"Part 1: {part_1(rucksacks)}")
    groups = load_groups()
    print(f"Part 2: {part_2(groups)}")
