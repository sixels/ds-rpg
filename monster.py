from enum import Enum
from typing import override
from health_bar import HealthBar

from entity import Entity


class MonsterType(Enum):
    """Enumeração para os tipos de monstros."""

    Undead = "Morto-vivo"
    Beast = "Besta"
    Demon = "Demônio"
    Human = "Humano"
    Vampire = "Vampiro"
    Spirit = "Espírito"
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
        self.current_health = self.base_health
        self.base_attack = base_attack
        self.level = level
        self.health_bar = HealthBar(self, color="red")

    @override
    def get_total_health(self) -> int:
        return self.base_health

    @override
    def get_current_health(self) -> int:
        return self.current_health

    @override
    def take_damage(self, damage: int):
        self.current_health = max(self.current_health - damage, 0)
        self.health_bar.update()

    @override
    def attack(self, other: Entity) -> int:
        total_attack = self.base_attack + (self.level * 2)
        other.take_damage(total_attack)
        return total_attack

