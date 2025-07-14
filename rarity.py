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


RARITY_COMMON = Rarity(RarityType.Common, 40.0)
RARITY_UNCOMMON = Rarity(RarityType.Uncommon, 30.0)
RARITY_RARE = Rarity(RarityType.Rare, 20.0)
RARITY_EPIC = Rarity(RarityType.Epic, 5.0)
RARITY_LEGENDARY = Rarity(RarityType.Legendary, 2.0)
