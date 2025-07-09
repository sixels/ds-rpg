from collections.abc import Callable
from enum import Enum

from monster import MonsterType
from rarity import Rarity

DamageMultiplierCallback = Callable[[MonsterType], float]


class ItemType(Enum):
    WEAPON = "Arma"
    POTION = "Poção"


class Item:
    name: str
    weight: float
    rarity: Rarity
    type: ItemType
    description: str = ""

    def __init__(
        self, name: str, description: str, type: ItemType, weight: float, rarity: Rarity
    ):
        self.name = name
        self.description = description
        self.type = type
        self.weight = weight
        self.rarity = rarity


class Weapon(Item):
    damage: int
    multiplier: DamageMultiplierCallback

    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        rarity: Rarity,
        damage: int,
        multiplier: DamageMultiplierCallback = lambda _: 1,  # retorna 1 por padrão
    ):
        super().__init__(name, description, ItemType.WEAPON, weight, rarity)
        self.damage = damage
        self.multiplier = multiplier

    def do_damage(self, monster_type: MonsterType) -> int:
        """Calcula o dano causado pela arma com base no tipo de monstro."""
        return int(self.damage * self.multiplier(monster_type))


class Potion(Item):
    healing_amount: int

    def __init__(
        self,
        name: str,
        description: str,
        weight: float,
        rarity: Rarity,
        healing_amount: int,
    ):
        super().__init__(name, description, ItemType.POTION, weight, rarity)
        self.healing_amount = healing_amount

    def do_healing(self) -> int:
        """Retorna a quantidade de cura fornecida pela poção."""
        return self.healing_amount
