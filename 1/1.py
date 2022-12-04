def group_input() -> list[int]:
    calories = []
    with open("input", "r") as f:
        current = 0
        for line in f:
            if line != "\n":
                current += int(line)
            else:
                calories.append(current)
                current = 0

    return sorted(calories, reverse=True)


def main():
    calories = group_input()
    print(f"Part 1: {calories[0]}")
    print(f"Part 2: {sum(calories[0:3])}")


if __name__ == "__main__":
    main()
