from typing import Optional
from chest import Chest
from item import Item
from monster import Monster


class Room:
    name: str
    exits: "Exits"
    dropped_items: list[Item]

    monster: Monster | None
    chest: Chest | None
    chest_opened: bool = False

    def __init__(self, name):
        self.name = name
        self.exits = Exits()
        self.dropped_items = []

        self.monster = None
        self.chest = None

    def set_exits(
        self,
        north: Optional["Room"] = None,
        south: Optional["Room"] = None,
        east: Optional["Room"] = None,
        west: Optional["Room"] = None,
    ):
        """Define as saídas da sala."""
        if north:
            north.exits.south = self
            self.exits.north = north
        if south:
            south.exits.north = self
            self.exits.south = south
        if east:
            east.exits.west = self
            self.exits.east = east
        if west:
            west.exits.east = self
            self.exits.west = west

    def add_item(self, item: Item):
        """Adiciona um item à lista de itens soltos na sala."""
        self.dropped_items.append(item)

    def remove_item(self, item: Item):
        """Remove um item da lista de itens soltos na sala."""
        if item in self.dropped_items:
            self.dropped_items.remove(item)

    def set_monster(self, monster: Monster):
        """Define o monstro da sala."""
        self.monster = monster

    def set_chest(self, chest: Chest):
        """Define o baú da sala."""
        self.chest = chest

    def get_exit(self, direction: str) -> Optional["Room"]:
        """Retorna a sala de saída na direção especificada."""
        if direction == "norte":
            return self.exits.north
        elif direction == "sul":
            return self.exits.south
        elif direction == "leste":
            return self.exits.east
        elif direction == "oeste":
            return self.exits.west
        else:
            return None


class Exits:
    north: Room | None = None
    south: Room | None = None
    east: Room | None = None
    west: Room | None = None
