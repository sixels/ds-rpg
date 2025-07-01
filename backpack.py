from item import Item


class Backpack:
    itens: list[Item]

    def __init__(self):
        self.itens = []

    def insert_item(self, item: Item) -> bool:
        """Insere um item no topo da mochila. Retorna True se a inserção for bem-sucedida, False caso contrário."""
        pass

    def list_items(self) -> list[Item]:
        """Retorna uma lista dos itens contidos na mochila."""
        return self.itens

    def pick_item(self) -> Item | None:
        """Remove um item do topo da mochila. Retorna o item removido ou None se a mochila estiver vazia."""
        pass

    def get_item(self) -> Item | None:
        """Retorna o item do topo da mochila ou None se a mochila estiver vazia."""
        pass
