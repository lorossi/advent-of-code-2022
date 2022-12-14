from __future__ import annotations
import re
from functools import reduce


class Operation:
    def __init__(self, operator_str: str, const: int = None) -> Operation:
        operators_map = {
            "+": lambda a, b: a + b,
            "*": lambda a, b: a * b,
        }
        self._operator_str = operator_str

        self._operator = operators_map[operator_str]
        self._const = const

    def apply(self, a: int) -> int:
        if self._const is None:
            return int(self._operator(a, a))
        else:
            return int(self._operator(a, self._const))

    @staticmethod
    def from_string(s: str) -> Operation:
        g = re.match(r"\w+\s+= (old|\d+) ([+|*]) (old|\d+)", s)
        if not g:
            raise ValueError(f"Invalid operation string {s}")

        if g.group(3) != "old":
            const = int(g.group(3))
        else:
            const = None

        return Operation(g.group(2), const)

    @property
    def operator_str(self) -> str:
        return self._operator_str

    @property
    def const(self) -> int:
        return self._const


class Monkey:
    def __init__(
        self,
        operation: Operation,
        test: int,
        monkey_true_id: int,
        monkey_false_id: int,
    ) -> Monkey:
        self._operation = operation
        self._test = test
        self._monkey_true_id = monkey_true_id
        self._monkey_false_id = monkey_false_id

        self._inspected = 0
        self._inventory = []

        self._monkey_true = None
        self._monkey_false = None

    def setInventory(self, inventory: list[int]) -> None:
        self._inventory = [i for i in inventory]

    def addItem(self, item: int) -> None:
        self._inventory.append(item)

    def simulate(self) -> None:
        while len(self._inventory) > 0:
            self._inspected += 1
            item = self._operation.apply(self._inventory.pop(0)) // 3

            if item % self._test == 0:
                destination = self._monkey_true
            else:
                destination = self._monkey_false

            destination.addItem(item)

    def setDestinations(self, monkey_true: Monkey, monkey_false: Monkey) -> None:
        self._monkey_true = monkey_true
        self._monkey_false = monkey_false

    @classmethod
    def from_string(cls, s: str) -> Monkey:
        for line in s.splitlines():
            if g := re.match(r"\s+Starting items: (.+)", line):
                inventory = [int(x) for x in g.group(1).split(", ")]
            elif g := re.match(r"\s+Operation: (.+)", line):
                operation = Operation.from_string(g.group(1))
            elif g := re.match(r"\s+Test: divisible by (\d+)", line):
                test = int(g.group(1))
            elif g := re.match(r"\s+If true: throw to monkey (\d+)", line):
                test_true = int(g.group(1))
            elif g := re.match(r"\s+If false: throw to monkey (\d+)", line):
                test_false = int(g.group(1))

        m = cls(operation, test, test_true, test_false)
        m.setInventory(inventory)
        return m

    @property
    def monkey_true_id(self) -> int:
        return self._monkey_true_id

    @property
    def monkey_false_id(self) -> int:
        return self._monkey_false_id

    @property
    def inventory(self) -> list[str]:
        return self._inventory

    @property
    def inspected(self) -> int:
        return self._inspected


class ShortMonkey(Monkey):
    def simulate(self) -> None:
        while len(self._inventory) > 0:
            self._inspected += 1
            # item = self._inventory.pop(0)
            item = self._operation.apply(self._inventory.pop(0))

            if item % self._test == 0:
                destination = self._monkey_true
            else:
                destination = self._monkey_false

            destination.addItem(item % self._lcm)

    @property
    def operation(self) -> Operation:
        return self._operation

    @property
    def test(self) -> int:
        return self._test

    @property
    def lcm(self) -> int:
        return self._lcm

    @lcm.setter
    def lcm(self, value: int) -> None:
        self._lcm = value


def parse_monkeys(short: bool = False) -> list[Monkey] | list[ShortMonkey]:
    with open("input", "r") as f:
        text = f.read()

    monkeys = []
    prototype = Monkey if not short else ShortMonkey
    for m in text.split("\n\n"):
        monkeys.append(prototype.from_string(m))

    for m in monkeys:
        m.setDestinations(monkeys[m.monkey_true_id], monkeys[m.monkey_false_id])

    return monkeys


def part_one() -> int:
    monkeys = parse_monkeys()
    for _ in range(20):
        for m in monkeys:
            m.simulate()

    highest = sorted([m.inspected for m in monkeys], reverse=True)[:2]
    return highest[0] * highest[1]


def part_two(n=10000) -> int:
    monkeys = parse_monkeys(short=True)
    tests = [m.test for m in monkeys]
    lcm = reduce(lambda x, y: x * y, tests)
    for m in monkeys:
        m.lcm = lcm

    for _ in range(n):
        for m in monkeys:
            m.simulate()

    highest = sorted([m.inspected for m in monkeys], reverse=True)[:2]
    return highest[0] * highest[1]


def main() -> None:
    print(f"Part one: {part_one()}")
    print(f"Part two: {part_two()}")


if __name__ == "__main__":
    main()
