from dataclasses import dataclass


@dataclass(frozen=True)
class GameSettings:
    ALERT_THRESHOLD: int = 4
    ALERT_MOVE: int = 2
    ALERT_DRILL: int = 4
    ALERT_WRONGCODE: int = 3
    CAMS_OFF_MOVES: int = 10
    CAMS_OFF_MOVES_FUSE: int = 5
    KEYPAD_LOCK_MOVES: int = 3
    PICK_DURABILITY: int = 3
    LOOT_NOISE: int = 1
    DISGUISE_MOVES: int = 6
    PATROL_START_MOVES: int = 15
    PATROL_ALERT_PER_MOVE: int = 1

HARD = GameSettings()
