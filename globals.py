from item import Potion, Weapon
from monster import Monster, MonsterType
from rarity import (
    RARITY_COMMON,
    RARITY_EPIC,
    RARITY_LEGENDARY,
    RARITY_RARE,
    RARITY_UNCOMMON,
)

# mudar os monstros, coloquei alguns exemplos
GAME_MONSTERS = [
    Monster(
        "Esqueleto",
        MonsterType.Undead,
        base_health=50,
        base_attack=7,
        level=1,
    ),
    Monster(
        "Zumbi",
        MonsterType.Undead,
        base_health=50,
        base_attack=5,
        level=1,
    ),
    Monster(
        "Lobisomem",
        MonsterType.Beast,
        base_health=40,
        base_attack=9,
        level=1,
    ),
    Monster(
        "Demônio Menor",
        MonsterType.Demon,
        base_health=60,
        base_attack=9,
        level=2,
    ),
    Monster(
        "Esqueleto com armadura",
        MonsterType.Undead,
        base_health=50,
        base_attack=7,
        level=2,
    ),
    Monster(
        "Vampiro Inferior",
        MonsterType.Vampire,
        base_health=80,
        base_attack=10,
        level=2,
    ),
    Monster(
        "Vampiro Superior",
        MonsterType.Vampire,
        base_health=80,
        base_attack=10,
        level=3,
    ),
    Monster(
        "Demônio Maior",
        MonsterType.Demon,
        base_health=60,
        base_attack=9,
        level=3,
    ),
    Monster(
        "Espírito do Rei",
        MonsterType.Spirit,
        base_health=150,
        base_attack=20,
        level=3,
    ),
]
GAME_WEAPONS = [
    Weapon(
        name="Espada Curta",
        description="Uma espada curta e afiada.",
        weight=4,
        rarity=RARITY_COMMON,
        damage=10,
    ),
    Weapon(
        name="Lança de Caça",
        description="Uma lança longa, perfeita para caçar criaturas maiores.",
        weight=10,
        rarity=RARITY_COMMON,
        damage=12,
        multiplier=lambda monster_type: 1.5 if monster_type == MonsterType.Beast else 1,
    ),
    Weapon(
        name="Estaca de Madeira",
        description="Uma estaca de madeira afiada, eficaz contra vampiros.",
        weight=3,
        rarity=RARITY_COMMON,
        damage=8,
        multiplier=lambda monster_type: 2.0
        if monster_type == MonsterType.Vampire
        else 1,
    ),
    Weapon(
        name="Machado Simples",
        description="Uma ferramenta robusta, pesada e afiada o suficiente para cortar mais do que apenas madeira.",
        weight=15,
        rarity=RARITY_COMMON,
        damage=15,
        multiplier=lambda monster_type: 1.2
        if monster_type == MonsterType.Undead
        else 1,
    ),
    Weapon(
        name="Porrete com Pregos",
        description="Um pedaço de madeira com pregos enferrujados. Brutal e intimidador.",
        weight=7,
        rarity=RARITY_COMMON,
        damage=11,
    ),
    # Uncommon weapons
    Weapon(
        name="Espada Longa",
        description="Uma espada longa e elegante, com um fio afiado.",
        weight=12,
        rarity=RARITY_UNCOMMON,
        damage=14,
        multiplier=lambda monster_type: 1.1
        if monster_type == MonsterType.Undead
        else 1,
    ),
    Weapon(
        name="Arco Longo",
        description="Um arco longo, perfeito para ataques à distância.",
        weight=13,
        rarity=RARITY_UNCOMMON,
        damage=10,
        multiplier=lambda monster_type: 1.5 if monster_type == MonsterType.Beast else 1,
    ),
    Weapon(
        name="Adaga Sacrificial",
        description="Uma adaga pequena, mas afiada, usada em rituais.",
        weight=5,
        rarity=RARITY_UNCOMMON,
        damage=6,
        multiplier=lambda monster_type: 1.5 if monster_type == MonsterType.Demon else 1,
    ),
    # Rare weapons
    Weapon(
        name="Martelo de Guerra",
        description="Um martelo pesado, capaz de esmagar armaduras.",
        weight=20,
        rarity=RARITY_RARE,
        damage=20,
    ),
    Weapon(
        name="Machado de Batalha",
        description="Um machado pesado, ideal para matar mortos-vivos.",
        weight=18,
        rarity=RARITY_RARE,
        damage=18,
        multiplier=lambda monster_type: 1.2
        if monster_type == MonsterType.Undead
        else 1,
    ),
    Weapon(
        name="Besta de Precisão",
        description="Uma besta de alta precisão, perfeita para caçar alvos distantes.",
        weight=15,
        rarity=RARITY_RARE,
        damage=16,
        multiplier=lambda monster_type: 1.5 if monster_type == MonsterType.Beast else 1,
    ),
    # Epic weapons
    Weapon(
        name="Espada Dracônica",
        description="Uma espada lendária forjada com escamas de dragão.",
        weight=28,
        rarity=RARITY_EPIC,
        damage=27,
    ),
    Weapon(
        name="Lança de Caçador de Demônios",
        description="Uma lança encantada por caçadores de demônios.",
        weight=22,
        rarity=RARITY_EPIC,
        damage=20,
        multiplier=lambda monster_type: 2.0 if monster_type == MonsterType.Demon else 1,
    ),
    Weapon(
        name="Arco Celestial",
        description="Um arco mágico que dispara flechas de luz.",
        weight=18,
        rarity=RARITY_EPIC,
        damage=22,
        multiplier=lambda monster_type: 1.5 if monster_type == MonsterType.Beast else 1,
    ),
    # Legendary weapons
    Weapon(
        name="O Rei Caído",
        description="Dizem que sua lâmina de aço pálido não corta metal ou carne, mas o próprio tecido do destino.",
        weight=30,
        rarity=RARITY_LEGENDARY,
        damage=45,
    ),
    Weapon(
        name="Sussurro Final",
        description="Uma adaga que parece absorver o som. Seus ataques são silenciosos e sempre encontram uma brecha na armadura. Causa dano extra em humanos e demônios.",
        weight=6,
        rarity=RARITY_LEGENDARY,
        damage=25,
        multiplier=lambda monster_type: 1.5
        if monster_type in [MonsterType.Human, MonsterType.Demon]
        else 1,
    ),
    Weapon(
        name="Alvorada, a Lâmina de Luz",
        description="Uma espada lendária que brilha com a luz do sol. Sua mera presença afasta as sombras. Causa dano extra em mortos-vivos, vampiros e espíritos.",
        weight=26,
        rarity=RARITY_LEGENDARY,
        damage=28,
        multiplier=lambda monster_type: 2.5
        if monster_type in [MonsterType.Undead, MonsterType.Vampire, MonsterType.Spirit]
        else 1,
    ),
]

GAME_POTIONS = [
    Potion(
        name="Poção de Cura Menor",
        description="Uma poção que cura ferimentos leves.",
        healing_amount=20,
        weight=1.0,
        rarity=RARITY_COMMON,
    ),
    Potion(
        name="Poção de Cura",
        description="Uma poção que cura ferimentos moderados.",
        healing_amount=40,
        weight=1.5,
        rarity=RARITY_UNCOMMON,
    ),
    Potion(
        name="Poção de Cura Avançada",
        description="Uma poção que cura ferimentos graves.",
        healing_amount=60,
        weight=2.0,
        rarity=RARITY_RARE,
    ),
    Potion(
        name="Poção de Cura Suprema",
        description="Uma poção que cura todos os ferimentos.",
        healing_amount=100,
        weight=3.0,
        rarity=RARITY_EPIC,
    ),
]

GAME_ITEMS = sorted(
    GAME_WEAPONS + GAME_POTIONS, key=lambda item: item.rarity.weight, reverse=True
)
