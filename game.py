from action import Actions, ActionType
from chest import (
    generate_random_chest,
    generate_common_chest,
    generate_epic_chest,
    generate_legendary_chest,
    generate_uncommon_chest,
)
from hero import Hero
from item import Item, Potion, Weapon
from misc import clear_screen, typed_print
from rarity import RARITY_COMMON
from room import Room
from globals import GAME_MONSTERS

HERO_BASE_HEALTH = 100
HERO_BASE_ATTACK = 5
HERO_BELT_SIZE = 5
HERO_BELT_MAX_WEIGHT = 15
HERO_BACKPACK_SIZE = 50


class Game:
    player: Hero
    entry_room: Room

    def __init__(self):
        self.entry_room, self.final_room = setup_game_rooms()
        self.current_room = self.entry_room

    def __reset(self):
        clear_screen()
        typed_print("""Seu reino já fora governado por um rei que por uma conspiração fora morto, acusado de bruxaria.
Uma marca despertou na pele de todos os habitantes do reino, um sinal de que a maldição pelo rei prometida em seus últimos minutos começou.

Para impedir a terrível maldição que acabará com a vida de todos, você caminha até o antigo castelo onde a alma do rei está presa.
Mas cuidado, a maldição deu vida aos mais terríveis monstros já criados pela mente humana.

Diga o nome daquele que salvará o destino.""")

        player_name = input("> Digite o nome do herói: ").strip()
        if not player_name:
            player_name = "Herói Desconhecido"

        typed_print(
            f'\nVocê será chamado de "{player_name}" nesta aventura! Se precisar de ajuda, digite "ajuda" para ver as ações disponíveis.'
        )

        self.player = Hero(
            player_name,
            HERO_BASE_HEALTH,
            HERO_BASE_ATTACK,
            HERO_BELT_SIZE,
            HERO_BELT_MAX_WEIGHT,
        )

        print("-" * 30)

    def start(self):
        self.__reset()

        actions = Actions()

        typed_print("\nVocê abre as portas e entra no castelo.")
        while self.player.is_alive():
            typed_print(f'\nVocê está em "{self.current_room.name}".')
            clear_screen()
            self.on_move_to_room()

            while True:
                try:
                    command = input("> Sua ação: ").strip().lower()
                except UnicodeDecodeError:
                    typed_print("Erro ao ler o comando. Tente novamente.")
                    continue
                command = actions.match(command)
                if command is None:
                    typed_print("Ação inválida")
                    continue

                if command["action"] not in self.valid_actions:
                    typed_print("Ação não permitida nesta situação.")
                    continue

                if self.on_action(command):
                    break

                if not self.player.is_alive():
                    typed_print("Você foi derrotado! Fim do jogo.")
                    break

                if not self.final_room.monster.is_alive():
                    typed_print(
                        "Você derrotou o espírito do rei e impediu a maldição de se espalhar.\n"
                        + f'Todos vão lembrar de "{self.player.name}" como o herói que salvou o reino!'
                    )
                    typed_print("Você completou o jogo!")
                    return

    def on_move_to_room(self) -> set:
        self.valid_actions: set = {
            ActionType.SHOW_HELP,
            ActionType.SHOW_ITEMS,
            ActionType.EQUIP_WEAPON,
            ActionType.USE_POTION,
            ActionType.DROP_ITEM,
            ActionType.STORE_ITEM,
            ActionType.UNEQUIP_WEAPON,
            ActionType.INSPECT,
            ActionType.SHOW_MAP,
        }

        # message = ""

        if self.current_room.monster and self.current_room.monster.is_alive():
            # message += f"Você se depara com um {self.current_room.monster.name} (level: {self.current_room.monster.level}, vida: {self.current_room.monster.base_health}).\n"

            self.valid_actions.add(ActionType.ATTACK)
        else:
            self.valid_actions.add(ActionType.MOVE)
            if self.current_room.chest:
                self.valid_actions.add(ActionType.PICK_ITEM)
                self.valid_actions.add(ActionType.STORE_ITEM)
                self.valid_actions.add(ActionType.SHOW_ITEMS)

            if self.current_room.dropped_items:
                self.valid_actions.add(ActionType.PICK_ITEM)
                self.valid_actions.add(ActionType.STORE_ITEM)
                self.valid_actions.add(ActionType.SHOW_ITEMS)

        self.handle_inspect({})
        # typed_print(message)

        # if ActionType.MOVE in self.valid_actions:
        #     typed_print("Saídas disponíveis:")
        #     if self.current_room.exits.north:
        #         typed_print("- Norte")
        #     if self.current_room.exits.south:
        #         typed_print("- Sul")
        #     if self.current_room.exits.east:
        #         typed_print("- Leste")
        #     if self.current_room.exits.west:
        #         typed_print("- Oeste")

        return self.valid_actions

    def on_action(self, command: dict) -> bool:
        command_handlers = {
            ActionType.INSPECT: self.handle_inspect,
            ActionType.MOVE: self.handle_move,
            ActionType.STORE_ITEM: self.handle_store_item,
            ActionType.DROP_ITEM: self.handle_drop_item,
            ActionType.USE_POTION: self.handle_use_potion,
            ActionType.EQUIP_WEAPON: self.handle_equip_weapon,
            ActionType.ATTACK: self.handle_attack,
            ActionType.SHOW_HELP: self.handle_help,
            ActionType.SHOW_ITEMS: self.handle_show_items,
            ActionType.PICK_ITEM: self.handle_pick_item,
            ActionType.UNEQUIP_WEAPON: self.handle_unequip_weapon,
            ActionType.SHOW_MAP: self.handle_show_map,
        }

        handler = command_handlers.get(command["action"])
        if handler:
            result = handler(command)
            return result
        else:
            typed_print("Ação não implementada.")

    def handle_help(self, _: dict) -> bool:
        """Mostra a ajuda."""
        actions = Actions()
        typed_print(actions.show_help)
        return False

    def handle_inspect(self, _: dict) -> bool:
        """Inspeciona o ambiente e o personagem."""
        typed_print(f"Você está em {self.current_room.name}.")
        self.player.health_bar.draw()
        typed_print(
            f"\nVocê está carregando {self.player.belt.current_weight} de peso no cinto (máximo: {self.player.belt.max_weight})."
        )
        for i, item in enumerate(self.player.belt.items):
            if item:
                show_item(item, listed=True)
            else:
                typed_print(f"  -{i + 1}: Vazio")

        print()
        if len(self.player.backpack.items) == 0:
            typed_print("Sua mochila está vazia.")
        else:
            typed_print(
                f"Você está com {len(self.player.backpack.items)} itens na mochila."
            )
            typed_print("Item no topo da mochila:")
            show_item(self.player.backpack.get_item(), listed=True)

        if self.player.equipped_item:
            typed_print(
                f"\nVocê está equipando: {self.player.equipped_item.name} (dano: {self.player.equipped_item.damage}, raridade: {self.player.equipped_item.rarity.type.value})"
            )

        if self.current_room.monster and self.current_room.monster.is_alive():
            typed_print(
                f"\nVocê vê um {self.current_room.monster.name} (level: {self.current_room.monster.level}, vida: {self.current_room.monster.base_health})."
            )
        else:
            if self.current_room.chest:
                typed_print(
                    f"\nVocê vê um baú {
                        'aberto' if self.current_room.chest_opened else 'fechado'
                    } no canto da sala."
                )
            if self.current_room.dropped_items:
                typed_print("Você vê alguns itens na sala")
                for item in self.current_room.dropped_items:
                    show_item(item, listed=True)

        if ActionType.MOVE in self.valid_actions:
            typed_print("\nSaídas disponíveis:")
            if self.current_room.exits.north:
                typed_print("- Norte")
            if self.current_room.exits.south:
                typed_print("- Sul")
            if self.current_room.exits.east:
                typed_print("- Leste")
            if self.current_room.exits.west:
                typed_print("- Oeste")

        typed_print(
            "\nAções disponíveis: "
            + ", ".join(action.value for action in self.valid_actions)
            + " use 'ajuda' para ver a lista em detalhes."
        )

        return False

    def handle_move(self, command: dict) -> bool:
        """Move o herói na direção especificada."""
        direction: str = command.get("direction")
        if direction not in ["norte", "sul", "leste", "oeste"]:
            typed_print("Direção inválida.")
            return False
        new_room = self.current_room.get_exit(direction)
        if new_room:
            self.current_room = new_room
            typed_print(f"Você abre a porta em direção {direction}.")
            return True
        else:
            typed_print("Não há saída nessa direção.")
            return False

    def handle_attack(self, command: dict) -> bool:
        """Ataca o monstro na sala atual."""
        if not self.current_room.monster or not self.current_room.monster.is_alive():
            typed_print("Não há monstros para atacar.")
            return False

        target = command.get("target")

        if target and target != "monstro" and target != self.current_room.monster.name:
            typed_print(f"Você não pode atacar {target} aqui.")
            return False

        # clear_screen()
        monster = self.current_room.monster
        _damage = self.player.attack(monster)
        monster.health_bar.draw()

        if not monster.is_alive():
            self.current_room.monster = None
            typed_print(
                f"{monster.name} foi derrotado! Você pode continuar explorando a sala."
            )

            self.on_move_to_room()
        else:
            _monster_damage = monster.attack(self.player)
            self.player.health_bar.draw()

        return False

    def handle_pick_item(self, command: dict) -> bool:
        """Armazena um item no cinto ou na mochila."""
        item = command.get("item")
        if not item:
            typed_print("Nenhum item especificado para armazenar.")
            return False
        item = item.lower()

        items_found = []

        if self.current_room.chest_opened:
            for chest_item in self.current_room.chest.list_itens():
                if chest_item.name().lower().startswith(item.lower()):
                    item = chest_item.pick_item()
                    items_found.append(item)
                    break
        if self.current_room.dropped_items:
            for dropped_item in self.current_room.dropped_items:
                if dropped_item.name.lower().startswith(item.lower()):
                    item = dropped_item
                    self.current_room.dropped_items.remove(dropped_item)
                    items_found.append(item)
                    break

        if not items_found:
            typed_print("Item não encontrado")
            return False

        if len(items_found) > 1:
            typed_print("Mais de um item encontrado.")
            for idx, found_item in enumerate(items_found, start=1):
                print(f"{idx}. ", end="")
                show_item(found_item, listed=False)
            while True:
                choice = input("> Qual item você deseja pegar? (digite o número): ")
                choice = int(choice) - 1
                if choice < 0 or choice >= len(items_found):
                    typed_print("Escolha inválida.")
                    continue
                item = items_found[choice]
                break
        else:
            item = items_found[0]

        while True:
            target = (
                input(
                    f'> Onde você deseja armazenar "{item.name}" (peso: {item.weight})? ({"equipar/" if type(item) is Weapon else ""}cinto/mochila): '
                )
                .strip()
                .lower()
            )

            if type(item) is Weapon and "equipar".startswith(target):
                if self.player.equipped_item:
                    typed_print(
                        f"Você já está equipando {self.player.equipped_item.name}. Guarde-o primeiro."
                    )
                    typed_print("Você derruba o item no chão.")
                    self.current_room.add_item(item)
                    return False
                self.player.equipped_item = item
                typed_print(f'Você equipa "{item.name}".')
                break
            elif "cinto".startswith(target):
                index = self.find_player_belt_empty_slot()
                if index == -1:
                    typed_print("Cinto cheio. Não é possível armazenar mais itens.")
                    typed_print("Você derruba o item no chão.")
                    self.current_room.add_item(item)
                    return False
                if self.player.store_item_in_belt(index, item):
                    typed_print(f'Você coloca "{item.name} no cinto.')
                else:
                    typed_print(
                        f'Você tenta colocar "{item.name}" no cinto, mas ele é muito pesado.'
                    )
                    typed_print("Você derruba o item no chão.")
                    self.current_room.add_item(item)
                break
            elif "mochila".startswith(target):
                if self.player.store_item_in_backpack(item):
                    typed_print(f'Você coloca "{item.name}" na mochila.')
                else:
                    typed_print("Não foi possível armazenar o item na mochila.")
                    typed_print("Você derruba o item no chão.")
                break
            else:
                typed_print("Destino inválido para armazenamento. Tente novamente.")

        return False

    def handle_store_item(self, command: dict) -> bool:
        """Armazena o item equipado, do chão ou do baú na mochila ou no cinto."""
        item = command.get("item")
        if not item:
            typed_print("Nenhum item especificado para armazenar.")
            return False
        item = item.lower()

        in_location = command.get("in")
        if not in_location:
            typed_print("Nenhum destino especificado para armazenar o item.")
            return False
        in_location = in_location.lower()

        item_found = False
        if "equipado".startswith(item) or "item equipado".startswith(item):
            if self.player.equipped_item:
                item = self.player.equipped_item
                self.player.equipped_item = None
                item_found = True
        elif (
            self.player.equipped_item
            and self.player.equipped_item.name.lower().startswith(item)
        ):
            item = self.player.equipped_item
            item_found = True
        else:
            room_item = self.take_item_from_room(item)
            if room_item:
                item = room_item
                item_found = True

        if not item_found:
            typed_print("Item não encontrado.")
            return False

        if "cinto".startswith(in_location):
            index = self.find_player_belt_empty_slot()
            if index == -1:
                typed_print(
                    "Seu cinto está cheio. Não é possível armazenar mais itens."
                )
                return False

            if self.player.store_item_in_belt(index, item):
                typed_print(f"{item.name} armazenado no cinto.")
            else:
                typed_print("Não foi possível armazenar o item no cinto.")
        elif "mochila".startswith(in_location):
            if self.player.store_item_in_backpack(item):
                typed_print(f"{item.name} armazenado na mochila.")
            else:
                typed_print("Não foi possível armazenar o item na mochila.")
        else:
            typed_print("Destino inválido para armazenamento.")
        return False

    def handle_drop_item(self, command: dict) -> bool:
        """Remove um item do cinto ou da mochila e o deixa na sala atual."""
        item = command.get("item")
        if not item:
            typed_print("Nenhum item especificado para remover.")
            return False
        item = item.lower()

        from_location = command.get("from")
        if not from_location:
            typed_print("Nenhum local especificado para remover o item.")
            return False
        from_location = from_location.lower()

        item_found = False
        if "cinto".startswith(from_location):
            for i in range(self.player.belt.size):
                belt_item = self.player.belt.get_item(i)
                if belt_item and belt_item.name.startswith(item):
                    item_found = True
                    item = self.player.belt.pick_item(i)

        elif "mochila".startswith(from_location):
            backpack_item = self.player.backpack.get_item()
            if backpack_item and backpack_item.name.startswith(item):
                item_found = True
                item = self.player.backpack.pick_item()
        else:
            typed_print("Local inválido para remoção do item.")
            return False

        if item_found:
            self.current_room.add_item(item)
            typed_print(f"{item.name} foi deixado na sala {self.current_room.name}.")
        else:
            typed_print(f"Item {item} não encontrado no {from_location}.")

        return False

    def handle_use_potion(self, command: dict) -> bool:
        """Usa uma poção do cinto ou da mochila."""
        item = command.get("item")
        if not item:
            typed_print("Nenhum item especificado para usar.")
            return False
        item_name = item.lower()

        from_location = command.get("from")

        if not from_location or "mochila".startswith(from_location):
            backpack_item = self.player.backpack.get_item()
            if backpack_item and backpack_item.name.lower().startswith(item_name):
                if type(backpack_item) is Potion:
                    if self.player.use_item_from_backpack():
                        typed_print(
                            f"Você usa {backpack_item.name} da mochila e recupera {backpack_item.healing_amount}.\nSua vida atual é {self.player.get_current_health()}."
                        )
                    else:
                        typed_print(
                            f"Não foi possível usar {backpack_item.name} da mochila."
                        )
                    return False
        if not from_location or "cinto".startswith(from_location):
            found_items: list[tuple[int, Item]] = []
            for i in range(self.player.belt.size):
                belt_item = self.player.belt.get_item(i)
                if belt_item and belt_item.name.lower().startswith(item_name):
                    found_items.insert(0, (i, belt_item))

            if len(found_items) == 1:
                i, belt_item = found_items[0]
                if type(belt_item) is Potion:
                    if self.player.use_item_from_belt(i):
                        typed_print(
                            f"Você usa {belt_item.name} do cinto e recupera {belt_item.healing_amount}.\nSua vida atual é {self.player.get_current_health()}."
                        )
                    else:
                        typed_print(f"Não foi possível usar {belt_item.name} do cinto.")
                    return False
            elif len(found_items) > 1:
                typed_print("Mais de um item encontrado no cinto.")
                for idx, (i, belt_item) in enumerate(found_items, start=1):
                    print(f"{idx}. ", end="")
                    show_item(belt_item, listed=False)
                while True:
                    choice = input("> Qual poção você deseja usar? (digite o número): ")
                    try:
                        choice = int(choice) - 1
                    except ValueError:
                        typed_print("Entrada inválida. Digite um número.")
                        continue

                    if choice < 0 or choice >= len(found_items):
                        typed_print("Escolha inválida.")
                        continue
                    i, belt_item = found_items[choice]
                    if type(belt_item) is Potion:
                        if self.player.use_item_from_belt(i):
                            typed_print(
                                f"Você usa {belt_item.name} do cinto e recupera {belt_item.healing_amount}.\nSua vida atual é {self.player.get_current_health()}."
                            )
                        else:
                            typed_print(
                                f"Não foi possível usar {belt_item.name} do cinto."
                            )
                        return False

        typed_print(f"Item {item} não encontrado.")
        return False

    def handle_show_items(self, command: dict) -> bool:
        """Mostra os itens no cinto, mochila ou baú."""
        target = command.get("target", "").lower()

        if "cinto".startswith(target):
            typed_print("Itens no cinto:")
            for item in self.player.belt.items:
                if item:
                    show_item(item, listed=True)
                else:
                    typed_print("  - Vazio")

        elif "mochila".startswith(target):
            if len(self.player.backpack.items) == 0:
                typed_print("Sua mochila está vazia.")
                return False

            typed_print("Itens na mochila:")
            for item in reversed(self.player.backpack.items):
                show_item(item, listed=True)

        elif "baú".startswith(target) or "bau".startswith(target):
            if not self.current_room.chest:
                typed_print("Você não vê nenhum baũ na sala.")
                return False

            self.current_room.chest_opened = True
            typed_print("Itens no baú:")
            for item in self.current_room.chest.list_itens():
                show_item(item.view_item(), listed=True)
        elif "sala".startswith(target) or "sala atual".startswith(target):
            if not self.current_room.dropped_items:
                typed_print("Você não vê nenhum item na sala.")
                return False

            typed_print(f"Itens na sala {self.current_room.name}:")
            for item in self.current_room.dropped_items:
                show_item(item, listed=True)
        else:
            typed_print("Destino inválido para mostrar itens.")

        return False

    def handle_equip_weapon(self, command: dict) -> bool:
        """Equipa uma arma do cinto ou da mochila."""
        item_name = command.get("item")
        if not item_name:
            typed_print("Nenhum item especificado para equipar.")
            return False
        item_name = item_name.lower()

        from_location = command.get("from")

        if from_location is None or "cinto".startswith(from_location):
            for i in range(self.player.belt.size):
                belt_item = self.player.belt.get_item(i)
                if belt_item and belt_item.name.lower().startswith(item_name):
                    if type(belt_item) is Weapon:
                        if self.player.use_item_from_belt(i):
                            typed_print(f"Equipou {belt_item.name} do cinto.")
                        else:
                            typed_print(
                                f"Não foi possível equipar {belt_item.name} do cinto."
                            )
                        return False

        if from_location is None or "mochila".startswith(from_location):
            backpack_item = self.player.backpack.get_item()
            if backpack_item and backpack_item.name.lower().startswith(item_name):
                if type(backpack_item) is Weapon:
                    if self.player.use_item_from_backpack():
                        typed_print(f"Equipou {backpack_item.name} da mochila.")
                    else:
                        typed_print(
                            f"Não foi possível equipar {backpack_item.name} da mochila."
                        )
                    return False

        if (
            from_location is None
            or "chão".startswith(from_location)
            or "sala".startswith(from_location)
        ):
            item = self.take_item_from_floor(item_name)
            if item and type(item) is Weapon:
                if self.player.equipped_item:
                    typed_print(
                        f"Você já está equipando {self.player.equipped_item.name}. Guarde-o primeiro."
                    )
                    typed_print("Você derruba o item no chão.")
                    self.current_room.add_item(item)
                    return False
                self.player.equipped_item = item
                typed_print(f'Você equipa "{item.name}".')
                return False

        if (
            from_location is None
            or "bau".startswith(from_location)
            or "baú".startswith(from_location)
        ):
            if not self.current_room.chest_opened:
                typed_print("O baú não está aberto.")
                return False

            for chest_item in self.current_room.chest.list_itens():
                if chest_item.name().lower().startswith(item_name):
                    item = chest_item.view_item()
                    if type(item) is Weapon:
                        if self.player.equipped_item:
                            typed_print(
                                f"Você já está equipando {self.player.equipped_item.name}. Guarde-o primeiro."
                            )
                            return False
                        self.player.equipped_item = chest_item.pick_item()
                        typed_print(f'Você equipa "{self.player.equipped_item.name}".')
                        return False

        typed_print(f"Item {item_name} não encontrado.")
        return False

    def handle_unequip_weapon(self, _: dict) -> bool:
        """Desequipa a arma equipada."""
        if self.player.equipped_item:
            while True:
                target = (
                    input(
                        f'> Onde você deseja colocar "{self.player.equipped_item.name}"? (cinto/mochila): '
                    )
                    .strip()
                    .lower()
                )
                if "cinto".startswith(target):
                    index = self.find_player_belt_empty_slot()
                    if index == -1:
                        typed_print("Cinto cheio. Não é possível armazenar mais itens.")
                        return False
                    if self.player.store_item_in_belt(index, self.player.equipped_item):
                        typed_print(
                            f'Você coloca "{self.player.equipped_item.name}" no cinto.'
                        )
                        self.player.equipped_item = None
                    else:
                        typed_print(
                            f'Não foi possível colocar "{self.player.equipped_item.name}" no cinto.'
                        )
                    break
                elif "mochila".startswith(target):
                    if self.player.store_item_in_backpack(self.player.equipped_item):
                        typed_print(
                            f'Você coloca "{self.player.equipped_item.name}" na mochila.'
                        )
                        self.player.equipped_item = None
                    else:
                        typed_print(
                            f'Não foi possível colocar "{self.player.equipped_item.name}" na mochila.'
                        )
                    break
                else:
                    typed_print("Destino inválido para armazenamento. Tente novamente.")
        else:
            typed_print("Você não está equipando nenhuma arma.")
        return False

    def handle_show_map(self, _: dict) -> bool:
        """Mostra o mapa do jogo."""
        typed_print("""
                         sala 6 -- sala 7
                           |         |
    entrada -- sala 4 -- sala 5 -- sala 8 --  sala 12 - sala 13
      |         |          |                    |
    sala 2 -- sala 3     sala 9 -- sala 10 -- sala 11
                                     |
                                   sala 14
""")
        return False

    def take_item_from_room(self, item_name: str) -> Item | None:
        """Procura um item pelo nome na sala atual."""
        if self.current_room.chest_opened:
            for chest_item in self.current_room.chest.list_itens():
                if chest_item.name().lower().startswith(item_name.lower()):
                    return chest_item.pick_item()

        for dropped_item in self.current_room.dropped_items:
            if dropped_item.name.lower().startswith(item_name.lower()):
                self.current_room.dropped_items.remove(dropped_item)
                return dropped_item

        return None

    def take_item_from_floor(self, item_name: str) -> Item | None:
        """Procura um item pelo nome no chão da sala atual."""
        for dropped_item in self.current_room.dropped_items:
            if dropped_item.name.lower().startswith(item_name.lower()):
                self.current_room.dropped_items.remove(dropped_item)
                return dropped_item
        return None

    def find_player_belt_empty_slot(self) -> int:
        """Encontra o primeiro espaço vazio no cinto do jogador."""
        for i, item in enumerate(self.player.belt.items):
            if item is None:
                return i
        return -1


def setup_game_rooms() -> tuple[Room, Room]:
    """
    Configura as salas e suas conexões.

                         sala 6 -- sala 7
                           |         |
    entrada -- sala 4 -- sala 5 -- sala 8 --  sala 12 - sala 13
      |         |          |                    |
    sala 2 -- sala 3     sala 9 -- sala 10 -- sala 11
                                     |
                                   sala 14
    """

    entry_room = Room("Hall de Entrada")

    room2 = Room("Posto da Guarda")
    room3 = Room("Arsenal")
    room4 = Room("Corredor Principal")
    room5 = Room("Corredor Principal")
    room6 = Room("Biblioteca")
    room7 = Room("Aposentos do Rei")
    room8 = Room("Salão do Trono Despedaçado")
    room9 = Room("Cozinha")
    room10 = Room("Salão de Jantar")
    room11 = Room("Capela da Vigília")
    room12 = Room("Jardim Real")
    room13 = Room("Câmara de execução")
    room14 = Room("Sala do Tesouro")

    entry_room.set_exits(south=room2, east=room4)

    room2.set_exits(east=room3)
    room2.set_monster(GAME_MONSTERS[0])
    room2.set_chest(generate_common_chest())

    room3.set_exits(north=room4)
    room3.set_chest(generate_uncommon_chest())

    room4.set_exits(east=room5)
    room4.set_chest(generate_random_chest())

    room5.set_exits(north=room6, south=room9, east=room8)
    room5.set_monster(GAME_MONSTERS[1])
    room5.set_chest(generate_random_chest())

    room6.set_exits(east=room7)
    room6.set_monster(GAME_MONSTERS[3])

    room7.set_exits(south=room8)
    room7.set_chest(generate_epic_chest())

    room8.set_exits(east=room12)
    room8.set_monster(GAME_MONSTERS[5])
    room8.set_chest(generate_random_chest())

    room9.set_exits(east=room10)
    room9.set_monster(GAME_MONSTERS[2])

    room10.set_exits(east=room11, south=room14)
    room10.set_monster(GAME_MONSTERS[4])
    room10.set_chest(generate_epic_chest())

    room11.set_exits(north=room12)
    room11.set_chest(generate_random_chest())

    room12.set_exits(east=room13)
    room12.set_monster(GAME_MONSTERS[7])
    room12.set_chest(generate_random_chest())

    room13.set_monster(GAME_MONSTERS[8])

    room14.set_chest(generate_legendary_chest())

    assert entry_room.exits.south == room2, (
        "Erro ao definir a saída sul da sala de entrada."
    )
    entry_room.add_item(
        Weapon(
            "Espada de Ferro Enferrujada",
            "Uma espada simples, mas afiada o suficiente para cortar carne.",
            6,
            RARITY_COMMON,
            4,
        )
    )
    entry_room.add_item(
        Potion(
            "Poção de Cura",
            "Uma poção que cura ferimentos leves.",
            healing_amount=20,
            weight=1.0,
            rarity=RARITY_COMMON,
        )
    )

    return entry_room, room13


def show_item(item: Item, listed: bool = False):
    if listed:
        print("  - ", end="")
    if type(item) is Weapon:
        typed_print(
            f"{item.name} (dano: {item.damage}, peso: {item.weight}, raridade: {item.rarity.type.value})\n{' ' if listed else ''}{item.description}"
        )
    elif type(item) is Potion:
        typed_print(
            f"{item.name} (cura: {item.healing_amount}, peso: {item.weight}, raridade: {item.rarity.type.value})\n{' ' if listed else ''}{item.description}"
        )
