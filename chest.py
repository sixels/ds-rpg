from typing import Optional
from item import Item
from rarity import RarityType


class Chest:
    rarity: RarityType
    items: list[Optional["ChestItem"]]

    def __init__(self, rarity: RarityType):
        self.rarity = rarity

        # Gerar itens aleatórios com base na raridade
        self.items = []

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

    def get_item(self) -> Item | None:
        """Remove o item do baú, retornando um Item."""
        if self.__chest is None:
            return None

        item = self.__item

        self.__chest.items[self.__index] = None
        self.__chest = None
        self.__item = None

        return item
