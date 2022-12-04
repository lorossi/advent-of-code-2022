from enum import IntEnum


class Move(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Outcome(IntEnum):
    LOSE = 0
    DRAW = 3
    WIN = 6


winner_map = {
    Move.ROCK: Move.SCISSORS,
    Move.PAPER: Move.ROCK,
    Move.SCISSORS: Move.PAPER,
}

loser_map = {v: k for k, v in winner_map.items()}


def winner(move_a: Move, move_b: Move) -> Outcome:
    if move_a == move_b:
        return Outcome.DRAW

    if winner_map.get(move_b) == move_a:
        return Outcome.WIN

    return Outcome.LOSE


def forced_move(move_a: Move, outcome: Outcome) -> Move:
    if outcome == Outcome.DRAW:
        return move_a

    if outcome == Outcome.WIN:
        return loser_map[move_a]
    elif outcome == Outcome.LOSE:
        return winner_map[move_a]

    raise ValueError(f"Invalid outcome {outcome} for move {move_a}")


def evaluate_round(move_a: Move, move_b: Move, part_1=True) -> int:
    if part_1:
        return winner(move_a, move_b) + move_b
    else:
        forced_outcome = {
            Move.ROCK: Outcome.LOSE,
            Move.PAPER: Outcome.DRAW,
            Move.SCISSORS: Outcome.WIN,
        }[move_b]
        player_move = forced_move(move_a, forced_outcome)
        return forced_outcome + player_move


def load_input() -> list[Move]:
    input_map = {
        "A": Move.ROCK,
        "B": Move.PAPER,
        "C": Move.SCISSORS,
        "X": Move.ROCK,
        "Y": Move.PAPER,
        "Z": Move.SCISSORS,
    }

    with open("input", "r") as f:
        return [[input_map[x] for x in line.strip().split(" ")] for line in f]


def part_1(moves: list[Move]) -> int:
    return sum(evaluate_round(*game_round) for game_round in moves)


def part_2(moves: list[Move]) -> int:
    return sum(evaluate_round(*game_round, part_1=False) for game_round in moves)


def main():
    rounds = load_input()
    print(f"Part 1: {part_1(rounds)}")
    print(f"Part 2: {part_2(rounds)}")


if __name__ == "__main__":
    main()
