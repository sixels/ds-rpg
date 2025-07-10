from room import Room


def setup_rooms(entry_room: Room):
    """Configura as salas e suas conexões."""
    # Criando outras salas
    room2 = Room("Sala 2")
    room3 = Room("Sala 3")

    # Definindo as saídas
    entry_room.set_exits(north=room2, east=room3)


def main():
    """Função principal do jogo."""

    entry_room = Room("Sala 1")
    setup_rooms(entry_room)

    print("Bem-vindo ao jogo!")
    print("Você está na sala de entrada.")

    room = entry_room
    while True:
        print(f"\nVocê está na {room.name}.")
        print("Saídas disponíveis:")
        if room.exits.north:
            print("- Norte")
        if room.exits.south:
            print("- Sul")
        if room.exits.east:
            print("- Leste")
        if room.exits.west:
            print("- Oeste")
        command = (
            input(
                "Digite uma direção para se mover (norte, sul, leste, oeste) ou 'sair' para encerrar: "
            )
            .strip()
            .lower()
        )
        if command == "sair":
            print("Saindo do jogo. Até logo!")
            break

        if command == "norte" and room.exits.north:
            room = room.exits.north
        elif command == "sul" and room.exits.south:
            room = room.exits.south
        elif command == "leste" and room.exits.east:
            room = room.exits.east
        elif command == "oeste" and room.exits.west:
            room = room.exits.west
        else:
            print("Direção inválida ou não há saída nessa direção. Tente novamente.")
            continue


if __name__ == "__main__":
    main()
