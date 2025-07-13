from action import Actions, ActionType
from hero import Hero
from misc import clear_screen, typed_print
from room import Room

HERO_BASE_HEALTH = 100
HERO_BASE_ATTACK = 10
HERO_BELT_SIZE = 5
HERO_BELT_MAX_WEIGHT = 20
HERO_BACKPACK_SIZE = 50


class Game:
    player: Hero
    entry_room: Room

    def __init__(self):
        self.entry_room = setup_game_rooms()
        self.current_room = self.entry_room

    def __reset(self):
        clear_screen()
        typed_print("""Seu reino já fora governando por um rei que por uma conspiração fora morto, acusado de bruxaria.
Uma marca despertou na pele de todos os habitantes do reino, um sinal de que a maldição pelo rei prometida em seus últimos minutos começou.

Para impedir a terrível maldição que acabará com a vida de todos, você caminha até o antigo castelo onde a alma do rei está presa.
Mas cuidado, a maldição deu vida aos mais terríveis monstros já criados pela mente humana.

Diga o nome daquele que salvará o destino.""")

        player_name = input("> Digite o nome do herói: ").strip()
        if not player_name:
            player_name = "Herói Desconhecido"
        self.player = Hero(
            player_name,
            HERO_BASE_HEALTH,
            HERO_BASE_ATTACK,
            HERO_BELT_SIZE,
            HERO_BELT_MAX_WEIGHT,
        )

    def start(self):
        self.__reset()

        print("-" * 30)
        typed_print(
            f"\nVocê abre as portas do castelo e entra no {self.entry_room.name}."
        )

        actions = Actions()
        command_handlers = {
            # ActionType.SHOW_BELT: self.player.show_belt,
            # ActionType.USE_POTION: self.player.use_potion,
            # ActionType.EQUIP: self.player.equip_item,
            # ActionType.ATTACK: self.player.attack_monster,
            ActionType.SHOW_HELP: actions.show_help,
        }

        while True:
            typed_print(f"\nVocê está em {self.current_room.name}.")

            if self.current_room.chest is None and self.current_room.monster is None:
                typed_print("A sala está vazia.")
                # self.choose_direction()

            # if current_room.monster is not None:
            #     typed_print(f"Você se depara com um {current_room.monster.name}!")

            typed_print("Saídas disponíveis:")
            if self.current_room.exits.north:
                typed_print("- Norte")
            if self.current_room.exits.south:
                typed_print("- Sul")
            if self.current_room.exits.east:
                typed_print("- Leste")
            if self.current_room.exits.west:
                typed_print("- Oeste")

            command = input("> Sua ação: ").strip().lower()
            command = actions.match(command)
            if command is None:
                typed_print("Ação inválida")
                continue

            handler = command_handlers.get(command["action"])
            if handler:
                result = handler(**command)
                if result:
                    typed_print(result)


def setup_game_rooms() -> Room:
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

    room2 = Room("Sala 2 (monstro)")
    room3 = Room("Sala 3 (bau)")
    room4 = Room("Sala 4 (monstro)")
    room5 = Room("Sala 5 (vazia)")
    room6 = Room("Sala 6 (monstro e bau)")
    room7 = Room("Sala 7 (bau)")
    room8 = Room("Sala 8 (vazia)")
    room9 = Room("Sala 9 (bau)")
    room10 = Room("Sala 10 (monstro)")
    room11 = Room("Sala 11 (bau)")
    room12 = Room("Sala 12 (monstro)")
    room13 = Room("Sala 13 (monstro final)")
    room14 = Room("Sala 14 (bau)")

    entry_room.set_exits(south=room2, east=room4)

    room2.set_exits(east=room3)
    room3.set_exits(north=room4)
    room4.set_exits(east=room5)
    room5.set_exits(north=room6, south=room9, east=room8)
    room6.set_exits(east=room7)
    room7.set_exits(south=room8)
    room8.set_exits(east=room12)
    room9.set_exits(east=room10)
    room10.set_exits(east=room11)
    room11.set_exits(north=room12)
    room12.set_exits(east=room13)
    room13.set_exits(south=room14)

    return entry_room
