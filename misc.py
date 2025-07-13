# Funções variadas que podem ser úteis no jogo


def clear_screen():
    """Limpa a tela do console."""
    import os
    import platform

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def typed_print(text: str, delay: float = 0.02):
    """Imprime o texto com um efeito de digitação."""
    import sys
    import select

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if select.select([sys.stdin], [], [], delay)[0]:
            sys.stdin.readline()
            delay = 0
    print()  # Nova linha após o texto
