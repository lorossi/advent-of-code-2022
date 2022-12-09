from __future__ import annotations


class Motion:
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

    @staticmethod
    def from_string(motion: str) -> Motion:
        return {
            "U": Motion.UP,
            "D": Motion.DOWN,
            "L": Motion.LEFT,
            "R": Motion.RIGHT,
        }[motion]

    @staticmethod
    def opposite(motion: Motion) -> Motion:
        return {
            Motion.UP: Motion.DOWN,
            Motion.DOWN: Motion.UP,
            Motion.LEFT: Motion.RIGHT,
            Motion.RIGHT: Motion.LEFT,
        }[motion]
