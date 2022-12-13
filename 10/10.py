from __future__ import annotations
from enum import Enum


class Opcode(Enum):
    NOP = "noop"
    ADD = "addx"


class Instruction:
    def __init__(self, opcode: Opcode, operand: int, duration: int) -> Instruction:
        self._opcode = opcode
        self._operand = operand
        self._duration = duration

    @staticmethod
    def fromString(s: str) -> Instruction:
        duration_map = {
            Opcode.NOP: 1,
            Opcode.ADD: 2,
        }
        str_opcode, *str_operand = s.split(" ")

        opcode = Opcode(str_opcode)
        operand = int(str_operand[0]) if str_operand else None

        return Instruction(
            opcode,
            operand,
            duration_map[Opcode(str_opcode)],
        )

    @property
    def opcode(self) -> str:
        return self._opcode

    @property
    def operand(self) -> int:
        return self._operand

    @property
    def duration(self) -> int:
        return self._duration


class CPU:
    def __init__(self) -> CPU:
        self._x = 1
        self._instructions = []
        self._screen = []

    def setInstructions(self, instructions: list[Instruction]) -> None:
        self._instructions = [i for i in instructions]

    def execute(self) -> int:
        count = 0

        for i in self._instructions:
            for _ in range(i.duration):
                x = count % 40
                y = count // 40

                if y >= len(self._screen):
                    self._screen.append([])

                if x in range(self._x - 1, self._x + 2):
                    self._screen[y].append("#")
                else:
                    self._screen[y].append(".")

                yield count
                count += 1

            match i.opcode:
                case Opcode.ADD:
                    self._x += i.operand

    @property
    def x(self) -> int:
        return self._x

    def __repr__(self) -> str:
        return "\n".join(["".join(line) for line in self._screen])


def load_instructions() -> list[Instruction]:
    with open("input", "r") as f:
        return [Instruction.fromString(line.strip()) for line in f.readlines()]


def part_one() -> int:
    cpu = CPU()
    cpu.setInstructions(load_instructions())
    total = 0
    for x in cpu.execute():
        if (x - 20) % 40 == 0:
            total += cpu.x * x

    return total


def part_two() -> None:
    cpu = CPU()
    cpu.setInstructions(load_instructions())
    for _ in cpu.execute():
        ...

    print(cpu)


def main() -> None:
    print(f"Part one: {part_one()}")
    print(f"Part two: {part_two()}")


if __name__ == "__main__":
    main()
