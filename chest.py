from typing import Optional
from item import Item
from rarity import (
    RARITY_COMMON,
    RARITY_EPIC,
    RARITY_LEGENDARY,
    RARITY_RARE,
    RARITY_UNCOMMON,
    Rarity,
)
import copy
import rng


class Chest:
    rarity: Rarity
    items: list[Optional["ChestItem"]]

    def __init__(self, rarity: Rarity):
        from globals import GAME_ITEMS

        self.rarity = rarity

        # Gerar itens aleatórios com base na raridade
        n_items = rng.random_range(1, 3)
        self.items = []
        possible_items = [copy.deepcopy(item) for item in GAME_ITEMS]

        for item in possible_items:
            item_order_value = rarity_order(item.rarity)
            rarity_order_value = rarity_order(self.rarity)

            if rarity_order_value > item_order_value:
                new_weight = rarity.weight - (
                    rarity.weight * 0.3 * (rarity_order_value - item_order_value)
                )
                item.rarity.weight = max(new_weight, 0)

        for _ in range(n_items):
            item = rng.pick_random_item(possible_items)
            if item:
                self.items.append(ChestItem(self, item, len(self.items)))

    def list_itens(self) -> list["ChestItem"]:
        """Retorna uma lista dos itens contidos no baú."""
        return list(filter(lambda x: x is not None, self.items))


class ChestItem:
    __chest: Chest | None
    __item: Item | None
    __index: int

    def __init__(self, chest: Chest, item: Item, index: int):
        self.__chest = chest
        self.__item = item
        self.__index = index

    def pick_item(self) -> Item | None:
        """Remove o item do baú, retornando um Item."""
        if self.__chest is None:
            return None

        item = self.__item

        self.__chest.items[self.__index] = None
        self.__chest = None
        self.__item = None

        return item

    def view_item(self) -> Item | None:
        """Retorna o item sem removê-lo do baú."""
        return self.__item

    def name(self) -> str:
        """Retorna o nome do item."""
        if self.__item is not None:
            return self.__item.name
        return ""


def generate_common_chest() -> Chest:
    """Gera um baú comum com itens aleatórios."""
    chest = Chest(RARITY_COMMON)
    # Adicionar lógica para gerar itens comuns
    return chest


def generate_uncommon_chest() -> Chest:
    """Gera um baú incomum com itens aleatórios."""
    chest = Chest(RARITY_UNCOMMON)
    # Adicionar lógica para gerar itens incomuns
    return chest


def generate_rare_chest() -> Chest:
    """Gera um baú raro com itens aleatórios."""
    chest = Chest(RARITY_RARE)
    # Adicionar lógica para gerar itens raros
    return chest


def generate_epic_chest() -> Chest:
    """Gera um baú épico com itens aleatórios."""
    chest = Chest(RARITY_EPIC)
    # Adicionar lógica para gerar itens épicos
    return chest


def generate_legendary_chest() -> Chest:
    """Gera um baú lendário com itens aleatórios."""
    chest = Chest(RARITY_LEGENDARY)
    # Adicionar lógica para gerar itens lendários
    return chest


def generate_random_chest() -> Chest:
    """Gera um baú com raridade aleatória."""

    rarity = rng.pick_random_rarity(
        [
            RARITY_COMMON,
            RARITY_UNCOMMON,
            RARITY_RARE,
            RARITY_EPIC,
            RARITY_LEGENDARY,
        ]
    )

    return Chest(rarity)


def rarity_order(rarity: Rarity) -> int:
    if rarity.type == RARITY_COMMON.type:
        return 0
    elif rarity.type == RARITY_UNCOMMON.type:
        return 1
    elif rarity.type == RARITY_RARE.type:
        return 2
    elif rarity.type == RARITY_EPIC.type:
        return 3
    elif rarity.type == RARITY_LEGENDARY.type:
        return 4
    raise ValueError(f"Raridade desconhecida: {rarity.type}")


if __name__ == "__main__":
    # Testando a geração de baús
    common_chest = generate_common_chest()
    print(
        f"Baú Comum: {[item.view_item().rarity.type.value for item in common_chest.list_itens()]}"
    )

    uncommon_chest = generate_uncommon_chest()
    print(
        f"Baú Incomum: {[item.view_item().rarity.type.value for item in uncommon_chest.list_itens()]}"
    )

    rare_chest = generate_rare_chest()
    print(
        f"Baú Raro: {[item.view_item().rarity.type.value for item in rare_chest.list_itens()]}"
    )

    epic_chest = generate_epic_chest()
    print(
        f"Baú Épico: {[item.view_item().rarity.type.value for item in epic_chest.list_itens()]}"
    )

    legendary_chest = generate_legendary_chest()
    print(
        f"Baú Lendário: {[item.view_item().rarity.type.value for item in legendary_chest.list_itens()]}"
    )
    random_chest = generate_random_chest()
    print(
        f"Baú Aleatório: {[item.view_item().rarity.type.value for item in random_chest.list_itens()]}"
    )
    assert len(random_chest.list_itens()) > 0, "O baú aleatório deve conter itens."
    print("Todos os testes de baús passaram com sucesso!")
