import re
import copy


def load_input() -> tuple[list[str], list[dict]]:
    stacks = []
    moves = []

    empty_line = None

    with open("input") as f:
        lines = f.readlines()

    # find empty line
    for x, line in enumerate(lines):
        if not line.strip():
            empty_line = x
            break

    # get the number of stacks
    stacks_num = max(int(x) for x in lines[empty_line - 1].strip().split(" ") if x)
    stacks = [[] for _ in range(stacks_num)]

    # parse the initial state of the stacks
    for line in lines[: empty_line - 1]:
        for x in range(1, len(line) - 1, 4):
            if (c := line[x]) != " ":
                stacks[x // 4].insert(0, c)

    # parse the moves
    for line in lines[empty_line + 1 :]:
        groups = re.match(r"[a-z]+\s(\d+)\s[a-z]+\s(\d+)\s[a-z]+\s(\d+)", line).groups()
        moves.append(
            {
                "quantity": int(groups[0]),
                "from": int(groups[1]) - 1,
                "to": int(groups[2]) - 1,
            }
        )

    return stacks, moves


def apply_moves(stacks: list[str], moves: list[dict], part_2=False):
    for move in moves:
        from_stack = move["from"]
        to_stack = move["to"]

        if part_2:
            stacks[to_stack].extend(stacks[from_stack][-move["quantity"] :])
            stacks[from_stack] = stacks[from_stack][: -move["quantity"]]
        else:
            for _ in range(move["quantity"]):
                stacks[to_stack].append(stacks[from_stack].pop())


def part_1(stacks: list[str], moves: list[dict]):
    s = copy.deepcopy(stacks)
    apply_moves(s, moves)
    return "".join(x[-1] for x in s)


def part_2(stacks: list[str], moves: list[dict]):
    s = copy.deepcopy(stacks)
    apply_moves(s, moves, part_2=True)
    return "".join(x[-1] for x in s)


def main():
    stacks, moves = load_input()
    print(f"Part 1: {part_1(stacks, moves)}")
    print(f"Part 2: {part_2(stacks, moves)}")


if __name__ == "__main__":
    main()
