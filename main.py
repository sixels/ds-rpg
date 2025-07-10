from misc import typed_print
from room import Room


def setup_rooms(entry_room: Room):
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
    room14 = Room("Sala 14 (secreta)")

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


def main():
    """Função principal do jogo."""

    entry_room = Room("Sala 1")
    setup_rooms(entry_room)

    typed_print("Bem-vindo ao jogo! Pressione Ctrl+C para sair a qualquer momento.")

    room = entry_room
    while True:
        typed_print(f"\nVocê está na {room.name}.")
        typed_print("Saídas disponíveis:")
        if room.exits.north:
            typed_print("- Norte")
        if room.exits.south:
            typed_print("- Sul")
        if room.exits.east:
            typed_print("- Leste")
        if room.exits.west:
            typed_print("- Oeste")

        while True:
            command = input("sua ação > ").strip().lower()

            match command:
                case "norte":
                    if room.exits.north:
                        room = room.exits.north
                        break

                case "sul":
                    if room.exits.south:
                        room = room.exits.south
                        break
                case "leste":
                    if room.exits.east:
                        room = room.exits.east
                        break
                case "oeste":
                    if room.exits.west:
                        room = room.exits.west
                        break
                case _:
                    typed_print("Comando inválido. Tente novamente.")
                    continue
            typed_print("não há saídas nessa direção.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        pass
