from enum import Enum


class ENodeStateColors(str, Enum):
    UNVISITED = "yellow"
    OPEN = "blue"
    CURRENT = "red"
    GOAL = "green"
    CLOSED = "gray"

    def color(self) -> str:
        return self.value