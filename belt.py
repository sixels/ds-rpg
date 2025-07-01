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

    def insert_item(index: int, item: Item) -> bool:
        """Insere um item no cinto na posição especificada. Retorna True se a inserção for bem-sucedida, False se a posição estiver ocupada ou o peso exceder o máximo."""
        pass

    def insert_item_on_empty_slot(item: Item) -> bool:
        """Insere um item no primeiro espaço vazio do cinto. Retorna True se a inserção for bem-sucedida, False se não houver espaço ou o peso exceder o máximo."""
        # dica: procure o primeiro espaço vazio e chame o método insert_item no indíce encontrado
        pass

    def pick_item(index: int) -> Item | None:
        """Remove um item do cinto na posição especificada. Retorna o item removido ou None se a posição estiver vazia."""
        pass

    def get_item(index: int) -> Item | None:
        """Retorna o item na posição especificada ou None se a posição estiver vazia."""
        pass
