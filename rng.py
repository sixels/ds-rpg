import random

from typing import Callable

from item import Item
from rarity import Rarity


def random_range(min_value: int, max_value: int) -> int:
    """Gera um número aleatório entre min_value e max_value (inclusivo)."""
    return random.randint(min_value, max_value)


def pick_random_item(items: list[Item]) -> Item | None:
    """Escolhe um item aleatório da lista baseado nas raridades."""
    return pick_random_weighted_element(items, lambda item: item.rarity.weight)


def pick_random_rarity(rarities: list[Rarity]) -> Rarity:
    """Escolhe uma raridade aleatória da lista."""
    return pick_random_weighted_element(rarities, lambda r: r.weight)


def pick_random_weighted_element[T](
    elements: list[T], weight_function: Callable[[T], float]
) -> T | None:
    """Escolhe um item aleatório da lista baseado no peso."""
    weights = [weight_function(element) for element in elements]
    total_weight = sum(weights)
    if total_weight == 0:
        return None

    random_value = random.uniform(0, total_weight)
    current_weight = 0.0
    for i, element in enumerate(elements):
        current_weight += weights[i]
        if current_weight >= random_value:
            return element
    raise None
