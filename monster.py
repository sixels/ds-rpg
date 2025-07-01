from enum import Enum
from typing import override

from entity import Entity


class MonsterType(Enum):
    """Enumeração para os tipos de monstros."""

    Undead = "Morto-vivo"
    Beast = "Besta"
    Demon = "Demônio"
    Human = "Humano"
    Vampire = "Vampiro"
    # outros tipos que quiser adicionar


class Monster(Entity):
    name: str
    base_health: int
    current_health: int
    base_attack: int
    level: int
    type: MonsterType

    def __init__(
        self,
        name: str,
        type: MonsterType,
        base_health: int,
        base_attack: int,
        level: int,
    ):
        self.name = name
        self.type = type
        self.base_health = base_health
        self.base_attack = base_attack
        self.level = level

    @override
    def get_total_health(self) -> float:
        pass

    @override
    def get_current_health(self) -> float:
        pass

    @override
    def take_damage(self, damage: int):
        pass

    @override
    def attack(self, other: Entity) -> int:
        pass
