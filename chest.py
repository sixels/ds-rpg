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
                item.rarity.weight -= (
                    rarity.weight * 0.3 * (rarity_order_value - item_order_value)
                )
                item.rarity.weight = max(item.rarity.weight, 0)

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
