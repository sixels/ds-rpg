from misc import typed_print
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

        command = input("sua ação > ").strip().lower()

        if command == "norte" and room.exits.north:
            room = room.exits.north
        elif command == "sul" and room.exits.south:
            room = room.exits.south
        elif command == "leste" and room.exits.east:
            room = room.exits.east
        elif command == "oeste" and room.exits.west:
            room = room.exits.west
        else:
            typed_print(
                "Direção inválida ou não há saída nessa direção. Tente novamente."
            )
            continue


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
