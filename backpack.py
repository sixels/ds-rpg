from item import Item


class Backpack:
    max_itens: int
    items: list[Item]

    def __init__(self, max_itens: int = 10):
        self.items = []
        self.max_itens = max_itens

    def insert_item(self, item: Item) -> bool:
        """Insere um item no topo da mochila. Retorna True se a inserção for bem-sucedida, False caso contrário."""
        insertion_suceed: bool

        if len(self.items) < self.max_itens:
            self.items.append(item)
            insertion_suceed = True
        else:
            insertion_suceed = False

        return insertion_suceed

    def list_items(self) -> list[Item]:
        """Retorna uma lista dos itens contidos na mochila."""
        return self.items

    def pick_item(self) -> Item | None:
        """Remove um item do topo da mochila. Retorna o item removido ou None se a mochila estiver vazia."""
        return self.items.pop()

    def get_item(self) -> Item | None:
        """Retorna o item do topo da mochila ou None se a mochila estiver vazia."""
        if len(self.items) == 0:
            return None
        else:
            return self.items[-1]
