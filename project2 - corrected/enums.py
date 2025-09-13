from enum import Enum, auto


class ExitType(Enum):
    BLOCKED = auto()
    FREE = auto()
    NEEDS = auto()
    EVENT = auto()
    LOCKED = auto()
