from item import Item


class Belt:
    items: list[Item | None]
    size: int
    max_weight: float
    current_weight: float

    def __init__(self, size: int, max_weight: float):
        self.items = [None for _ in range(size)]
        self.size = size
        self.max_weight = max_weight
        self.current_weight = 0.0

    def insert_item(self, index: int, item: Item) -> bool:
        """Insere um item no cinto na posição especificada. Retorna True se a inserção for bem-sucedida, False se a posição estiver ocupada ou o peso exceder o máximo."""
        if index < 0 or index >= self.size:
            return False

        if (
            self.items[index] is None
            and self.current_weight + item.weight <= self.max_weight
        ):
            self.items[index] = item
            return True
        return False

    def insert_item_on_empty_slot(self, item: Item) -> bool:
        """Insere um item no primeiro espaço vazio do cinto. Retorna True se a inserção for bem-sucedida, False se não houver espaço ou o peso exceder o máximo."""
        # dica: procure o primeiro espaço vazio e chame o método insert_item no indíce encontrado
        for index in range(self.size):
            if self.items[index] is None:
                return self.insert_item(index, item)
        return False

    def pick_item(self, index: int) -> Item | None:
        """Remove um item do cinto na posição especificada. Retorna o item removido ou None se a posição estiver vazia."""
        item = self.get_item(index)
        if item is not None:
            self.items[index] = None
        return item

    def get_item(self, index: int) -> Item | None:
        """Retorna o item na posição especificada ou None se a posição estiver vazia."""
        if index < 0 or index >= self.size:
            return None

        return self.items[index]
