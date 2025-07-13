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
    def get_total_health(self) -> int:
        return self.base_health
        

    @override
    def get_current_health(self) -> int:
        return self.current_health

    @override
    def take_damage(self, damage: int):
        self.base_health -= damage

    @override
    def attack(self, other: Entity) -> int:
        total_attack = self.base_attack + (self.level * 2)
        other.take_damage(total_attack)
        return total_attack


def espada_multiplier(target_monster_type: MonsterType) -> int:   
    if target_monster_type == MonsterType.Human or target_monster_type == MonsterType.Beast:
        return 2 
    else:
        return 1
        
def estaca_multiplier(target_monster_type: MonsterType) ->  int:   
    if target_monster_type == MonsterType.Vampire:
        return 2
    else:
        return 1 
        
def cajado_multiplier(target_monster_type: MonsterType) -> int:   
    if target_monster_type == MonsterType.Demon:
        return 2
    else:
        return 1
        
def machado_multiplier(target_monster_type: MonsterType) -> int:   
    if target_monster_type == MonsterType.Vampire or target_monster_type == MonsterType.Demon:
        return 1
    else:
        return 2


   