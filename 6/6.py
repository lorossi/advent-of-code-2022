def n_different(data: str, n: int = 4) -> int:
    for i in range(4, len(data)):
        if len(set(data[i - n : i])) == n:
            return i


def load_input() -> str:
    with open("input") as f:
        return f.read()


def part_1(data: str) -> int:
    return n_different(data)


def part_2(data: str) -> int:
    return n_different(data, 14)


def main():
    data = load_input()
    print(f"Part 1: {part_1(data)}")
    print(f"Part 2: {part_2(data)}")


if __name__ == "__main__":
    main()
