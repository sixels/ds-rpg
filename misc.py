# Funções variadas que podem ser úteis no jogo


def clear_screen():
    """Limpa a tela do console."""
    import os
    import platform

    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def typed_print(text: str, delay: float = 0.035):
    """Imprime o texto com um efeito de digitação."""
    import sys
    import time

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()  # Nova linha após o texto
