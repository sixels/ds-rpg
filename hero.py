from typing import override

from backpack import Backpack
from belt import Belt
from entity import Entity
from item import Item
from item import ItemType


class Hero(Entity):
    name: str
    base_health: int
    current_health: int
    base_attack: float
    backpack: Backpack
    belt: Belt
    equipped_item: Item | None

    def __init__(
        self,
        name: str,
        base_health: int,
        base_attack: float,
        belt_size: int,
        belt_max_weight: float,
    ):
        self.name = name
        self.base_health = base_health
        self.current_health = base_health
        self.base_attack = base_attack
        self.backpack = Backpack()
        self.belt = Belt(size=belt_size, max_weight=belt_max_weight)
        self.equipped_item = None

    def store_item_in_belt(self, index: int, item: Item) -> bool:
        """Insere um item no cinto na posição especificada. Retorna True se a inserção for bem-sucedida, False se a posição estiver ocupada ou o peso exceder o máximo."""
        return self.belt.insert_item_on_empty_slot(self.equipped_item)
    

    def store_item_in_backpack(self, item: Item) -> bool:
        """Insere um item na mochila. Retorna True se a inserção for bem-sucedida, False caso contrário."""
        return self.backpack.insert_item(self.equipped_item)

    def store_equipped_item_in_belt(self, index: int) -> bool:
        """Armazena o item equipado no cinto, se possível."""
        # Dica: use o método store_item_in_belt e depois desquipe o item equipado
        if self.store_item_in_belt == True:
            self.equipped_item == None
        else:
            print(f"Não é possível guardar {self.equipped_item.name} pois não há espaço disponível no cinto")

    def store_equipped_item_in_backpack(self) -> bool:
        """Armazena o item equipado na mochila, se possível."""
        # Dica: use o método store_item_in_backpack e depois desquipe o item equipado
        if self.store_equipped_item_in_backpack == True:
            self.equipped_item = None
        else:
            print(f"Não é possível guardar {self.equipped_item.name} pois não há espaço disponível na mochila")

    def use_item_from_belt(self, index: int) -> bool:
        """
        Usa um item do cinto.
        Se for item do tipo Poção, restaura a vida do herói.
        Se for item do tipo Arma, equipa o item.

        Retorna True se o uso for bem-sucedido, False caso contrário.
        """
        
        if self.belt.items[index].type == ItemType.WEAPON : 
            self.equipped_item = self.belt.items[index]
            return True
        elif self.belt.items[index].type == ItemType.POTION:
            self.current_health += self.belt.items[index].healing_amount
    

    def use_item_from_backpack(self) -> bool:
        """
        Usa o item do topo da mochila.
        Se for item do tipo Poção, restaura a vida do herói.
        Se for item do tipo Arma, equipa o item.

        Retorna True se o uso for bem-sucedido, False caso contrário.
        """
        pass

    @override
    def get_total_health(self) -> int:
        return self.base_health
        

    @override
    def get_current_health(self) -> int:
        return self.current_health

    @override
    def take_damage(self, damage: int):
        self.current_health -= damage

    @override
    def attack(self, other: Entity) -> int:
       attack_total = self.equipped_item.do_damage(other.type)
       other.take_damage(attack_total)
       return attack_total
        
