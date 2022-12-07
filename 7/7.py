from entity import File, Folder, Command
from math import inf


def parse_commands() -> list:
    with open("input") as f:
        lines = f.readlines()

    commands = []
    for x, line in enumerate(lines):
        if line.startswith("$"):
            com = line[1:].strip()
            out = []
            x += 1

            while x < len(lines) and not lines[x].startswith("$"):
                out.append(lines[x].strip())
                x += 1

            commands.append(Command(com, out))

    return commands


def parse_ls(output: list[str]) -> list[File | Folder]:
    subtree = []

    for o in output:
        if o.startswith("dir"):
            subtree.append(Folder(o[4:], []))
        else:
            size, name = o.split(" ")
            subtree.append(File(name, int(size)))

    return subtree


def parse_input() -> Folder:
    commands = parse_commands()

    root = Folder("/", [])
    current_folder = None

    for c in commands:
        match c.command:
            case "cd":
                if not current_folder and c.args[0] == "/":
                    current_folder = root
                elif c.args[0] == "..":
                    current_folder = current_folder.parent
                else:
                    current_folder = current_folder.cd(c.args[0])

            case "ls":
                for e in parse_ls(c.output):
                    e.parent = current_folder
                    current_folder.append(e)

    return root


def part_one(current_folder: Folder, size=0) -> int:
    for entity in current_folder.subtree:
        if isinstance(entity, Folder):
            if entity.size < 100000:
                size += part_one(entity, entity.size)
            else:
                size += part_one(entity, 0)

    return size


def part_two(current_folder: Folder, to_free=None, best_size=inf) -> int:
    if not to_free:
        to_free = current_folder.size - 40000000

    for entity in current_folder.subtree:
        if isinstance(entity, Folder):
            if entity.size >= to_free and entity.size < best_size:
                best_size = entity.size

            best_size = part_two(entity, to_free, best_size)

    return best_size


def main():
    root = parse_input()
    print(f"Part 1: {part_one(root)}")
    print(f"Part 2: {part_two(root)}")


if __name__ == "__main__":
    main()
