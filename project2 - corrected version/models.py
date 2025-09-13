from dataclasses import dataclass, field
from typing import Dict, List, Optional

from enums import ExitType


@dataclass
class Exit:
    target: str
    exit_type: ExitType
    requires: Optional[str] = None


@dataclass
class Room:
    key: str
    name: str
    short_desc: str
    long_desc: str
    exits: Dict[str, Exit] = field(default_factory=dict)
    items: List[str] = field(default_factory=list)
    visited: bool = False

    def describe(self) -> None:
        print(self.long_desc if not self.visited else self.short_desc)
        self.visited = True


@dataclass
class Player:
    location: str
    inventory: List[str] = field(default_factory=list)
    notes: int = 0
    has_loot: bool = False

    def has_item(self, item: str) -> bool:
        return any(i.lower() == item.lower() for i in self.inventory)

    def remove_item_case_insensitive(self, item: str) -> None:
        self.inventory = [i for i in self.inventory if i.lower() != item.lower()]
