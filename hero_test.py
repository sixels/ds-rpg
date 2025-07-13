from hero import Hero
from item import Weapon
from rarity import Rarity, RarityType


def test_hero_initialization():
    """Testa a inicialização do herói."""
    hero = Hero("Test Hero", 100, 10, 5, 20)

    assert hero.name == "Test Hero", "Nome do herói não corresponde."
    assert hero.base_health == 100, "Vida inicial do herói incorreta."
    assert hero.base_attack == 10, "Ataque inicial do herói incorreto."
    assert hero.belt.size == 5, "Tamanho do cinto do herói incorreto."
    assert hero.belt.max_weight == 20, "Peso máximo do cinto do herói incorreto."


def test_hero_belt_management():
    """Testa a inserção de itens no cinto do herói."""
    hero = Hero("Test Hero", 100, 10, 5, 25)
    sword = Weapon(
        "Espada", "", 10, Rarity(RarityType.Common, 20), 1
    )  # Exemplo de item
    spear = Weapon(
        "Lança", "", 15, Rarity(RarityType.Rare, 30), 2
    )  # Outro exemplo de item

    assert hero.belt.insert_item_on_empty_slot(sword), (
        "Item deve ser inserido no cinto."
    )

    assert hero.belt.current_weight == 10, (
        "Peso atual do cinto incorreto após inserção."
    )

    assert hero.belt.insert_item_on_empty_slot(spear), (
        "Segundo item deve ser inserido no cinto."
    )
    assert hero.belt.current_weight == 25, (
        "Peso atual do cinto incorreto após inserção do segundo item."
    )

    assert hero.use_item_from_belt(2) is False, (
        "Não deveria poder equipar item de uma posição vazia."
    )
    assert hero.belt.get_item(0) == sword, (
        "Item não encontrado na posição correta do cinto."
    )

    assert hero.use_item_from_belt(0), "Item não foi usado corretamente."
    assert hero.belt.get_item(0) is None, "Item deveria ter sido removido do cinto."

    assert hero.use_item_from_belt(1) is False, (
        "Não pode equipar dois itens ao mesmo tempo."
    )

    assert hero.store_equipped_item_in_belt(0) is True, (
        "Deveria conseguir armazenar o item equipado de volta no cinto."
    )
    assert hero.use_item_from_belt(1) is True, "Item na posição 1 deveria ser equipado."


if __name__ == "__main__":
    test_hero_initialization()
    test_hero_belt_management()
    print("Todos os testes passaram!")
