from enum import Enum


class RarityType(Enum):
    """Enumeração para os tipos de raridade."""

    Common = "Comum"
    Uncommon = "Incomum"
    Rare = "Raro"
    Epic = "Épico"
    Legendary = "Lendário"


class Rarity:
    type: RarityType
    weight: float

    def __init__(self, type: RarityType, weight: float):
        self.type = type
        self.weight = weight
